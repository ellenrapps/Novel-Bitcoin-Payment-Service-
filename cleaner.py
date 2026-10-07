# AGPL-3.0 License. Copyright © 2026 Ellen Red

import logging
import re
from decimal import Decimal, InvalidOperation


MAX_BTC = Decimal('21000000')


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    
    class SensitiveDataFilter(logging.Filter):
        SENSITIVE_FIELDS = {'self.explorer_log_user', 'self.explorer_log_pass', 'self.explorer_check_address_ent', 'self.rpc_username', 'self.rpc_auth_header', 'self.recipient_address_ent', 'self.send_amount_ent', 'self.send_message_ent', 'self.content_key_address', 'self.create_address_key_text', 'username',
            'password', 'credentials', 'encoded', 'auth_header', 'self.display_result', 'addr', 'tweaked_privkey', 'tweaked_pubkey', 'recipient_addr', 'address', 'send_amount',
            }

        def __init__(self):
            super().__init__()
            fields_alt = "|".join(re.escape(f) for f in self.SENSITIVE_FIELDS)
            self._pattern = re.compile(
                rf'(?P<key>("?{fields_alt}"?)\s*[:=]\s*)'
                rf'(?P<sep>["\']?\$?)'
                rf'(?P<value>[^"\',\s}}\]]+)',
                re.IGNORECASE,
            )

        def filter(self, record: logging.LogRecord) -> bool:
            msg = record.getMessage()
            msg = self._pattern.sub(
                lambda m: f'{m.group("key")}{m.group("sep")}***',
                msg,
            )
            record.msg = msg
            record.args = ()
            return True

    root_logger = logging.getLogger()
    if not any(isinstance(f, SensitiveDataFilter) for f in root_logger.filters):
        root_logger.addFilter(SensitiveDataFilter())


def is_btc_amount_valid(amount_str: str) -> tuple[bool, str]:
    s = amount_str.strip()

    if not s:
        return False

    if s.startswith('-'):
        return False

    if '.' in s:
        parts = s.split('.')
        if len(parts) > 2:
            return False
        integer_part, fractional_part = parts
    else:
        integer_part = s
        fractional_part = ''

    if not integer_part:
        return False

    if not integer_part.isdigit():
        return False

    if fractional_part and not fractional_part.isdigit():
        return False

    if len(fractional_part) > 8:
        return False

    try:
        value = Decimal(s)
    except InvalidOperation:
        return False

    if value > MAX_BTC:
        return False

    return True


def is_op_return_message_valid(message: str, max_bytes: int = 80) -> tuple[bool, str]:
    cleaned = message.strip()

    if not cleaned:
        return True

    try:
        raw = cleaned.encode('utf-8')
    except UnicodeEncodeError:
        return False

    if len(raw) > max_bytes:
        return False

    return True
