# AGPL-3.0 License. Copyright © 2026 Ellen Red

import logging
import re


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    
    class SensitiveDataFilter(logging.Filter):
        SENSITIVE_FIELDS = {'username', 'password', 'credentials', 'encoded', 'auth_header', 'address_pu', 'address_textbox_content', 'addr', 'tweaked_privkey', 'tweaked_pubkey', 'self.rpc_username', 'self.rpc_auth_header', 'self.content_key_address', 'Address', 'Private Key', 'Public Key',}

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
