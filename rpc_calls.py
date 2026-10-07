# AGPL-3.0 License. Copyright © 2026 Ellen Red

import json
import urllib.request
import urllib.error
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed


def call_rpc(
    host: str,
    port: int,
    auth_header: str,
    method: str,
    params: Optional[List[Any]] = None,
) -> Dict[str, Any]:

    url = f'http://{host}:{port}'
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
        with urllib.request.urlopen(req, timeout=60) as response:
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
                        final_msg = f'RPC Validation Error (-5): {message}'
                        
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


#################
# Blockchain Info
#################
def get_blockchain_info_v1(host, port, auth_header) -> Dict[str, Any]:
    resp = call_rpc(host, port, auth_header, 'getblockchaininfo')

    if not resp['success']:
        return resp

    return {
        'success': True,
        'data': f'✅ Connection Status: Successfully connected to Bitcoin Testnet4 node.'
    }


def get_blockchain_info_v2(host, port, auth_header) -> Dict[str, Any]:
    try:
        resp = call_rpc(host, port, auth_header, 'getblockchaininfo')
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'is_synced': None,
        }

    if not resp.get('success'):
        return resp

    data = resp.get('data', {})
    if not isinstance(data, dict):
        return {
            'success': False,
            'error': 'Unexpected response format: "data" is not a dict',
            'is_synced': None,
        }

    initial_block_download: Optional[bool] = data.get('initialblockdownload')
    is_synced = initial_block_download is False
    status_code = (
        'SYNCED' if is_synced
        else 'DOWNLOADING' if initial_block_download is True
        else 'UNKNOWN'
    )

    return {
        'success': True,
        'is_synced': is_synced,
        'status_code': status_code,
        'sync_details': {
            'initialblockdownload': initial_block_download,
        },
    }


####################
# Address Validation
####################
def validate_address(
    host: str,
    port: int,
    auth_header: str,
    address: str
) -> Dict[str, Any]:
    resp = call_rpc(host, port, auth_header, 'validateaddress', [address])

    if not resp['success']:
        return resp

    result = resp['data']

    is_valid = result.get('isvalid', False)

    if not is_valid:
        return {
            'success': False,
            'data': f'Address "{address}" is not a valid Bitcoin Testnet Taproot (Bech32m) address.'
        }

    is_witness = result.get('iswitness', False)
    witness_version = result.get('witness_version')
    witness_program = result.get('witness_program', '')

    if not is_witness:
        return {
            'success': False,
            'data': (
                f'Address "{address}" is valid but NOT a SegWit (bech32/bech32m) address. '
                f'Only Taproot (bech32m, tb1p...) addresses are allowed.'
            )
        }

    if witness_version != 1:
        return {
            'success': False,
            'data': (
                f'Address "{address}" is a valid SegWit address but uses witness version '
                f'{witness_version}. Only witness version 1 (Taproot, tb1p...) is allowed.'
            )
        }

    if len(witness_program) != 64:
        return {
            'success': False,
            'data': (
                f'Address "{address}" has a witness program of length {len(witness_program)} hex chars '
                f'({len(witness_program) // 2} bytes). Taproot requires a 32-byte witness program.'
            )
        }

    if not address.lower().startswith('tb1p'):
        return {
            'success': False,
            'data': (
                f'Address "{address}" does not start with "tb1p". '
                f'Only Testnet Taproot (bech32m) addresses are allowed.'
            )
        }

    formatted_json = json.dumps(result, indent=4, separators=(',', ': '))

    return {
        'success': True,
        'data': (
            f'Address Validation Result:\n'
            f'Address: {address}\n'
            f'Valid: {is_valid}\n'
            f'SegWit: {is_witness}\n'
            f'Witness Version: {witness_version} (Taproot)\n'
            f'Witness Program: {witness_program}\n'
            f'ScriptPubKey: {result.get("scriptPubKey", "")}\n\n'
            f'Full validateaddress response:\n{formatted_json}\n'
        )
    }


##################################
# Address Balance and Transactions
##################################
def rpc_scan_address_utxos(
    host: str,
    port: int,
    auth_header: str,
    address: str
) -> Dict[str, Any]:
    try:
        resp = call_rpc(
            host=host,
            port=port,
            auth_header=auth_header,
            method='scantxoutset',
            params=['start', [f"addr({address})"]]
        )
    except Exception as e:
        return {'success': False, 'data': f'RPC call "scantxoutset" failed: {e}'}

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
                'data': f'Invalid amount value found in UTXO: {u.get("amount")}'
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
            auth_header=auth_header,
            method='getrawtransaction',
            params=[txid, True]  
        )
    except Exception as e:
        return {'success': False, 'data': f'RPC call "getrawtransaction" failed: {e}'}

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
    auth_header: str,
    address: str,
    limit: int = 5
) -> Dict[str, Any]:

    scan_res = rpc_scan_address_utxos(host, port, auth_header, address)
    if not scan_res['success']:
        return scan_res

    scan_data = scan_res['data']
    unspents = scan_data['unspents']
    total_balance = scan_data['total_balance']

    txids = list({u['txid'] for u in unspents})

    confirmed_txs: List[Dict[str, Any]] = []
    unconfirmed_txs: List[Dict[str, Any]] = []
    seen_txids = set()

    def fetch_tx(txid: str):
        if txid in seen_txids:
            return None
        seen_txids.add(txid)
        tx_res = rpc_get_transaction_details(host, port, auth_header, txid)
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
                    confirmed_txs.append({
                        'txid': txid,
                        'error': tx_res['data'],
                        'inputs': [],
                        'outputs': []
                    })
                    continue

                tx = tx_res['data']
                confirmations = tx.get('confirmations', 0)

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
                        'value': str(vout.get('value', '0'))
                    })

                tx_entry = {
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
                }

                if confirmations <= 0:
                    unconfirmed_txs.append(tx_entry)
                else:
                    confirmed_txs.append(tx_entry)

    confirmed_txs.sort(key=_normalize_tx_for_sorting, reverse=True)
    latest_confirmed = confirmed_txs[:limit]

    unconfirmed_txs.sort(key=_normalize_tx_for_sorting, reverse=True)
    latest_unconfirmed = unconfirmed_txs[:limit]

    return {
        'success': True,
        'data': {
            'address': address,
            'total_balance': total_balance,
            'utxo_count': len(unspents),
            'confirmed_transactions_found': len(confirmed_txs),
            'unconfirmed_transactions_found': len(unconfirmed_txs),
            'transactions': latest_confirmed,
            'unconfirmed_transactions': latest_unconfirmed,
            'raw_unspents': unspents
        }
    }
