import tkinter as tk
from tkinter import WORD
from tkinter import messagebox
import master
import decimal
import requests, json
import master


class Home():
    def __init__(self, root):
        self.root = root
        ###########
        # Stringvar
        ###########        
        # Explorer
        self.address_balance_var = tk.StringVar()
        # Send
        self.recipient_address_var = tk.StringVar()
        self.recipient_amount_var = tk.StringVar()
        self.miner_fee_var = tk.StringVar()
        self.sender_address_var = tk.StringVar()
        self.sender_key_var = tk.StringVar()
        self.sender_note_var = tk.StringVar()
        self.send_donation_var = tk.StringVar()

        ##############
        # Main Widgets
        ##############
        root.title('Novel Bitcoin Payment Service -- Testnet 4. AGPL-3.0 License.')
        root.resizable(False, False)    
        root.config(bg='#414850')
        self.main_win_screen_width = root.winfo_screenwidth()
        self.main_win_screen_height =root.winfo_screenheight()
        self.main_win_window_width = 975 
        self.main_win_window_height = 500
        self.main_win_x = (self.main_win_screen_width // 2) - (self.main_win_window_width  // 2)
        self.main_win_y = (self.main_win_screen_height // 2) - (self.main_win_window_height // 2)
        root.geometry(f'{self.main_win_window_width}x{self.main_win_window_height}+{self.main_win_x}+{self.main_win_y}')
        
        # Main Logo/Buttons Frame
        self.main_logo_buttons_frame = tk.Frame(root, borderwidth=0.5, bg='#414850')
        self.main_logo_buttons_frame.pack(side='top')

        # Main Logo
        self.main_logo = tk.PhotoImage(file='novel_logo81.png') 
        self.main_logo_label = tk.Label(self.main_logo_buttons_frame, borderwidth=0, highlightthickness=0, image=self.main_logo)
        self.main_logo_label.grid(row=0, column=0, rowspan=15)

        # Main Home Button
        self.main_home_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_home_click(), state=tk.DISABLED, text= 'Home', bg='#4f697f', width=5, font=('Segoe', 9))
        self.main_home_button.grid(row=1, column=2)

        # Main Explorer Button
        self.main_explorer_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_explorer_click(), text= 'Block Explorer', bg='#4f697f', width=11, font=('Segoe', 9))
        self.main_explorer_button.grid(row=1, column=3)
        
        # Main Address Button
        self.main_gen_address_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_gen_address_click(), text= 'Create Address', bg='#4f697f', width=12, font=('Segoe', 9))
        self.main_gen_address_button.grid(row=1, column=4)

        # Main Smart Contract Button
        self.main_smart_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_gen_address_click(), state=tk.DISABLED, text= 'Smart Contract', bg='#4f697f', width=12, font=('Segoe', 9))
        self.main_smart_button.grid(row=1, column=5)

        # Main Send Button
        self.main_sats_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_send_click(), text= 'Payment Service', bg='#4f697f', width=13, font=('Segoe', 9))
        self.main_sats_button.grid(row=1, column=6)

        # Main Privacy Button
        self.main_privacy_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_privacy_click(), text= 'Privacy/Terms', bg='#4f697f', width=11, font=('Segoe', 9))
        self.main_privacy_button.grid(row=1, column=7) 

        # Main FAQ Button
        self.main_faq_button = tk.Button(self.main_logo_buttons_frame, command=lambda: self.main_faq_click(), text= 'FAQ', bg='#4f697f', width=4, font=('Segoe', 9))
        self.main_faq_button.grid(row=1, column=8)

        ##############
        # Home Widgets
        ##############
        # Home Outer Frame
        self.home_outer_frame = tk.Frame(root, bg='#414850')
        self.home_outer_frame.pack()
       
        # Home Label1
        self.home_win_label = tk.Label(self.home_outer_frame, bg='#414850', fg='white', text='"Bitcoin: A Peer-to-Peer Electronic Cash System"', font=('Segoe', 16, 'bold italic'))
        self.home_win_label.pack(side='top', pady=50)

        # Home Label1
        self.home_win_label = tk.Label(self.home_outer_frame, bg='#414850', fg='white', text='Novel Bitcoin Payment Service aims to be your very own Bitcoin payment service.', font=('Segoe', 13, 'bold italic'))
        self.home_win_label.pack(side='top')

        ##################
        # Explorer Widgets
        ##################
        # Explorer Outer Frame
        self.explorer_outer_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='#414850')
        self.explorer_outer_frame.pack()
        self.explorer_outer_frame.pack_forget()

        # Explorer Label Frame
        self.explorer_win_label_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_win_label_frame.pack(side='top')

        # Explorer Address/ID Frame
        self.explorer_addressid_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_addressid_frame.pack(side='top')

        # Explorer Search Buttons Frame 
        self.explorer_search_buttons_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_search_buttons_frame.pack(side='top')

        # Explorer Textbox Frame 
        self.explorer_textbox_frame = tk.Frame(self.explorer_outer_frame, bg='#414850')
        self.explorer_textbox_frame.pack(side='top')
        
        # Explorer Label
        self.explorer_win_label = tk.Label(self.explorer_win_label_frame, bg='#414850', fg='white', text='B l o c k   E x p l o r e r', font=('Segoe', 12, 'bold'))
        self.explorer_win_label.pack(side='left')

        # Explorer Address & ID
        self.input_balance_label = tk.Label(self.explorer_addressid_frame, text="Enter Bitcoin Address (Limit to 62 Alphanumeric) *", font=("Segoe", 10), fg='white', bg='#414850')
        self.input_balance_label.pack()
        self.entry_balance = tk.Entry(self.explorer_addressid_frame, bg='#e2dada', validate="key", textvariable=self.address_balance_var, width=85, font=("Segoe", 9))
        self.entry_balance['validatecommand'] = (self.entry_balance.register(self.explorer_val_addr),'%P','%d')
        self.entry_balance.pack()

        # Explorer Check Address Balance Button
        self.balance_button = tk.Button(self.explorer_search_buttons_frame, text= "Check Bitcoin Address Balance", fg="black",  bg='#4f697f', height=1, width=23, font=("Segoe", 10), command=self.explorer_show_delete_balance) 
        self.balance_button.bind("<Enter>", lambda event, h=self.balance_button : h.configure())
        self.balance_button.bind("<Leave>", lambda event, h=self.balance_button : h.configure())
        self.balance_button.grid(row=0, column=0, padx=10)
        
        # Explorer Instant Messaging System Button
        self.explorer_messages_button = tk.Button(self.explorer_search_buttons_frame, state=tk.DISABLED, text= "Check Messages", fg="black",  bg='#4f697f', width=13, font=("Segoe", 10)) 
        self.explorer_messages_button.bind("<Enter>", lambda event, h=self.explorer_messages_button : h.configure())
        self.explorer_messages_button.bind("<Leave>", lambda event, h=self.explorer_messages_button : h.configure())
        self.explorer_messages_button.grid(row=0, column=2, pady=7)

        # Explorer Balance Textbox
        self.text_balance = tk.Text(self.explorer_textbox_frame, bg='#e2dada', width=110, height=15, fg="black", font=("Arial", 11))
        self.text_balance.bind("<Key>", lambda e: "break")
        self.text_balance.bind("<Button-1>", self.explorer_disable_click_balance)
        self.text_balance.pack(pady=2)
        
        ##########################
        # Create Address Widgets
        ##########################
        # Create Address Outer Frame
        self.create_address_outer_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='#414850')
        self.create_address_outer_frame.pack(pady=40)
        self.create_address_outer_frame.pack_forget()

        # Create Address Label + Button Frame
        self.create_address_label_button_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_label_button_frame.pack()

        # Create Address Text + Logo Frame
        self.create_address_textlogo_frame = tk.Frame(self.create_address_outer_frame, bg='#414850')
        self.create_address_textlogo_frame.pack()

        # Create Address Label
        self.create_address_win_label = tk.Label(self.create_address_label_button_frame, bg='#414850', fg='white', text='C r e a t e  A d d r e s s', font=('Segoe', 12, 'bold'))
        self.create_address_win_label.pack(side='top')
        
        # Create Address Button
        self.create_address_key_button = tk.Button(self.create_address_label_button_frame, text= "Generate Single Signature Taproot Bitcoin Address with Private Key", bg='#4f697f', height=1, width=52, font=("Segoe", 10), command=self.create_address_show_delete_keyadd)
        self.create_address_key_button.bind("<Enter>", lambda event, h=self.create_address_key_button: h.configure())
        self.create_address_key_button.bind("<Leave>", lambda event, h=self.create_address_key_button: h.configure())
        self.create_address_key_button.pack(pady=5)
        
        # Create Address Text
        self.create_address_key_text = tk.Text(self.create_address_textlogo_frame, bg='#e2dada', height=4, width=70, fg="black", font=("Segoe", 9))
        self.create_address_key_text.bind("<Button-1>", self.create_address_disable_click_master)
        self.create_address_key_text.bind("<Key>", lambda e: "break")
        self.create_address_key_text.bind("<Key>", lambda e: self.create_address_mouse_copy(e))
        self.create_address_key_text.grid(row=0, column=0)

        # Create Address Copy Button
        self.create_address_logo = tk.PhotoImage(file='c713.gif') 
        self.create_address_copy_button = tk.Button(self.create_address_textlogo_frame, image=self.create_address_logo, compound=tk.LEFT, command= lambda: self.is_address_copy_clicked())                           
        self.create_address_copy_button.bind("<Enter>", lambda event, h=self.create_address_copy_button: h.configure(bg='red'))
        self.create_address_copy_button.bind("<Leave>", lambda event, h=self.create_address_copy_button: h.configure(bg='orange'))
        self.create_address_copy_button.grid(row=0, column=1)        

        ##############
        # Send Widgets
        ##############
        # Send Outer Frame
        self.send_outer_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='#414850')
        self.send_outer_frame.pack()
        self.send_outer_frame.pack_forget()

        # Send Label Frame
        self.send_win_label_frame = tk.Frame(self.send_outer_frame, bg='#414850')
        self.send_win_label_frame.pack(side='top')

        # Send Label
        self.send_win_label = tk.Label(self.send_win_label_frame, bg='#414850', fg='white', text='P a y m e n t   S e r v i c e', font=('Segoe', 12, 'bold'))
        self.send_win_label.pack(side='left')

        # Send General Frame       
        self.send_general_frame = tk.Frame(self.send_outer_frame, bg='#414850')
        self.send_general_frame.pack()

        # Send Recipient Address
        self.recipient_address_label = tk.Label(self.send_general_frame, text="Enter Recipient Address (Limit to 62 Alphanumeric)", font=("Segoe", 10), fg='white', bg='#414850')
        self.recipient_address_label.pack()
        self.input_recipient_address = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.recipient_address_var, width=85, font=("Segoe", 8))
        self.input_recipient_address['validatecommand'] = (self.input_recipient_address.register(self.send_val_addr),'%P','%d')
        self.input_recipient_address.pack(padx=20, pady=2)

        # Send Amount to Recipient
        self.amount_recipient_label = tk.Label(self.send_general_frame, text="Enter Amount to Recipient (Limit to 8 decimal places)", font=("Segoe", 10), fg='white', bg='#414850')
        self.amount_recipient_label.pack()
        self.input_recipient_amount = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.recipient_amount_var, width=85,font=("Segoe", 8))
        self.input_recipient_amount['validatecommand'] = (self.input_recipient_amount.register(self.send_val_deci),'%P','%d')
        self.input_recipient_amount.pack(padx=20, pady=2)

        # Send Miner's Fee
        self.miner_fee_label = tk.Label(self.send_general_frame, text="Enter Miner's Fee (Limit to 8 decimal places)", fg='white', bg='#414850', font=("Segoe", 10))
        self.miner_fee_label.pack()
        self.input_miner_amount = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.miner_fee_var, width=85,font=("Segoe", 8))
        self.input_miner_amount['validatecommand'] = (self.input_miner_amount.register(self.send_val_deci),'%P','%d')
        self.input_miner_amount.pack(padx=20, pady=2)

        # Sender Address
        self.sender_address_label = tk.Label(self.send_general_frame, text="Enter Sender Address (Limit to 62 Alphanumeric)", font=("Segoe", 10), fg='white', bg='#414850')
        self.sender_address_label.pack()
        self.input_sender_address = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.sender_address_var, width=85, font=("Segoe", 8))
        self.input_sender_address['validatecommand'] = (self.input_sender_address.register(self.send_val_addr),'%P','%d')
        self.input_sender_address.pack(padx=20, pady=2)

        # Sender Private Key
        self.sender_key_label = tk.Label(self.send_general_frame, text="Enter Sender Private Key (Limit to 64 Alphanumeric. Key isn't visible.) Novel self-destructs all users' data.", font=("Segoe", 10), fg='white', bg='#414850')
        self.sender_key_label.pack(padx=10)
        self.input_sender_key = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.sender_key_var, width=85, font=("Segoe", 8), show="*")
        self.input_sender_key['validatecommand'] = (self.input_sender_key.register(self.send_val_k),'%P','%d')
        self.input_sender_key.pack(padx=20, pady=2)

        # Send Message to Recipient
        self.sender_note_label = tk.Label(self.send_general_frame, text="Enter Message to Recipient (Limit to 64 Alphanumeric) -- Optional", font=("Segoe", 10), fg='white', bg='#414850')
        self.sender_note_label.pack()
        self.input_note_key = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.sender_note_var, width=85, font=("Segoe", 8))
        self.input_note_key['validatecommand'] = (self.input_note_key.register(self.send_val_k),'%P','%d')
        self.input_note_key.pack(padx=20, pady=2)

        # Send Donation 
        self.send_donation_label = tk.Label(self.send_general_frame, text="Enter Donation Amount to Developer (Limit to 8 decimal places) -- Optional", fg='white', bg='#414850', font=("Segoe", 10))
        self.send_donation_label.pack()
        self.send_donation_amount = tk.Entry(self.send_general_frame, bg='#e2dada', validate="key", textvariable=self.send_donation_var, width=85,font=("Segoe", 8))
        self.send_donation_amount['validatecommand'] = (self.send_donation_amount.register(self.send_val_deci),'%P','%d')
        self.send_donation_amount.pack(padx=20, pady=2)

        # Send Button
        self.send_button = tk.Button(self.send_outer_frame, text= "Send Bitcoin + Message", state=tk.DISABLED, fg="black", bg='#4f697f', height=1, width=19, font=("Segoe", 10, 'bold'), command=self.send_update_pbar) 
        self.send_button.bind("<Enter>", lambda event, h=self.send_button : h.configure())
        self.send_button.bind("<Leave>", lambda event, h=self.send_button : h.configure())
        self.send_button.pack(pady=5)

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
        self.privacy_scrollbar = tk.Scrollbar(self.privacy_inner_frame, orient='vertical')
        self.privacy_scrollbar.pack(side='right', fill='y')        
        self.privacy_textbox = tk.Text(self.privacy_inner_frame, wrap=WORD, width=110, height=23, font=('Segoe', 11), yscrollcommand=self.privacy_scrollbar.set)
        self.privacy_textbox.insert(tk.END, 'Privacy Policy + Terms of Service\n\nBitcoin Payment Service respects your privacy. It doesn’t access, collect, or transmit any information (data that could be used to identify a person). As a user of this service, you have full control over your bitcoin address and private key. What this means is that you are fully responsible for securing your bitcoin address and private key and you have full control over your bitcoin funds.\n\n\n\nTerms of Service\n\nBY USING THIS BITCOIN PAYMENT SERVICE, YOU AGREE THAT YOU WILL NOT USE THIS SERVICE TO COMMIT ILLEGAL ACTIVITIES WITHIN AND OUTSIDE YOUR GEOGRAPHICAL LOCATION.')  
        self.privacy_textbox.config(state=tk.DISABLED)
        self.privacy_textbox.pack()

        ######################
        # FAQ-Tutorial Widgets
        ######################
        # FAQ Outer Frame
        self.faq_outer_frame = tk.Frame(root, bg='#414850')
        self.faq_outer_frame.pack()
        self.faq_outer_frame.pack_forget()

        # FAQ Textbox Frame
        self.faq_textbox_frame = tk.Frame(self.faq_outer_frame, bg='#414850')
        self.faq_textbox_frame.pack()

        # FAQ Textbox
        self.faq_scrollbar = tk.Scrollbar(self.faq_textbox_frame, orient='vertical')
        self.faq_scrollbar.pack(side='right', fill='y')
        self.faq_textbox = tk.Text(self.faq_textbox_frame, wrap=WORD, width=110, height=23, font=('Segoe', 11), yscrollcommand=self.faq_scrollbar.set)
        self.faq_textbox.insert(tk.END, 'Frequently Asked Questions(FAQ)/Tutorial\n\nWhat is new with this Bitcoin Payment Service?\n\nBitcoin Payment Service aims to be your very own payment service, attaining the goal of Peer-to-Peer Electronic Cash System as envisioned by Satoshi Nakamoto.\n\nIn the Bitcoin white paper written by Nakamoto, Peer-to-Peer Electronic Cash System is described as allowing online payments to be sent directly from one party to another without going through a financial institution.\n\nThis payment service does not aim to be a financial institution. Rather, this payment service aims to be a means for ordinary folks to send bitcoin, whether as payment or donation, to one another, that is, without an intermediary financial institution.\n\nSpecifically, this payment service will allow ordinary folks to:\n1. Create bitcoin addresses\n2. Create smart contracts\n3. Check bitcoin address balance using an in-built blockchain explorer\n4. Receive bitcoin\n5. Send bitcoin\n6. Communicate regarding the received or sent satoshis within the Bitcoin blockchain\n\nUnknown to many, Nakamoto built within the Bitcoin infrastracture a means for senders and receivers to communicate with each other. Nakamoto also built within the Bitcoin infrastracture smart contracts. These in-built communication system and smart contracts within the Bitcoin blockchain will be put into use in this novel Bitcoin Payment System.\n\nThis Bitcoin Payment Service is a work in progress.')  
        self.faq_textbox.config(state=tk.DISABLED)
        self.faq_textbox.pack()        

    ################
    # Main Functions
    ################
    def main_home_click(self):
        self.explorer_outer_frame.pack_forget()
        self.create_address_outer_frame.pack_forget()
        self.privacy_outer_frame.pack_forget()
        self.faq_outer_frame.pack_forget()
        self.send_outer_frame.pack_forget()
        self.main_explorer_button.config(state=tk.NORMAL)
        self.main_gen_address_button.config(state=tk.NORMAL)
        self.main_faq_button.config(state=tk.NORMAL)
        self.main_privacy_button.config(state=tk.NORMAL)
        self.main_home_button.config(state=tk.DISABLED)
        self.main_sats_button.config(state=tk.NORMAL)
        self.home_outer_frame.pack()
        # Destroy Payment Entries Pending Send Button Activation
        self.input_recipient_address.delete(0, tk.END)
        self.input_recipient_amount.delete(0, tk.END)
        self.input_miner_amount.delete(0, tk.END)
        self.input_sender_address.delete(0, tk.END)
        self.input_sender_key.delete(0, tk.END)
        self.input_note_key.delete(0, tk.END)
        self.send_donation_amount.delete(0, tk.END)
    
    def main_explorer_click(self):
        self.home_outer_frame.pack_forget()
        self.main_explorer_button.config(state=tk.DISABLED)
        self.main_gen_address_button.config(state=tk.DISABLED)
        self.main_privacy_button.config(state=tk.DISABLED)
        self.main_faq_button.config(state=tk.DISABLED)
        self.main_sats_button.config(state=tk.DISABLED)
        self.explorer_outer_frame.pack()
        self.main_home_button.config(state=tk.NORMAL)
        self.main_home_button.config(fg='#f7931a')

    def main_gen_address_click(self):
        self.home_outer_frame.pack_forget()
        self.main_gen_address_button.config(state=tk.DISABLED)
        self.main_explorer_button.config(state=tk.DISABLED)
        self.main_privacy_button.config(state=tk.DISABLED)
        self.main_faq_button.config(state=tk.DISABLED)
        self.main_sats_button.config(state=tk.DISABLED)
        self.create_address_outer_frame.pack()
        self.main_home_button.config(state=tk.NORMAL)
        self.main_home_button.config(fg='#f7931a')

    def main_send_click(self):
        self.home_outer_frame.pack_forget()
        self.main_privacy_button.config(state=tk.DISABLED)
        self.main_gen_address_button.config(state=tk.DISABLED)
        self.main_explorer_button.config(state=tk.DISABLED)
        self.main_faq_button.config(state=tk.DISABLED)
        self.send_outer_frame.pack()
        self.main_home_button.config(state=tk.NORMAL)
        self.main_home_button.config(fg='#f7931a')

    def main_privacy_click(self):
        self.home_outer_frame.pack_forget()
        self.main_privacy_button.config(state=tk.DISABLED)
        self.main_gen_address_button.config(state=tk.DISABLED)
        self.main_explorer_button.config(state=tk.DISABLED)
        self.main_faq_button.config(state=tk.DISABLED)
        self.main_sats_button.config(state=tk.DISABLED)
        self.privacy_outer_frame.pack()
        self.main_home_button.config(state=tk.NORMAL)
        self.main_home_button.config(fg='#f7931a')

    def main_faq_click(self):
        self.home_outer_frame.pack_forget()
        self.main_faq_button.config(state=tk.DISABLED)
        self.main_gen_address_button.config(state=tk.DISABLED)
        self.main_explorer_button.config(state=tk.DISABLED)
        self.main_privacy_button.config(state=tk.DISABLED)
        self.main_sats_button.config(state=tk.DISABLED)
        self.faq_outer_frame.pack()
        self.main_home_button.config(state=tk.NORMAL)
        self.main_home_button.config(fg='#f7931a')

    ####################
    # Explorer Functions
    ####################
    def explorer_val_addr(self, value, inp_typ):    
        if inp_typ == '1':
            value_len = len(value)
            if value_len > 62:
                return False  
            if not value.isalnum():
                return False
        return True
    
    def explorer_disable_click_balance(self, event):
        if not self.text_balance.get("1.0", "end-1c"): 
            return "break"         

    def explorer_balance(self):
        try: 
            # For now, Blockstream is used in the absence of an in-built blockchain explorer. Internet connection needed.
            self.url = f'https://blockstream.info/testnet/api/address/{self.address_balance_var.get()}' 
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            self.data = self.response.json()
            self.chain_stats = self.data['chain_stats']
            self.mempool_stats = self.data['mempool_stats']
            self.confirmed_balance = self.chain_stats['funded_txo_sum'] - self.chain_stats['spent_txo_sum']
            self.unconfirmed_balance = self.mempool_stats['funded_txo_sum'] - self.mempool_stats['spent_txo_sum']
            self.confirmed_bit = decimal.Decimal(self.confirmed_balance) / decimal.Decimal('100000000')
            self.unconfirmed_bit = decimal.Decimal(self.unconfirmed_balance) / decimal.Decimal('100000000')
            self.show_sat_to_bit = f'Confirmed Balance: {self.confirmed_bit } BTC \nUnconfirmed Balance: {self.unconfirmed_bit} BTC'
            return self.show_sat_to_bit
        except:
            return "Can't verify address and balance"

    def explorer_delete_entry_balance(self):
        self.entry_balance.delete(0, tk.END)

    def explorer_delete_text_balance(self):
        self.text_balance.delete('1.0','end')

    def explorer_show_delete_balance(self):
        self.balance_def = self.explorer_balance()    
        self.balance_button.config(state="disabled")
        self.text_balance.tag_configure("center", justify='center')
        self.text_balance.insert(tk.INSERT, self.balance_def)
        self.text_balance.tag_add("center", "1.0", "end")
        self.text_balance.after(5000, self.explorer_delete_text_balance)    
        self.entry_balance.after(5000, self.explorer_delete_entry_balance)
        self.balance_button.update()
        self.enable = self.balance_button.config(state="normal")
        self.text_balance.after(5001, self.enable)
    
    ###################
    # Address Functions
    ###################
    def create_address_mouse_copy(self, event):
        if event.state == 4 and event.keysym == 'c':
            address_textbox_content = self.create_address_key_text.selection_get()
            self.create_address_outer_frame.clipboard_clear()
            self.create_address_outer_frame.clipboard_append(address_textbox_content)
            return "break"
        elif event.state == 4 and event.keysym == 'v':
            self.create_address_key_text.insert('end', self.create_address_outer_frame.selection_get(selection='CLIPBOARD'))
            return "break"
        else:
            return "break"        

    def create_address_disable_click_master(self, event):
        if not self.create_address_key_text.get("1.0", "end-1c"): 
            return "break"    

    def create_address_key_address(self): 
        addr, tweak_pri_hex, tweak_pri_codec, tweak_pubx_hex = master.iden()
        self.content_key_address = f'Bitcoin Address and Private Key\n\nBitcoin Address: {addr} \n\n\nPrivate Key: {tweak_pri_hex}\n' 
        return self.content_key_address
    
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
        self.create_address_key_text.tag_configure("center", justify='center')  
        self.create_address_key_text.insert(tk.INSERT, self.key_add)
        self.create_address_key_text.tag_add("center", "1.0", "end")
        self.create_address_key_text.after(5000, self.create_address_delete_keyadd)    
        self.create_address_key_button.update()

    def is_address_copy_clicked(self):
        self.create_address_textlogo_frame.clipboard_clear()
        self.create_address_textlogo_frame.clipboard_append(self.create_address_key_text.get("1.0", tk.END))   
    
    
    ################
    # Send Functions
    ################
    def send_disable_click_send(self, event):
        if not self.text_send.get("1.0", "end-1c"): 
            return "break"

    def send_val_addr(self, value, inp_typ):    
        if inp_typ == '1':
            value_len = len(value)
            if value_len > 62:
                return False  
            if not value.isalnum():
                return False
        return True

    def send_val_k(self, value, inp_typ):    
        if inp_typ == '1':
            value_len = len(value)
            if value_len > 64:
                return False  
            if not value.isalnum():
                return False
        return True

    def send_val_deci(self, P, inp_typ):
        if inp_typ == '1':
            text = P
            parts = text.split('.')
            parts_number = len(parts)
            if parts_number > 2:
                return False        
            if parts_number > 1 and parts[1]: 
                if not parts[1].isdecimal() or len(parts[1]) > 8:
                    return False
            if parts_number > 0 and parts[0]: 
                if not parts[0].isdecimal():
                    return False
        return True
 
    def send_update_pbar(self):
        pass
    

#################
# Run Application
#################
main_root = tk.Tk()
home_instance = Home(main_root)
main_root.mainloop()
