# AGPL-3.0 License. Copyright © 2026 Ellen Red


import json
import urllib.request
import urllib.error
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed


def call_rpc(
    host: str,
    port: int,
    username: str,
    auth_header: str,
    method: str,
    params: Optional[List[Any]] = None,
) -> Dict[str, Any]:

    url = f'http://{'127.0.0.1'}:{18332}'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'python-explorer-client/2026-secure',
        'Authorization': auth_header,
    }

    payload = {
        'jsonrpc': '2.0',
        'id': 'explorer-call',
        'method': method,
        'params': params if params is not None else []
    }
    json_data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            raw_data = response.read()
            
            if len(raw_data) == 0:
                return {
                    'success': False,
                    'data': 'Empty response from the RPC server.',
                    'error_code': None
                }

            text_data = raw_data.decode('utf-8', errors='strict')
            result = json.loads(text_data)

            if not isinstance(result, dict):
                return {
                    'success': False,
                    'data': 'Unexpected response format from the RPC server.',
                    'error_code': None
                }

            if 'error' in result and result['error'] is not None:
                err = result['error']
                
                if isinstance(err, dict):
                    code = err.get('code')
                    message = err.get('message', 'Unknown RPC error')
                    data_payload = err.get('data')
                    
                    if code == -5:
                        final_msg = f"RPC Validation Error (-5): {message}"
                        
                        return {
                            'success': False,
                            'data': final_msg,
                            'error_code': -5,          
                            'raw_error': err          
                        }
                        
                        
                    else:
                        return {
                            'success': False,
                            'data': f'RPC Error ({code}): {message}',
                            'error_code': code,
                            'raw_error': err
                        }
                else:
                    return {
                        'success': False,
                        'data': f'RPC Error: {str(err)}',
                        'error_code': None
                    }

            if 'result' not in result:
                return {
                    'success': False,
                    'data': 'Missing "result" field in the RPC response.',
                    'error_code': None
                }

            return {
                'success': True, 
                'data': result['result'],
                'error_code': None
            }

    except urllib.error.HTTPError as e:
        reason = e.reason if e.reason else 'Unknown HTTP error'
        return {
            'success': False,
            'data': f'HTTP Error {e.code}: {reason}',
            'error_code': e.code
        }

    except urllib.error.URLError as e:
        reason_str = str(e.reason) if e.reason else 'Unknown connection issue'
        if 'Connection refused' in reason_str or 'ECONNREFUSED' in reason_str:
            return {
                'success': False,
                'data': 'Connection Refused: Is bitcoind running and bound to localhost?',
                'error_code': 'ECONNREFUSED'
            }
        return {
            'success': False,
            'data': 'Failed to connect to the RPC service.',
            'error_code': 'CONNECTION_FAILED'
        }

    except json.JSONDecodeError:
        return {
            'success': False,
            'data': 'Invalid JSON received from the RPC server.',
            'error_code': 'JSON_DECODE_ERROR'
        }

    except Exception as e:
        return {
            'success': False,
            'data': f'An unexpected error occurred: {str(e)}',
            'error_code': 'UNEXPECTED'
        }


#####################
# Get Blockchain Info
#####################
def get_blockchain_info(host: str, port: int, username:str, auth_header: str) -> Dict[str, Any]:
    resp = call_rpc(host, port, username, auth_header, 'getblockchaininfo')

    if not resp['success']:
        return resp

    formatted_json = json.dumps(resp['data'], indent=4, separators=(',', ': '))
    return {
        'success': True,
        'data': (
            f'✅ Connected to Local Bitcoin Node'
        ),
    }

#######################
# Create or Load Wallet
#######################
def create_or_load_wallet(
    host: str,
    port: int,
    username: str,
    auth_header: str,
    wallet_name: str
) -> Dict[str, Any]:
    resp = call_rpc(host, port, username, auth_header, 'listwallets')
    if not resp.get('success'):
        return resp

    wallets = resp.get('data', [])
    if wallet_name in wallets:
        return {'success': True, 'data': wallet_name}

    resp = call_rpc(
        host,
        port,
        username,
        auth_header,
        'createwallet',
        [
            wallet_name,
            True, 
            False,
            '',    
            False  
        ]
    )

    if resp.get('success'):
        return resp

    error_msg = resp.get('data', '')
    if 'Database already exist' in error_msg or '-18' in error_msg:
        load_resp = call_rpc(
            host,
            port,
            username,
            auth_header,
            'loadwallet',
            [wallet_name]
        )
        if load_resp.get('success'):
            return {'success': True, 'data': wallet_name}
        else:
            return load_resp

    return resp

################
# Add Public Key
################
def get_descriptor_with_checksum(host, port, username, auth_header, descriptor):
    resp = call_rpc(
        host=host,
        port=port,
        username=username,
        auth_header=auth_header,
        method='getdescriptorinfo',
        params=[descriptor]
    )
    if not resp.get('success'):
        raise RuntimeError(f"getdescriptorinfo failed: {resp.get('data')}")
    info = resp['data']
    return info['descriptor']


def rpc_add_pubkey(
    host: str,
    port: int,
    username: str,
    auth_header: str,    
    pubkey_hex: str,
    label: str = '#1',
    timestamp: str | int = 'now'
) -> Dict[str, Any]:
    if not isinstance(pubkey_hex, str) or not re.fullmatch(r'[0-9a-fA-F]+', pubkey_hex):
        return {'success': False, 'data': 'Public key must be a valid hex string.'}

    pubkey_len = len(pubkey_hex)
    if pubkey_len != 64:
        return {
            'success': False,
            'data': (
                f"Invalid public key length for Taproot. Expected 64 hex chars (32 bytes). "
                f"Got {pubkey_len}."
            )
        }

    base_descriptor = f"tr({pubkey_hex})"

    try:
        descriptor_with_checksum = get_descriptor_with_checksum(
            host, port, username, auth_header, base_descriptor
        )
    except Exception as e:
        return {'success': False, 'data': f"Failed to compute descriptor checksum: {e}"}

    try:
        list_resp = call_rpc(
            host=host,
            port=port,
            username=username,
            auth_header=auth_header,
            method='listdescriptors',
            params=[]
        )
    except Exception as e:
        return {'success': False, 'data': f"RPC call 'listdescriptors' failed: {e}"}

    if list_resp.get('success'):
        existing_descriptors = list_resp.get('data', {}).get('descriptors', [])
        for entry in existing_descriptors:
            existing_desc = entry.get('desc', '')
            if pubkey_hex in existing_desc and entry.get('next', 0) == 0:
                return {
                    'success': False,
                    'data': f"Public key {pubkey_hex} is already imported as a watch-only descriptor."
                }
    else:
        error_msg = list_resp.get('data', '')
        return {'success': False, 'data': f"'listdescriptors' failed: {error_msg}"}
    
    descriptor_entry = {
        'desc': descriptor_with_checksum,
        'active': False,
        'internal': False,
        'watchonly': True,
        'label': label,
        'timestamp': timestamp
    }

    try:
        resp = call_rpc(
            host=host,
            port=port,
            username=username,
            auth_header=auth_header,
            method='importdescriptors',
            params=[[descriptor_entry]]
        )
    except Exception as e:
        return {'success': False, 'data': f"RPC call failed: {e}"}

    if resp.get('success'):
        return {'success': True, 'data': resp.get('data')}
    else:
        error_msg = resp.get('data', '')
        return {'success': False, 'data': error_msg}

#############################################
# Get Address Balance and Transaction Details
#############################################
def _is_valid_taproot_testnet_address(address: str) -> bool:
    if not isinstance(address, str):
        return False

    if len(address) < 42 or len(address) > 90:
        return False

    if not address.startswith('tb1p'):
        return False

    if not re.fullmatch(r'[a-z0-91]+', address):
        return False

    parts = address.split('1')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return False

    return True


def rpc_scan_address_utxos(
    host: str,
    port: int,
    username: str,
    auth_header: str,
    address: str
) -> Dict[str, Any]:
    if not _is_valid_taproot_testnet_address(address):
        return {
            'success': False,
            'data': (
                'Address is not a valid Testnet Taproot (tb1p...) address. '
                'Only Testnet Taproot addresses are allowed.'
            )
        }

    try:
        resp = call_rpc(
            host=host,
            port=port,
            username=username,
            auth_header=auth_header,
            method='scantxoutset',
            params=['start', [f"addr({address})"]]
        )
    except Exception as e:
        return {'success': False, 'data': f"RPC call 'scantxoutset' failed: {e}"}

    if not resp.get('success'):
        return resp

    result = resp.get('data', {})
    if not result.get('success'):
        err_msg = result.get('error', {}).get('message', 'Unknown scantxoutset error')
        return {'success': False, 'data': err_msg}

    unspents = result.get('unspents', [])

    total_balance = Decimal('0')
    for u in unspents:
        amount_str = str(u.get('amount', '0'))
        try:
            total_balance += Decimal(amount_str)
        except InvalidOperation:
            return {
                'success': False,
                'data': f"Invalid amount value found in UTXO: {u.get('amount')}"
            }

    return {
        'success': True,
        'data': {
            'unspents': unspents,
            'total_balance': total_balance,
        }
    }


def rpc_get_transaction_details(
    host: str,
    port: int,
    username: str,
    auth_header: str,
    txid: str
) -> Dict[str, Any]:
    if not isinstance(txid, str):
        return {'success': False, 'data': 'TXID must be a string.'}

    txid = txid.strip()
    if len(txid) != 64 or not re.fullmatch(r'[0-9a-fA-F]+', txid):
        return {'success': False, 'data': 'TXID must be a valid 64-character hex string.'}

    try:
        resp = call_rpc(
            host=host,
            port=port,
            username=username,
            auth_header=auth_header,
            method='getrawtransaction',
            params=[txid, True]  # decoded JSON
        )
    except Exception as e:
        return {'success': False, 'data': f"RPC call 'getrawtransaction' failed: {e}"}

    if not resp.get('success'):
        return resp

    tx_data = resp.get('data')
    if tx_data is None:
        return {'success': False, 'data': 'No transaction data returned.'}

    return {'success': True, 'data': tx_data}


def _normalize_tx_for_sorting(tx: Dict[str, Any]) -> int:
    block_height = tx.get('blockheight')
    confirmations = tx.get('confirmations', 0)

    if block_height is not None and block_height >= 0:
        return block_height
    elif confirmations > 0:
        return confirmations
    else:
        return 0


def fetch_latest_balance_transactions(
    host: str,
    port: int,
    username: str,
    auth_header: str,
    address: str,
    limit: int = 5
) -> Dict[str, Any]:
    if not _is_valid_taproot_testnet_address(address):
        return {
            'success': False,
            'data': (
                'Address is not a valid Testnet Taproot (tb1p...) address. '
                'Only Testnet Taproot addresses are allowed.'
            )
        }

    scan_res = rpc_scan_address_utxos(host, port, username, auth_header, address)
    if not scan_res['success']:
        return scan_res

    scan_data = scan_res['data']
    unspents = scan_data['unspents']
    total_balance = scan_data['total_balance']

    txids = list({u['txid'] for u in unspents})

    detailed_txs: List[Dict[str, Any]] = []
    seen_txids = set()

    def fetch_tx(txid: str):
        if txid in seen_txids:
            return None
        seen_txids.add(txid)
        tx_res = rpc_get_transaction_details(host, port, username, auth_header, txid)
        return txid, tx_res

    if txids:
        with ThreadPoolExecutor(max_workers=min(10, len(txids))) as executor:
            futures = {executor.submit(fetch_tx, txid): txid for txid in txids}
            for future in as_completed(futures):
                result = future.result()
                if result is None:
                    continue
                txid, tx_res = result

                if not tx_res['success']:
                    detailed_txs.append({
                        'txid': txid,
                        'error': tx_res['data'],
                        'inputs': [],
                        'outputs': []
                    })
                    continue

                tx = tx_res['data']
                confirmations = tx.get('confirmations', 0)
                if confirmations <= 0:
                    continue

                inputs = []
                for vin in tx.get('vin', []):
                    inputs.append({
                        'txid': vin.get('txid'),
                        'vout': vin.get('vout'),
                        'sequence': vin.get('sequence'),
                        'scriptSig': vin.get('scriptSig', {}).get('hex', ''),
                        'txinwitness': vin.get('txinwitness', [])
                    })

                outputs = []
                for i, vout in enumerate(tx.get('vout', [])):
                    outputs.append({
                        'index': i,
                        'value': str(vout.get('value', '0')),
                        'scriptPubKey': {
                            'asm': vout.get('scriptPubKey', {}).get('asm', ''),
                            'hex': vout.get('scriptPubKey', {}).get('hex', ''),
                            'type': vout.get('scriptPubKey', {}).get('type', ''),
                            'addresses': vout.get('scriptPubKey', {}).get('addresses', [])
                        }
                    })

                detailed_txs.append({
                    'txid': tx.get('txid'),
                    'blockheight': tx.get('blockheight'),
                    'confirmations': confirmations,
                    'time': tx.get('time'),
                    'inputs': inputs,
                    'outputs': outputs,
                    'size': tx.get('size'),
                    'weight': tx.get('weight'),
                    'version': tx.get('version'),
                    'locktime': tx.get('locktime'),
                })

    detailed_txs.sort(key=_normalize_tx_for_sorting, reverse=True)
    latest_txs = detailed_txs[:limit]

    return {
        'success': True,
        'data': {
            'address': address,
            'total_balance': total_balance,
            'utxo_count': len(unspents),
            'confirmed_transactions_found': len(detailed_txs),
            'transactions': latest_txs,
            'raw_unspents': unspents
        }
    }
