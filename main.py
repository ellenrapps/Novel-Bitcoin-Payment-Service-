# AGPL-3.0 License. Copyright © 2026 Ellen Red

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import base64
import master_key
import rpc_calls


class Home():
    def __init__(self, root):
        self.root = root
        self.wallet_name = 'watch_only_wallet'
        self.add_default_text = 'Enter Testnet Taproot Public Key'
        self.check_default_text = 'Enter Testnet Taproot Address' 
        self.rpc_host = '127.0.0.1'
        self.rpc_port = 48332
        self.rpc_username = None
        self.rpc_auth_header = None
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)       

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
        
        #Main Logo/Buttons Frame
        self.main_logo_buttons_frame = tk.Frame(root, borderwidth=2, bg='#414850')
        self.main_logo_buttons_frame.pack(side='top')

        #Main Logo
        self.main_logo = tk.PhotoImage(file='nov_logo.png') 
        self.main_logo_label = tk.Label(self.main_logo_buttons_frame, borderwidth=0, highlightthickness=0, image=self.main_logo)
        self.main_logo_label.grid(row=0, column=0, padx=(1), rowspan=20)

        #Main Home Button
        self.main_home_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_home_click(), state='disabled', text= 'Home', bd=2.5, bg='#4f697f', width=3, font=('Segoe', 9, 'bold'))
        self.main_home_button.grid(row=1, column=2)

        # Main Explorer Button
        self.main_explorer_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_explorer_click(), text= 'Block Explorer', bd=2.5, bg='#4f697f', fg='white', width=10, font=('Segoe', 9, 'bold'))
        self.main_explorer_button.grid(row=1, column=3)
        
        # Main Address Button
        self.main_gen_address_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_gen_address_click(), text= 'Create Address + Key Pair', bd=2.5, bg='#4f697f', fg='white', width=20, font=('Segoe', 9, 'bold'))
        self.main_gen_address_button.grid(row=1, column=4)        

        # Main Send Button
        self.main_send_button = tk.Button(self.main_logo_buttons_frame, state='disabled', text= 'Send Bitcoin', bd=2.5, bg='#4f697f', fg='white', width=9, font=('Segoe', 9, 'bold'))
        self.main_send_button.grid(row=1, column=6)

        # Main Privacy Button
        self.main_privacy_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_privacy_click(), text= 'FAQ', bd=2.5, bg='#4f697f', fg='white', width=4, font=('Segoe', 9, 'bold'))
        self.main_privacy_button.grid(row=1, column=7) 

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
        self.explorer_frame.pack(side='top')
       
        # Explorer Label
        self.explorer_label = tk.Label(self.explorer_frame, bg='#414850', fg='white', text='B i t c o i n   E x p l o r e r', font=('Segoe', 10, 'bold'))
        self.explorer_label.pack(side='left') 
        
        # Explorer Login
        self.explorer_log_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_log_frame.pack(pady=1, padx=3, fill=tk.X)
        self.explorer_log_user = tk.Entry(self.explorer_log_frame, width=14, font=('Arial', 9))
        self.explorer_log_user.insert(0, 'Enter Node User')
        self.explorer_log_user.pack(side=tk.LEFT, padx=(6, 1), fill=tk.BOTH)
        self.explorer_log_user.bind('<FocusIn>', self.user_focus_in)
        self.explorer_log_user.bind('<FocusOut>', self.user_focus_out)
        self.explorer_log_pass = tk.Entry(self.explorer_log_frame, width=14, font=('Arial', 9))
        self.explorer_log_pass.insert(0, 'Enter Node PWD')
        self.explorer_log_pass.bind('<FocusIn>', self.pass_focus_in)
        self.explorer_log_pass.bind('<FocusOut>', self.pass_focus_out)
        self.explorer_log_pass.pack(side=tk.LEFT, padx=(0, 2), fill=tk.BOTH)
        self.explorer_log_connect_btn = tk.Button(self.explorer_log_frame, width=27, command=self.connect_click, text='Connect to Local Bitcoin Node', bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_log_connect_btn.pack(side=tk.LEFT, padx=(0, 1), fill=tk.BOTH)
        self.explorer_log_wallet_btn = tk.Button(self.explorer_log_frame, width=19, state='disable', command=self.load_wallet_click, text='Load Watch-Only Wallet', bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_log_wallet_btn.pack(side=tk.LEFT, padx=(0, 6), fill=tk.BOTH)
        
        # Explorer Add Public Key
        self.explorer_add_pubkey_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_add_pubkey_frame.pack(padx=3, fill=tk.X)
        self.explorer_add_pubkey_ent = tk.Entry(self.explorer_add_pubkey_frame, justify="center", font=('Arial', 9), width=68)
        self.explorer_add_pubkey_ent.insert(0, self.add_default_text)
        self.explorer_add_pubkey_ent.pack(side=tk.LEFT, padx=(6, 1), pady=(0, 1), fill=tk.BOTH)
        self.explorer_add_pubkey_ent.config(state='disabled')
        self.explorer_add_pubkey_ent.bind("<FocusIn>", self.on_entry_focus)
        self.explorer_add_pubkey_btn = tk.Button(self.explorer_add_pubkey_frame, state='disabled', text='Add Public Key', command=self.add_pubkey_clicked, bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_add_pubkey_btn.pack(side=tk.LEFT, padx=(0, 6), fill=tk.Y)
        
        # Explorer Check Address
        self.explorer_check_address_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_check_address_frame.pack(padx=3, fill=tk.X)
        self.explorer_check_address_ent = tk.Entry(self.explorer_check_address_frame, justify="center", font=('Arial', 9), width=68)
        self.explorer_check_address_ent.insert(0, self.check_default_text)        
        self.explorer_check_address_ent.pack(side=tk.LEFT, padx=(6, 1), pady=(0, 1), fill=tk.BOTH)
        self.explorer_check_address_ent.config(state='disabled')
        self.explorer_check_address_ent.bind("<FocusIn>", self.on_entry_focus)
        self.explorer_check_address_btn = tk.Button(self.explorer_check_address_frame, state='disabled', text='Check Address', command=self.scan_address_clicked, bg='#4f697f', fg='#f7931a', font=('Arial', 9))
        self.explorer_check_address_btn.pack(side=tk.LEFT, padx=(0, 6), fill=tk.Y)
        
        # Explorer Textbox
        self.results_label = tk.Label(self.explorer_outer_frame, text="Results/Notifications", anchor="w", bg='#414850', fg='white', font=("Arial", 9))
        self.results_label.pack(fill='x', padx=6, pady=7)
        self.explorer_textbox_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_textbox_frame.pack() 
        self.explorer_textbox = tk.Text(self.explorer_textbox_frame, font=('Segoe', 11))
        self.explorer_textbox = scrolledtext.ScrolledText(self.explorer_textbox_frame, wrap=tk.WORD, height=14)
        self.explorer_textbox.tag_configure('center_tag', justify='center')
        self.explorer_textbox.tag_add('center_tag', '1.0', '1.end')
        self.explorer_textbox.bind('<Up>', self.privacy_move_up)
        self.explorer_textbox.bind('<Down>', self.privacy_move_down)
        self.explorer_textbox.pack(pady=(4), padx=10, anchor='w')

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
        self.address_win_label.pack(side='left', pady=10)

        # Address Notice Frame
        self.address_win_notice_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.address_win_notice_frame.pack(side='top', pady=3)

        # Address Notice
        self.address_win_notice = tk.Label(self.address_win_notice_frame, bg='#414850', fg='white', text='To create Bitcoin Address + Public Key + Private Key:\n1. Press Generate.\n2. Scroll down to view Public Key and Private Key.\n3. Write down the Address and Key Pair (Public and Private keys) and keep it in a safe place\nor copy it to a safe digital storage.\nAddress and Key Pair texts will self-distruct after 10 minutes.\nIn case you run out of time, should you choose the writing option,\ngenerate another Andress + Key Pair by repeating the process.', font=('Segoe', 8))
        self.address_win_notice.pack(side='left')

        # Address Label + Button Frame
        self.create_address_label_button_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_label_button_frame.pack()

        # Address Text Frame
        self.create_address_text_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_text_frame.pack()

        # Address Copy Clear Frame
        self.create_address_copy_clear_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_copy_clear_frame.pack()

        # Address Button
        self.create_address_key_button = tk.Button(self.create_address_label_button_frame, text='G e n e r a t e', borderwidth=3, fg='white', bg='#4f697f', height=1, width=10, font=('Segoe', 10), command=lambda: [self.create_address_show_delete_keyadd(), self.address_copy_button_enable(), self.address_clear_button_enable()])
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
        
        # Address Copy Button
        self.create_address_copy_button = tk.Button(self.create_address_copy_clear_frame, state='disabled', text= 'C o p y',  borderwidth=3, fg='white', bg='#4f697f', height=1, width=7, font=('Segoe', 10), command= lambda: self.is_address_copy_clicked())                           
        self.create_address_copy_button.bind('<Enter>', lambda event, h=self.create_address_copy_button: h.configure())
        self.create_address_copy_button.bind('<Leave>', lambda event, h=self.create_address_copy_button: h.configure())
        self.create_address_copy_button.grid(row=0, column=0,pady=(0, 20))
      
        # Address Clear Button
        self.create_address_clear_button = tk.Button(self.create_address_copy_clear_frame, state='disabled', text= "C l e a r",  borderwidth=3, fg='white', bg='#4f697f', height=1, width=7, font=('Segoe', 10), command= lambda: [self.clear_address_text(), self.address_copy_button_disable(), self.address_clear_button_disable()])                           
        self.create_address_clear_button.bind('<Enter>', lambda event, h=self.create_address_clear_button: h.configure())
        self.create_address_clear_button.bind('<Leave>', lambda event, h=self.create_address_clear_button: h.configure())
        self.create_address_clear_button.grid(row=0, column=1,padx=20, pady=(0, 20))
                
        #######################
        # Privacy-Terms Widgets
        #######################
        # Privacy Outer Frame
        self.privacy_outer_frame = tk.Frame(root, bg='#414850')
        self.privacy_outer_frame.pack()
        self.privacy_outer_frame.pack_forget()

        # Privacy Inner Frame
        self.privacy_inner_frame = tk.Frame(self.privacy_outer_frame, bg='#414850')
        self.privacy_inner_frame.pack()

        # Privacy Textbox
        self.privacy_textbox = tk.Text(self.privacy_inner_frame, height=23, font=('Segoe', 11))
        self.privacy_textbox = scrolledtext.ScrolledText(self.privacy_inner_frame, wrap=tk.WORD, height=23)
        self.privacy_textbox.insert(tk.END, 'P R I V A C Y / T E R M S / F A Q\n\nPRIVACY POLICY\nNovel Bitcoin Payment Service respects your privacy. It doesn’t access, collect, or transmit any information (data that could be used to identify a person). As a user of this service, you have full control over your bitcoin address and private key. What this means is that you are fully responsible for securing your bitcoin address and private key and you have full control over your bitcoin funds.\n\nTERMS OF SERVICE\nBy using this Novel Bitcoin Payment Service, you agree that you will not use this service to commit illegal activities within and outside your geographical location.\n\nFREQUENTLY ASKED QUESTION: What is Novel Bitcoin Payment Service?\nBitcoin Payment Service aims to be your very own payment service, attaining the goal of Peer-to-Peer Electronic Cash System as envisioned by Satoshi Nakamoto.\n\nIn the Bitcoin white paper written by Nakamoto, Peer-to-Peer Electronic Cash System is described as allowing online payments to be sent directly from one party to another without going through a financial institution.\n\nThis payment service does not aim to be a financial institution. Rather, this payment service aims to be a means for ordinary folks to send bitcoin, whether as payment or donation, to one another, that is, without an intermediary financial institution.\n\nSpecifically, this payment service will allow everyday users to:\n1. Create bitcoin address + key\n2. Create smart contracts\n3. Check bitcoin address balance using an in-built blockchain explorer\n4. Receive bitcoin\n5. Send bitcoin\n6. Communicate regarding the received or sent satoshis within the Bitcoin blockchain\n\nUnknown to many, Nakamoto built within the Bitcoin infrastracture a means for senders and receivers to communicate with each other. Nakamoto also built within the Bitcoin infrastracture smart contracts. These in-built communication system and smart contracts within the Bitcoin blockchain will be put into use in this novel Bitcoin Payment System.')  
        self.privacy_textbox.tag_configure('center_tag', justify='center')
        self.privacy_textbox.tag_add('center_tag', '1.0', '1.end')
        self.privacy_textbox.bind('<Up>', self.privacy_move_up)
        self.privacy_textbox.bind('<Down>', self.privacy_move_down)
        self.privacy_textbox.pack(pady=(25, 25), padx=10, anchor='w')       
    
    ################
    # Home Functions
    ################
    def main_home_click(self):
        self.explorer_outer_frame.pack_forget()
        self.create_address_outer_frame.pack_forget()
        self.privacy_outer_frame.pack_forget()
        self.home_outer_frame.pack_forget()
        self.main_explorer_button.config(state='normal')
        self.main_gen_address_button.config(state='normal')
        self.main_privacy_button.config(state='normal')
        self.main_home_button.config(state='disabled')
        self.home_outer_frame.pack()
        self.create_address_key_text.delete('1.0', 'end')


    def main_explorer_click(self):
        self.home_outer_frame.pack_forget()
        self.main_gen_address_button.config(state='disabled')
        self.main_explorer_button.config(state='disabled')
        self.main_privacy_button.config(state='disabled')
        self.explorer_outer_frame.pack()
        self.main_home_button.config(state='normal')
        self.main_home_button.config(fg='#f7931a')


    def main_gen_address_click(self):
        self.home_outer_frame.pack_forget()
        self.main_gen_address_button.config(state='disabled')
        self.main_explorer_button.config(state='disabled')
        self.main_privacy_button.config(state='disabled')
        self.create_address_outer_frame.pack()
        self.main_home_button.config(state='normal')
        self.main_home_button.config(fg='#f7931a')
    

    def main_privacy_click(self):
        self.home_outer_frame.pack_forget()
        self.main_privacy_button.config(state='disabled')
        self.main_gen_address_button.config(state='disabled')
        self.main_explorer_button.config(state='disabled')
        self.privacy_outer_frame.pack()
        self.main_home_button.config(state='normal')
        self.main_home_button.config(fg='#f7931a')   

    ####################
    # Explorer Functions
    ####################
    def copy_text(self):
        if self.explorer_textbox.tag_ranges('sel'):
            selected = self.explorer_textbox.get('sel.first', 'sel.last')
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.copy_text_showinfo = f'Text Copied'
            self.display_result(self.copy_text_showinfo)
        else:
            all_text = self.explorer_textbox.get('1.0', tk.END).rstrip('\n')
            if all_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(all_text)                
            else:
                self.copy_text_showwarning = f'Nothing to copy. Textbox is empty.'
                self.display_result(self.copy_text_showwarning)
        
        copy_text_btn_frame = tk.Frame(
            self.root,
            bg='#e0f7fa',          
            relief='raised',
            bd=2.5
        )

        copy_icon_label = tk.Label(
            copy_text_btn_frame,
            text='📋',
            font=('Arial', 10),
            fg='#0277bd',  
            bg='#e0f7fa'
        )
        copy_icon_label.pack(side='left')
        
        copy_text_label = tk.Label(
            copy_text_btn_frame,
            text='Copy',
            font=('Arial', 9, 'bold'),
            fg='#0d47a1',         
        )

        copy_text_label.pack(side='left')
        copy_text_btn_frame.bind('<Button-1>', lambda e: self.copy_text())
        copy_text_btn_frame.bind('<Enter>', lambda e: copy_text_btn_frame.config(bg='#99d2f2'))
        copy_text_btn_frame.bind('<Leave>', lambda e: copy_text_btn_frame.config(bg='#e0f7fa'))
        copy_text_btn_frame.place(in_=self.explorer_textbox, relx=1.0, rely=0.0, anchor='ne', x=-14)


    def display_result(self, text):
        self.explorer_textbox.config(state='normal')
        self.explorer_textbox.delete(1.0, tk.END)
        self.explorer_textbox.insert(tk.END, "\n" + text)
        self.explorer_textbox.see('1.0')
        self.copy_text()

    
    def clear_result(self):
        self.explorer_textbox.delete(1.0, tk.END)
        self.explorer_textbox.config(state='normal')       
    
    
    def on_entry_focus(self, event):
        widget = event.widget
        
        if widget == self.explorer_add_pubkey_ent:
            widget.delete(0, 'end')            
            other_ent = self.explorer_check_address_ent
            if other_ent.get() == '':
                other_ent.insert(0, self.check_default_text)
                
            self.explorer_check_address_btn.config(state='disabled')
            self.explorer_add_pubkey_btn.config(state='normal')            
                
        elif widget == self.explorer_check_address_ent:
            widget.delete(0, 'end')            
            other_ent = self.explorer_add_pubkey_ent
            if other_ent.get() == '':
                other_ent.insert(0, self.add_default_text)
                
            self.explorer_add_pubkey_btn.config(state='disabled')
            self.explorer_check_address_btn.config(state='normal')

            
    def user_focus_in(self, event):
        if self.explorer_log_user.get() == 'Enter Node User':
            self.explorer_log_user.delete(0, 'end') 
            self.explorer_log_user.insert(0, '') 


    def user_focus_out(self, event):
        if self.explorer_log_user.get() == '':
            self.explorer_log_user.insert(0, 'Enter Node User')


    def pass_focus_in(self, event):
        if self.explorer_log_pass.get() == 'Enter Node PWD':
            self.explorer_log_pass.delete(0, 'end')  # Delete all the text in the entry
            self.explorer_log_pass.insert(0, '')
            # Hides password 
            self.explorer_log_pass.config(show='*')


    def pass_focus_out(self, event):
        if self.explorer_log_pass.get() == '':
            self.explorer_log_pass.insert(0, 'Enter Node PWD')
            self.explorer_log_pass.config(show='')


    def validate_credential_inputs(self):
        username = self.explorer_log_user.get().strip()
        password = self.explorer_log_pass.get().strip()

        if not username:
            return False, 'Username cannot be empty.'
        if not password:
            return False, 'Password cannot be empty.'
        
        return True, (username, password)
    
    
    def connect_click(self):
        is_valid, result = self.validate_credential_inputs()
        if not is_valid:
            messagebox.showerror('Input Validation Failed\n------\n', result)
            return

        username, password = result
        credentials = f'{username}:{password}'
        encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        auth_header = f'Basic {encoded}'

        # Store persistent Bitcoin Node access data. Password not Included. 
        # If user closes the app, persistent data is lost. User has to login next time.
        self.rpc_username = username
        self.rpc_auth_header = auth_header  # <-- Store this instead of password
        del password
        self.root.update_idletasks()

        result_blockchain_info = rpc_calls.get_blockchain_info(
            self.rpc_host,
            self.rpc_port,
            self.rpc_username,
            self.rpc_auth_header
        )

        if result_blockchain_info['success']:
            self.display_result(result_blockchain_info['data'])
            self.explorer_log_user.delete(0, tk.END)
            # Immediate Clearance: As soon as the user clicks “Connect”, the password disappears from the screen.
            self.explorer_log_pass.delete(0, tk.END)
            self.explorer_log_user.config(state='disabled')
            self.explorer_log_pass.config(state='disabled')
            self.explorer_log_connect_btn.config(state='disabled', text='Connected to Local Bitcoin Node')
            self.explorer_log_wallet_btn.config(state='normal')
            
        else:
            self.explorer_textbox.delete(1.0, tk.END)            
            self.explorer_textbox.config(state='normal')
            self.explorer_log_user.delete(0, tk.END)
            self.explorer_log_pass.delete(0, tk.END)
            self.explorer_textbox.insert(tk.END, 'Something is wrong. Check Bitcoin Node connection. Enter correct Bitcoin Node username and password.') 
            self.explorer_log_user.config(state='normal')
            self.explorer_log_pass.config(state='normal')
            self.explorer_log_connect_btn.config(state='normal', text='Connect to Local Bitcoin Node', fg='#f7931a')            
            self.root.after(2000, self.clear_result)            

    
    def load_wallet_click(self):        
        result_wallet_creation = rpc_calls.create_or_load_wallet(
                self.rpc_host,
                self.rpc_port,
                self.rpc_username,
                self.rpc_auth_header,
                self.wallet_name
                )

        if result_wallet_creation['success']:                
            result_wallet_creation_success = f'✅ Loaded default Watch-Only Wallet named "{result_wallet_creation['data']}"'
            self.display_result(result_wallet_creation_success)
            self.explorer_log_wallet_btn.config(state='disabled')
            self.explorer_add_pubkey_ent.config(state='normal')
            self.explorer_add_pubkey_btn.config(state='normal')
            self.explorer_check_address_ent.config(state='normal')
            self.explorer_check_address_btn.config(state='normal')
                
        else:
            result_wallet_creation_error = f'{result_wallet_creation}.\n\n'
            self.display_result(result_wallet_creation_error)
    
   
    def add_pubkey_clicked(self):
        self.pubkey_hex = self.explorer_add_pubkey_ent.get().strip()
        self.explorer_add_pubkey_ent.delete(0, 'end') 
        self.explorer_add_pubkey_ent.insert(0, self.add_default_text)
        self.explorer_add_pubkey_ent.config(bg='light gray')
        self.explorer_add_pubkey_btn.config(state='disabled')
        
        try:
            result_add_pubkey = rpc_calls.rpc_add_pubkey(
                self.rpc_host,
                self.rpc_port,
                self.rpc_username,
                self.rpc_auth_header,
                self.pubkey_hex,
                label='#1'
            )

            if result_add_pubkey['success']:
                import_results = result_add_pubkey['data']

                if isinstance(import_results, list) and len(import_results) > 0:
                    first_result = import_results[0]
                    if 'error' in first_result and first_result['error'] is not None:
                        err = first_result['error']
                        specific_importdescriptors_error_msg = (
                            f'\nImport Error reported by node: {err}'
                        )
                        self.display_result(specific_importdescriptors_error_msg)
                    else:
                        importdescriptors_success_msg = '\nImport successful!'
                        self.display_result(importdescriptors_success_msg)
                else:
                    self.display_result('\nUnexpected response format from importdescriptors.')
            else:
                error_msg = result_add_pubkey['data'] or 'Unknown error'
                self.display_result(f'\n{error_msg}')

        except Exception as e:
            gen_importdescriptors_errror_msg = f'Error: {e}'
            self.display_result(gen_importdescriptors_errror_msg)

        finally:
            self.explorer_add_pubkey_btn.config(state='normal')
            self.explorer_add_pubkey_ent.config(bg='white')

    ###############
    # Check Address
    ###############
    def run_rpc_in_thread(self, address: str) -> None:
        try:
            result_balance_transactions = rpc_calls.fetch_latest_balance_transactions(
                self.rpc_host,
                self.rpc_port,
                self.rpc_username,
                self.rpc_auth_header,
                address,
                limit=5
            )

            if result_balance_transactions['success']:
                data = result_balance_transactions['data']
                
                full_output = ''

                summary = (
                    f"Address: {data['address']}\n"
                    f"Total Balance: {data['total_balance']} tBTC\n"
                    f"Confirmed Transactions Found: {data['confirmed_transactions_found']}\n"
                    f"Showing Latest Confirmed Transactions: {len(data['transactions'])}\n"
                )
                full_output += summary + "\n"

                for i, tx in enumerate(data['transactions'], start=1):
                    tx_info = (
                        f"--- Transaction #{i} ---\n"
                        f"TXID: {tx['txid']}\n"
                        f"Block Height: {tx.get('blockheight')}\n"
                        f"Confirmations: {tx.get('confirmations')}\n"
                        f"Time: {tx.get('time')}\n"
                        f"Inputs ({len(tx['inputs'])}):\n"
                    )
                    for j, vin in enumerate(tx['inputs']):
                        script_sig_preview = vin['scriptSig'][:64] + "..." if len(vin['scriptSig']) > 64 else vin['scriptSig']
                        tx_info += (
                            f"  [{j}] txid={vin['txid']}, vout={vin['vout']}, "
                            f"scriptSig_hex={script_sig_preview}\n"
                        )

                    tx_info += f"Outputs ({len(tx['outputs'])}):\n"
                    for j, vout in enumerate(tx['outputs']):
                        spk = vout['scriptPubKey']
                        addrs = ','.join(spk.get('addresses', [])) or '(no addresses)'
                        tx_info += (
                            f"  [{j}] value={vout['value']} tBTC, type={spk['type']}, "
                            f"addresses=[{addrs}]\n"
                        )
                    
                    full_output += tx_info + '\n'

                self.root.after(0, self.display_result, full_output)

            else:
                error_msg = result_balance_transactions['data'] or 'Unknown error'
                self.root.after(0, self.display_result, f"\nFailed to scan address: {error_msg}")

        except Exception as e:
            gen_error_msg = f"Error: {e}"
            self.root.after(0, self.display_result, gen_error_msg)

        finally:
            self.root.after(0, lambda: self.explorer_check_address_btn.config(state='normal'))
            self.root.after(0, lambda: self.explorer_check_address_ent.config(bg='white'))


    def scan_address_clicked(self) -> None:
        address = self.explorer_check_address_ent.get().strip()
        self.explorer_check_address_ent.delete(0, 'end')
        self.explorer_check_address_ent.insert(0, self.add_default_text)
        self.explorer_check_address_ent.config(bg='light gray')
        self.explorer_check_address_btn.config(state='disabled')

        self.display_result('Processing ...')

        thread = threading.Thread(target=self.run_rpc_in_thread, args=(address,), daemon=True)
        thread.start()

    ###################
    # Address Functions
    ###################  
    def create_address_mouse_copy(self, event):
        if event.state == 4 and event.keysym == 'c':
            address_textbox_content = self.create_address_key_text.selection_get()
            self.create_address_outer_frame.clipboard_clear()
            self.create_address_outer_frame.clipboard_append(address_textbox_content)
            return 'break'
        elif event.state == 4 and event.keysym == 'v':
            self.create_address_key_text.insert('end', self.create_address_outer_frame.selection_get(selection='CLIPBOARD'))
            return 'break'
        else:
            return 'break'        
    

    def create_address_disable_click_master(self, event):
        if not self.create_address_key_text.get('1.0', 'end-1c'): 
            return 'break'    


    def create_address_key_address(self): 
        try:
            addr, tweaked_privkey, tweaked_pubkey = master_key.iden()
            self.content_key_address = f"\nBitcoin Address: {addr} \n\n\nPrivate Key: {tweaked_privkey}\n\n\nPublic Key: {tweaked_pubkey}" 
            return self.content_key_address
        
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
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
        self.create_address_key_text.after(300000, self.create_address_delete_keyadd)    
        self.create_address_key_button.update()  
    

    def adress_move_up(event):
        self.create_address_key_text.mark_set('insert', 'insert-1lines') # type: ignore
        self.create_address_key_text.see('insert') # type: ignore
        return 'break'


    def adress_move_down(event):
        self.create_address_key_text.mark_set('insert', 'insert+1lines') # type: ignore
        self.create_address_key_text.see('insert') # type: ignore
        return 'break'  
    

    def is_address_copy_clicked(self):
        self.create_address_text_frame.clipboard_clear()
        self.create_address_text_frame.clipboard_append(self.create_address_key_text.get("1.0", tk.END))           


    def address_copy_button_enable(self):
        self.create_address_copy_button.config(state='normal')


    def address_clear_button_enable(self):
        self.create_address_clear_button.config(state='normal')
        

    def address_copy_button_disable(self):
        self.create_address_copy_button.config(state='disabled')


    def address_clear_button_disable(self):
        self.create_address_clear_button.config(state='disabled')


    def clear_address_text(self):
        self.create_address_key_text.delete('1.0', 'end')    

    ###################
    # Privacy Functions
    ###################
    def privacy_move_up(event):
        self.privacy_textbox.mark_set('insert', 'insert-1lines') # type: ignore
        self.privacy_textbox.see('insert') # type: ignore
        return 'break'


    def privacy_move_down(event):
        self.privacy_textbox.mark_set('insert', 'insert+1lines') # type: ignore
        self.privacy_textbox.see('insert') # type: ignore
        return 'break'

    ###################
    # Clean Up on Close
    ###################
    def on_close(self):
        # Clear sensitive data
        self.rpc_auth_header = None
        self.rpc_host = None
        self.rpc_port = None
        self.rpc_username = None
        self.root.destroy()

#################
# Run Application
#################
main_root = tk.Tk()
home_instance = Home(main_root)
main_root.mainloop()
