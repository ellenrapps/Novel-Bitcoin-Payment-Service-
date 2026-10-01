# AGPL-3.0 License. Copyright © 2026 Ellen Red

import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import sys
import base64
import master_key
import rpc_calls
import cleaner


cleaner.setup_logging()


class Home():
    def __init__(self, root):
        self.root = root
        self.check_default_text = 'Enter Address'
        self.rpc_host = '127.0.0.1'
        self.rpc_port = 48332
        self.explorer_log_user = None 
        self.explorer_log_pass = None
        self.explorer_check_address_ent = None        
        self.rpc_username = None
        self.rpc_auth_header = None


        ##############
        # Main Widgets
        ##############
        root.title('Novel Bitcoin Payment Service – Testnet © 2026 Ellen Red')
        root.resizable(False, False)    
        root.config(bg='#414850')
        self.main_win_screen_width = root.winfo_screenwidth()
        self.main_win_screen_height =root.winfo_screenheight()
        self.main_win_window_width = 600 
        self.main_win_window_height = 450
        self.main_win_x = (self.main_win_screen_width // 2) - (self.main_win_window_width  // 2)
        self.main_win_y = (self.main_win_screen_height // 2) - (self.main_win_window_height // 2)
        root.geometry(f'{self.main_win_window_width}x{self.main_win_window_height}+{self.main_win_x}+{self.main_win_y}')
        
         # Main Logo/Buttons Frame
        self.main_logo_buttons_frame = tk.Frame(root, borderwidth=2, bg='#414850')
        self.main_logo_buttons_frame.pack(side='top')

        # Main Home Button
        self.main_home_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_home_click(), state='disabled', text= 'Home', bd=4, bg='#4f697f', width=3, font=('Segoe', 9, 'bold'))
        self.main_home_button.grid(row=1, column=2)

        # Main Explorer Button
        self.main_explorer_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_explorer_click(), text= 'Block Explorer', bd=4, bg='#4f697f', fg='white', width=10, font=('Segoe', 9, 'bold'))
        self.main_explorer_button.grid(row=1, column=3)
        
        # Main Address Button
        self.main_gen_address_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_gen_address_click(), text= 'Create Address + Key Pair', bd=4, bg='#4f697f', fg='white', width=20, font=('Segoe', 9, 'bold'))
        self.main_gen_address_button.grid(row=1, column=4)        

        # Main Send Button
        self.main_send_button = tk.Button(self.main_logo_buttons_frame, state='disable', text= 'Send Bitcoin', bd=4, bg='#4f697f', fg='white', width=9, font=('Segoe', 9, 'bold'))
        self.main_send_button.grid(row=1, column=6)
        
        # Main Reset Button
        self.main_reset_button = tk.Button(self.main_logo_buttons_frame, command=self.reset_app, state='normal', text= 'Reset', bd=4, bg='#4f697f', fg='#f7931a', width=4, font=('Segoe', 9, 'bold'))
        self.main_reset_button.grid(row=1, column=7)  


        ##############
        # Home Widgets
        ##############
        # Home Outer Frame
        self.home_outer_frame = tk.Frame(root, bg='#414850')
        self.home_outer_frame.pack()
       
        # Home Label1
        self.home_win_label = tk.Label(self.home_outer_frame, bg='#414850', fg='#00BFFF', text='Novel Bitcoin Payment Service\nis\nyour very own Bitcoin Payment Service.', font=('Segoe', 15, 'bold italic'))
        self.home_win_label.pack(side='top', pady=100)

        
        ##################
        # Explorer Widgets
        ##################
        # Explorer Outer Frame
        self.explorer_outer_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=0, bg='#414850')
        self.explorer_outer_frame.pack()
        self.explorer_outer_frame.pack_forget()

        # Explorer Label Frame 
        self.explorer_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_frame.pack(pady=10, side='top')
       
        # Explorer Label
        self.explorer_label = tk.Label(self.explorer_frame, bg='#414850', fg='white', text='B i t c o i n   E x p l o r e r', font=('Segoe', 10, 'bold'))
        self.explorer_label.pack(side='left') 
        
        # Explorer Login
        self.explorer_log_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_log_frame.pack(padx=3, fill=tk.X)
        self.explorer_log_user = tk.Entry(self.explorer_log_frame, justify="center", bd=2.5, width=23, font=('Arial', 9))
        self.explorer_log_user.insert(0, 'Enter Node Username')
        self.explorer_log_user.pack(side=tk.LEFT, padx=(6, 0), pady=(0, 1), fill=tk.BOTH)
        self.explorer_log_user.bind('<FocusIn>', self.user_focus_in)
        self.explorer_log_user.bind('<FocusOut>', self.user_focus_out)
        self.explorer_log_pass = tk.Entry(self.explorer_log_frame, justify="center", bd=2.5, width=23, font=('Arial', 9))
        self.explorer_log_pass.insert(0, 'Enter Node Password')
        self.explorer_log_pass.bind('<FocusIn>', self.pass_focus_in)
        self.explorer_log_pass.bind('<FocusOut>', self.pass_focus_out)
        self.explorer_log_pass.pack(side=tk.LEFT, pady=(0, 1), fill=tk.BOTH)
        self.explorer_log_connect_btn = tk.Button(self.explorer_log_frame, bd=2.5, width=30, command=self.connect_click, text='Connect to Local Bitcoin Node', bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_log_connect_btn.pack(side=tk.LEFT, padx=(0, 6), fill=tk.BOTH)
        
        # Explorer Check Balance, Transaction & Messages
        self.explorer_check_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_check_frame.pack(padx=3, fill=tk.X)
        self.explorer_check_address_ent = tk.Entry(self.explorer_check_frame, bd=2.5, justify="center", font=('Arial', 9), width=25)
        self.explorer_check_address_ent.insert(0, self.check_default_text)        
        self.explorer_check_address_ent.bind('<FocusIn>', self.bal_tx_focus_in)
        self.explorer_check_address_ent.bind('<FocusOut>', self.bal_tx_focus_out)
        self.explorer_check_address_ent.pack(side=tk.LEFT, padx=(6, 0), fill=tk.BOTH)
        self.explorer_check_address_ent.config(state='disabled')
        self.explorer_check_balance_tx_btn = tk.Button(self.explorer_check_frame, width=31, bd=2.5, state='disabled', text='Check Balance & Transaction Details', command=self.check_balance_clicked, bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_check_balance_tx_btn.pack(side=tk.LEFT, fill=tk.Y)
        self.explorer_check_messages_btn = tk.Button(self.explorer_check_frame, width=17, bd=2.5, state='disabled', text=' Check Messages', bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_check_messages_btn.pack(side=tk.LEFT, padx=(0,5), fill=tk.Y)

        # Explorer Sync
        self.explorer_sync_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_sync_frame.pack(padx=3, pady=4, fill=tk.X)
        self.explorer_check_sync_btn = tk.Button(self.explorer_sync_frame, width=20, command=self.check_sync_func, fg='#f7931a', bd=2.5, state='disabled', text='Check Node Sync Status', bg='#4f697f', font=('Arial', 9))
        self.explorer_check_sync_btn.pack(side=tk.LEFT, padx=(225,0), fill=tk.Y)
        
        # Explorer Textbox
        self.explorer_textbox_frame = tk.Frame(self.explorer_outer_frame)
        self.explorer_textbox_frame.pack() 
        self.explorer_textbox = scrolledtext.ScrolledText(self.explorer_textbox_frame, bg='#414850', fg="white", font=("Segoe", 11), wrap=tk.WORD, width=68, height=11)
        self.explorer_textbox.tag_configure('center_tag', justify='center')
        self.explorer_textbox.tag_add('center_tag', '1.0', '1.end')
        self.explorer_textbox.pack(pady=(8), padx=(8), anchor='w')
        self.nov_logo = tk.PhotoImage(file='nov_logo.png')
        self.explorer_textbox.image_create('end', image=self.nov_logo)
        self.explorer_textbox.image = self.nov_logo


        #################
        # Address Widgets
        #################
        # Address Outer Frame
        self.create_address_outer_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='#414850')
        self.create_address_outer_frame.pack(pady=40)
        self.create_address_outer_frame.pack_forget()

        # Address Label Frame
        self.address_win_label_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.address_win_label_frame.pack(side='top')

        # Address Label
        self.address_win_label = tk.Label(self.address_win_label_frame, bg='#414850', fg='white', text='Create Bitcoin Address + Public Key + Private Key', font=('Segoe', 11, 'bold'))
        self.address_win_label.pack(side='left', pady=30)

        # Address Notice Frame
        self.address_win_notice_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.address_win_notice_frame.pack(side='top', pady=3)

        # Address Notice
        self.address_win_notice = tk.Label(self.address_win_notice_frame, bg='#414850', fg='white', text='To create Bitcoin Address + Public Key + Private Key:\n1. Click Generate.\n2. Scroll down to view keys.\n3. Copy data by highlighting text and pressing Ctrl+C. Save it to a secure digital location.\n Data will self-destruct after 3 seconds. If you run out of time, click Generate button again.', font=('Segoe', 9))
        self.address_win_notice.pack(side='left')

        # Address Label + Button Frame
        self.create_address_label_button_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_label_button_frame.pack()

        # Address Text Frame
        self.create_address_text_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_text_frame.pack()

        # Address Copy Clear Frame
        self.create_address_clear_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_clear_frame.pack()

        # Address Button
        self.create_address_key_button = tk.Button(self.create_address_label_button_frame, text='G e n e r a t e', borderwidth=3, fg='white', bg='#4f697f', height=1, width=10, font=('Segoe', 10), command=lambda: [self.create_address_show_delete_keyadd(), self.address_clear_button_enable()])
        self.create_address_key_button.bind('<Enter>', lambda event, h=self.create_address_key_button: h.configure())
        self.create_address_key_button.bind('<Leave>', lambda event, h=self.create_address_key_button: h.configure())
        self.create_address_key_button.pack(pady=10)
        
        # Address Text
        self.create_address_key_text = tk.Text(self.create_address_text_frame, bg='#e2dada', height=4, width=50, fg='black', font=('Segoe', 8))
        self.create_address_key_text = scrolledtext.ScrolledText(self.create_address_text_frame, wrap=tk.WORD, height=4, width=70)
        self.create_address_key_text.bind('<Button-1>', self.create_address_disable_click_master)
        self.create_address_key_text.bind('<Up>', self.adress_move_up)
        self.create_address_key_text.bind('<Down>', self.adress_move_down)
        self.create_address_key_text.pack(pady=(0, 10))
        
        # Address Clear Button
        self.create_address_clear_button = tk.Button(self.create_address_clear_frame, state='disabled', text= "C l e a r",  borderwidth=3, fg='white', bg='#4f697f', height=1, width=7, font=('Segoe', 10), command= lambda: [self.clear_address_text(), self.address_clear_button_disable()])                           
        self.create_address_clear_button.bind('<Enter>', lambda event, h=self.create_address_clear_button: h.configure())
        self.create_address_clear_button.bind('<Leave>', lambda event, h=self.create_address_clear_button: h.configure())
        self.create_address_clear_button.grid(row=0, column=1,padx=20, pady=(0, 20))
        
        
    ################
    # Home Functions
    ################
    def main_home_click(self):
        self.home_outer_frame.pack_forget()
        self.explorer_outer_frame.pack_forget()
        self.create_address_outer_frame.pack_forget()
        self.main_explorer_button.config(state='normal')
        self.main_gen_address_button.config(state='normal')
        self.main_home_button.config(state='disabled')
        self.home_outer_frame.pack()
        self.create_address_key_text.delete('1.0', 'end')


    def main_explorer_click(self):
        self.home_outer_frame.pack_forget()
        self.main_explorer_button.config(state='disabled')
        self.main_gen_address_button.config(state='disabled')        
        self.explorer_outer_frame.pack()
        self.main_home_button.config(state='normal')
        self.main_home_button.config(fg='#f7931a')
        self.display_result(text=
            'False Positive and False Negative Alert\n\n'
            '💡 Steps to check address balance and transaction details to prevent false positives and false negatives:\n\n'
            '1. In bitcoin.conf, add this: assumevalid=0. (This forces the node to verify every signature from the genesis block forward.)\n'
            '2. Start bitcoind in the Linux terminal.\n'
            '3. Ensure your computer is connected to the internet.\n'
            '4. Log in with your node username and password. Use rpcauth.\n'
            '5. Click “Check Node Sync Status”.\n'
            '6. Enter the Bitcoin Testnet Taproot (Bech32m) address and click “Check Balance & Transaction Details”.'
            )


    def main_gen_address_click(self):
        self.home_outer_frame.pack_forget()
        self.main_explorer_button.config(state='disabled')
        self.main_gen_address_button.config(state='disabled')        
        self.create_address_outer_frame.pack()
        self.main_home_button.config(state='normal')
        self.main_home_button.config(fg='#f7931a')
    

    ####################
    # Explorer Functions
    ####################
    def display_result(self, text):
        self.explorer_textbox.config(state='normal')
        self.explorer_textbox.delete(1.0, tk.END)
        self.nov_logo = tk.PhotoImage(file='nov_logo.png')
        self.explorer_textbox.image_create('end', image=self.nov_logo)
        self.explorer_textbox.image = self.nov_logo
        self.explorer_textbox.insert(tk.END, text)
        self.explorer_textbox.see('1.0')  


    def clear_result(self):
        self.explorer_textbox.delete(1.0, tk.END)
        self.explorer_textbox.config(state='normal')

        
    def user_focus_in(self, event):
        if self.explorer_log_user.get() == 'Enter Node Username':
            self.explorer_log_user.delete(0, 'end') 
            self.explorer_log_user.insert(0, '') 
            self.explorer_log_user.config(show='*')


    def user_focus_out(self, event):
        if self.explorer_log_user.get() == '':
            self.explorer_log_user.insert(0, 'Enter Node Username')


    def pass_focus_in(self, event):
        if self.explorer_log_pass.get() == 'Enter Node Password':
            self.explorer_log_pass.delete(0, 'end')  
            self.explorer_log_pass.insert(0, '')
            self.explorer_log_pass.config(show='*')


    def pass_focus_out(self, event):
        if self.explorer_log_pass.get() == '':
            self.explorer_log_pass.insert(0, 'Enter Node Password')
            self.explorer_log_pass.config(show='')

   
    def bal_tx_focus_in(self, event):
        entry = event.widget 
        if entry.get() == self.check_default_text:
            entry.delete(0, tk.END)


    def bal_tx_focus_out(self, event):
        entry = event.widget  
        if not entry.get():
            entry.insert(0, self.check_default_text)

    
    def connect_click(self):
        username = self.explorer_log_user.get().strip()
        cleaner.logging.info(f'username={username}')
        password = self.explorer_log_pass.get().strip()
        cleaner.logging.info(f'password={password}')
        credentials = f'{username}:{password}'
        cleaner.logging.info(f'credentials={credentials}')
        encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        cleaner.logging.info(f'encoded={encoded}')        
        auth_header = f'Basic {encoded}'
        cleaner.logging.info(f'auth_header={encoded}')

        self.rpc_username = username
        self.rpc_auth_header = auth_header
        del password
        self.root.update_idletasks()

        result_blockchain_info = rpc_calls.get_blockchain_info_v1(
            self.rpc_host,
            self.rpc_port,
            self.rpc_auth_header
        )

        if result_blockchain_info['success']:
            self.display_result(result_blockchain_info['data'])
            self.explorer_log_user.delete(0, tk.END)
            self.explorer_log_pass.delete(0, tk.END)
            self.explorer_log_user.config(state='disabled')
            self.explorer_log_pass.config(state='disabled')
            self.explorer_log_connect_btn.config(state='disabled', text='Connected to Local Bitcoin Node')
            self.explorer_check_address_ent.config(state='normal')
            self.explorer_check_balance_tx_btn.config(state='normal')
            self.explorer_check_sync_btn.config(state='normal')
            
        else:
            self.explorer_textbox.delete(1.0, tk.END)            
            self.explorer_textbox.config(state='normal')
            self.explorer_log_user.delete(0, tk.END)
            self.explorer_log_pass.delete(0, tk.END)
            self.explorer_textbox.insert(tk.END, 'Something is wrong. Enter correct Bitcoin Node username and password. Check Bitcoin Node connection.') 
            self.explorer_log_user.config(state='normal')
            self.explorer_log_pass.config(state='normal')
            self.explorer_log_connect_btn.config(state='normal', text='Connect to Local Bitcoin Node', fg='#f7931a')            
            self.root.after(15000, self.clear_result)   
    
    
    def check_sync_func(self):
        try:
            self.general_sync_helper()
            self.explorer_check_address_ent.delete(0, tk.END)
            self.explorer_check_address_ent.insert(0, self.check_default_text)
            self.explorer_check_address_ent.master.focus_set()

        except Exception as e:
            error_msg = f'❗ Could not determine sync status due to an error: {e}'
            self.handle_sync_error(error_msg)
            self.explorer_check_address_ent.delete(0, tk.END)
            self.explorer_check_address_ent.insert(0, self.check_default_text)
            self.explorer_check_address_ent.master.focus_set()      

        
    def general_sync_helper(self):
        result_blockchain_info = rpc_calls.get_blockchain_info_v2(
            self.rpc_host,
            self.rpc_port,
            self.rpc_auth_header
        )

        if not result_blockchain_info.get("success"):
            self.display_result(f'❌ Check Bitcoin Node connection.')
            self.not_sync_helper()
            return

        sync_details = result_blockchain_info['sync_details']
        is_synced = result_blockchain_info['is_synced']
        initial_download = sync_details.get('initialblockdownload', False)

        if is_synced:
            self.display_result('✅ Node is fully synchronized.')
            self.sync_helper()

            address = self.explorer_check_address_ent.get().strip()
            cleaner.logging.info(f'address={address}')

            self.explorer_check_address_ent.delete(0, 'end')
            self.explorer_check_address_ent.insert(0, self.check_default_text)
            self.explorer_check_address_ent.config(bg='light gray')
            self.explorer_check_balance_tx_btn.config(state='normal')
            return

        if initial_download:
            self.display_result(
                'Try again later. ❎ The node is not fully synchronized.\n\n'
                'Syncing Time Calculation:\n'
                '✅ Syncing a Bitcoin Testnet node from scratch takes approximately 1–2 hours\n\n'
                '✅ Re‑synchronization takes a few minutes or longer, depending on the conditions.'
            )
            self.sync_helper()

    
    def not_sync_helper(self):
        self.explorer_textbox.delete(1.0, tk.END)            
        self.explorer_textbox.config(state='normal')
        self.explorer_log_user.delete(0, tk.END)
        self.explorer_log_pass.delete(0, tk.END)
        self.explorer_log_user.config(state='normal')
        self.explorer_log_pass.config(state='normal')
        self.explorer_log_connect_btn.config(state='normal', text='Connect to Local Bitcoin Node', fg='#f7931a')            
            
   
    def sync_helper(self):
        self.explorer_log_user.delete(0, tk.END)
        self.explorer_log_pass.delete(0, tk.END)
        self.explorer_log_user.config(state='disabled')
        self.explorer_log_pass.config(state='disabled')
        self.explorer_log_connect_btn.config(state='disabled', text='Connected to Local Bitcoin Node')


    def handle_sync_error(self, error_msg: str):
        self.display_result(error_msg)
        self.not_sync_helper()
    
        
        ##############################
        # Check Balance & Transactions
        ##############################
    def check_bal_tx_thread(self, address: str) -> None:
        try:
            result_balance_transactions = rpc_calls.fetch_latest_balance_transactions(
                self.rpc_host,
                self.rpc_port,
                self.rpc_auth_header,
                address,
                limit=5
            )

            if result_balance_transactions['success']:
                data = result_balance_transactions['data']

                full_output = ''

                summary = (
                    f'Address: {data['address']}\n'
                    f'Total Balance: {data['total_balance']} tBTC\n'
                    f'Confirmed Transactions Found: {data['confirmed_transactions_found']}\n'
                    f'Unconfirmed Transactions Found: {data['unconfirmed_transactions_found']}\n'
                    f'Latest confirmed transactions are listed below: {len(data['transactions'])}\n'
                )
                full_output += summary + '\n'

                for i, tx in enumerate(data['transactions'], start=1):
                    tx_info = (
                        f'--- Transaction #{i} ---\n'
                        f'TXID: {tx["txid"]}\n'
                        f'Confirmations: {tx.get('confirmations')}\n'
                        f'Time: {tx.get("time")}\n'
                        f'Inputs ({len(tx["inputs"])}):\n'
                    )
                    for j, vin in enumerate(tx['inputs']):
                        script_sig_preview = vin['scriptSig'][:64] + "..." if len(vin['scriptSig']) > 64 else vin['scriptSig']
                        tx_info += (
                            f'  [{j}] txid={vin["txid"]}, vout={vin["vout"]}, '
                            f'scriptSig_hex={script_sig_preview}\n'
                        )

                    tx_info += f'Outputs ({len(tx["outputs"])}):\n'
                    for j, vout in enumerate(tx['outputs']):
                        tx_info += (
                            f'  [{j}] value={vout["value"]} tBTC\n'
                        )

                    full_output += tx_info + '\n'

                if data['unconfirmed_transactions']:
                    full_output += (
                        f'Latest unconfirmed transactions are listed below: '
                        f'{len(data["unconfirmed_transactions"])}\n\n'
                    )
                    for i, tx in enumerate(data['unconfirmed_transactions'], start=1):
                        tx_info = (
                            f'--- Unconfirmed Transaction #{i} ---\n'
                            f'TXID: {tx["txid"]}\n'
                            f'Confirmations: {tx.get("confirmations")}\n'
                            f'Time: {tx.get("time")}\n'
                            f'Inputs ({len(tx["inputs"])}):\n'
                        )
                        for j, vin in enumerate(tx['inputs']):
                            script_sig_preview = vin['scriptSig'][:64] + "..." if len(vin['scriptSig']) > 64 else vin['scriptSig']
                            tx_info += (
                                f'  [{j}] txid={vin["txid"]}, vout={vin["vout"]}, '
                                f'scriptSig_hex={script_sig_preview}\n'
                            )

                        tx_info += f'Outputs ({len(tx["outputs"])}):\n'
                        for j, vout in enumerate(tx['outputs']):
                            tx_info += (
                                f'  [{j}] value={vout["value"]} tBTC\n'
                            )

                        full_output += tx_info + '\n'
                else:
                    full_output += 'No unconfirmed transactions found.\n\n'

                self.root.after(0, self.display_result, full_output)

            else:
                error_msg = result_balance_transactions['data'] or 'Unknown error'
                self.root.after(0, self.display_result, f'\nFailed to scan address: {error_msg}. Please try again.')

        except Exception as e:
            gen_error_msg = f'Error: {e}'
            self.root.after(0, self.display_result, gen_error_msg)

        finally:
            self.root.after(0, lambda: self.explorer_check_balance_tx_btn.config(state='normal'))
            self.root.after(0, lambda: self.explorer_check_address_ent.config(bg='white'))
            
    
    def check_balance_clicked(self) -> None:
        self.explorer_textbox.delete(1.0, tk.END)
        address = self.explorer_check_address_ent.get().strip()
        cleaner.logging.info(f'address={address}')
        if not address:
            self.display_result('Please enter an address to check.')
            return

        self.explorer_check_balance_tx_btn.config(state='disabled')
        self.explorer_check_address_ent.config(bg='light gray')

        threading.Thread(
            target=self.validate_and_check_balance_tx,
            args=(address,),
            daemon=True
            ).start()    

    
    def validate_and_check_balance_tx(self, address: str) -> None:
        try:
            val_result = rpc_calls.validate_address(
                self.rpc_host,
                self.rpc_port,
                self.rpc_auth_header,
                address
            )

            if not val_result['success']:
                self.root.after(0, self.display_result, f'\nAddress validation failed: {val_result["data"]} Enter a valid address.')
                self.root.after(0, lambda: self.explorer_check_balance_tx_btn.config(state='normal'))
                self.root.after(0, lambda: self.explorer_check_address_ent.config(bg='white'))
                return

            result_blockchain_info = rpc_calls.get_blockchain_info_v2(
                self.rpc_host,
                self.rpc_port,
                self.rpc_auth_header
            )
            
            is_synced = result_blockchain_info.get('is_synced', False)
            initial_download = result_blockchain_info.get('sync_details', {}).get('initialblockdownload', False)

            if is_synced and not initial_download:
                self.display_result('Processing ...')
                thread = threading.Thread(target=self.check_bal_tx_thread, args=(address,), daemon=True)
                thread.start()
                self.explorer_check_address_ent.insert(0, self.check_default_text)
            else:
                if initial_download:
                    msg = (
                        'Try again later. ❎ The node is not fully synchronized.\n\n'
                        'Syncing Time Calculation:\n'
                        '✅ Syncing a Bitcoin Testnet node from scratch takes approximately 1–2 hours\n\n'
                        '✅ Re‑synchronization takes a few minutes or longer, depending on the conditions.'
                    )
                    
                else:
                    msg = '❗ Could not determine sync status or node is not fully synchronized.'
                    
                self.root.after(0, self.display_result, msg)
                self.root.after(0, lambda: self.explorer_check_balance_tx_btn.config(state='normal'))
                self.root.after(0, lambda: self.explorer_check_address_ent.config(bg='white'))
            
            self.explorer_check_address_ent.delete(0, tk.END)
            self.explorer_check_address_ent.insert(0, self.check_default_text)
            self.explorer_check_address_ent.master.focus_set()

        except Exception as e:
            gen_error_msg = f'❗ Error during address validation before checking balance and tx: {e}'
            self.root.after(0, self.display_result, gen_error_msg)
            self.root.after(0, lambda: self.explorer_check_balance_tx_btn.config(state='normal'))
            self.root.after(0, lambda: self.explorer_check_address_ent.config(bg='white'))
            self.handle_sync_error(gen_error_msg)


    ###################
    # Address Functions
    ###################  
    def create_address_disable_click_master(self, event):
        if not self.create_address_key_text.get('1.0', 'end-1c'): 
            return 'break'    


    def create_address_key_address(self): 
        self.clear_address_text()
        try:
            addr, tweaked_privkey, tweaked_pubkey = master_key.iden()
            cleaner.logging.info(f'addr={addr}, tweaked_privkey={tweaked_privkey}, tweaked_pubkey={tweaked_pubkey}')
            
            self.content_key_address = f'\nBitcoin Address: {addr} \n\n\nPrivate Key: {tweaked_privkey}\n\n\nPublic Key: {tweaked_pubkey}' 
            cleaner.logging.info(f'self.content_key_address={self.content_key_address}')

            return self.content_key_address
        
        except Exception as e:
            error_message = f'Error occurred: {str(e)}'
            self.create_address_key_text.delete('1.0','end')
            self.create_address_key_text.insert(tk.END, error_message)
        

    def create_address_key_dis_but(self, button, delay):
        self.create_address_key_button.config(state='disabled')
        self.root.after(delay*1500, self.create_address_key_enab_but)


    def create_address_key_enab_but(self):
        self.create_address_key_button.config(state='normal')


    def create_address_delete_keyadd(self):
        self.create_address_key_text.delete('1.0','end')


    def create_address_show_delete_keyadd(self):
        self.key_add = self.create_address_key_address()
        self.disable_button = self.create_address_key_dis_but(self.create_address_key_button, 3)
        self.create_address_key_text.tag_configure('center', justify='center') 
        self.create_address_key_text.insert(tk.INSERT, self.key_add)
        self.create_address_key_text.tag_add('center', '1.0', 'end')
        self.create_address_key_text.after(3000, self.create_address_delete_keyadd)    
        self.create_address_key_button.update()
        

    def adress_move_up(self, event):
        self.create_address_key_text.mark_set('insert', 'insert-1lines') 
        self.create_address_key_text.see('insert') 
        return 'break'


    def adress_move_down(self, event):
        self.create_address_key_text.mark_set('insert', 'insert+1lines') 
        self.create_address_key_text.see('insert') 
        return 'break'  
    

    def address_clear_button_enable(self):
        self.create_address_clear_button.config(state='normal')


    def address_clear_button_disable(self):
        self.create_address_clear_button.config(state='disabled')


    def clear_address_text(self):
        self.create_address_key_text.delete('1.0', 'end')  
   
        
    ################
    # Reset Function
    ################
    def reset_app(self):
            os.execv(sys.executable, [sys.executable] + sys.argv)

    
    ##############
    # Data Removal
    ##############
    def on_close(self):
        self.explorer_log_user = None 
        self.explorer_log_pass = None
        self.explorer_check_address_ent = None        
        self.rpc_username = None
        self.rpc_auth_header = None
        self.root.destroy()
        

#################
# Run Application
#################
main_root = tk.Tk()
home_instance = Home(main_root)
main_root.mainloop()
