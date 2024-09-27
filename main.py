# Copyright © 2024 Ellen Red. All rights reserved.

import decimal
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import WORD


class Home:
    def __init__(self, root):
        self.root = root
        # StringVar
        self.address_balance_var = tk.StringVar()
        self.recipient_address_var = tk.StringVar()
        self.recipient_amount_var = tk.StringVar()
        self.miner_fee_var = tk.StringVar()
        self.sender_address_var = tk.StringVar()
        self.sender_key_var = tk.StringVar()
        self.sender_note_var = tk.StringVar() 
        # FAQ
        self.faq_button = tk.Button(self.root, text= "Frequently Asked Questions (FAQ)", bg='gray', height=1, width=30, font=("Arial", 10, 'bold'), command=self.faq_window)
        self.faq_button.bind("<Enter>", lambda event, h=self.faq_button: h.configure(bg="white"))
        self.faq_button.bind("<Leave>", lambda event, h=self.faq_button: h.configure(bg="gray"))
        self.faq_button.pack(padx=10, in_=top, side='left')
        # Terms of Service + Privacy Policy
        self.terms_button = tk.Button(self.root, text= "Terms of Service + Privacy Policy", bg='gray', height=1, width=30, font=("Arial", 10, 'bold'), command=self.terms)
        self.terms_button.bind("<Enter>", lambda event, h=self.terms_button: h.configure(bg="white"))
        self.terms_button.bind("<Leave>", lambda event, h=self.terms_button: h.configure(bg="gray"))
        self.terms_button.pack(padx=10, in_=top, side='left')
        # Donate
        self.support_button = tk.Button(self.root, text= "Donate", bg='gray', height=1, width=30, font=("Arial", 10, 'bold'), command=self.donate)
        self.support_button.bind("<Enter>", lambda event, h=self.support_button: h.configure(bg="white"))
        self.support_button.bind("<Leave>", lambda event, h=self.support_button: h.configure(bg="gray"))
        self.support_button.pack(padx=10, in_=top, side='left')
        # Key + Address
        self.label_step1 = tk.Label(self.root, text="Step 1: Get new bitcoin address and private key. Warning! Address & key will self-destruct in 5 seconds.", bg='#0f3d0f', fg="white", font=("Segoe", 9))
        self.label_step1.pack(pady=10)
        self.key_button = tk.Button(self.root, text= "Get New Bitcoin Address + Private Key (Disabled)", bg="gray", height=1, width=40, font=("Arial", 10, 'bold'), command=self.show_delete_keyadd)
        self.key_button.bind("<Enter>", lambda event, h=self.key_button: h.configure(bg="white"))
        self.key_button.bind("<Leave>", lambda event, h=self.key_button: h.configure(bg="gray"))
        self.key_button.pack(padx=10)
        self.text_key_address = tk.Text(self.root, bg='#8fbc8f', height=2, width=90, fg="black", font=("Arial", 11))
        self.text_key_address.bind("<Button-1>", self.disable_click_master)
        self.text_key_address.bind("<Key>", lambda e: "break")
        self.text_key_address.pack()
        # Send Bitcoin
        self.label_send = tk.Label(self.root, text="Step 2: Send bitcoin. Warning! Check multiple times entries made. Wrong entry could mean sending bitcoin to wrong person. ", bg='#0f3d0f', fg="white", font=("Segoe", 9))
        self.label_send.pack(pady=20)
        self.frame = tk.Frame(self.root, bg='#8fbc8f')
        self.frame.pack()
        # Recipient Address
        self.recipient_address_label = tk.Label(self.frame, text="Enter Recipient Address (Limit to 62 Alphanumeric)", font=("Arial", 9), bg='#8fbc8f')
        self.recipient_address_label.pack()
        self.input_recipient_address = tk.Entry(self.frame, validate="key", textvariable=self.recipient_address_var,  width=85,font=("Arial", 9), borderwidth=2, relief="raised")
        self.input_recipient_address['validatecommand'] = (self.input_recipient_address.register(self.val_addr),'%P','%d')
        self.input_recipient_address.pack()
        # Amount to Recipient
        self.amount_recipient_label = tk.Label(self.frame, text="Enter Amount to Recipient (Limit to 8 decimal places)", font=("Arial", 9), bg='#8fbc8f')
        self.amount_recipient_label.pack()
        self.input_recipient_amount = tk.Entry(self.frame, validate="key", textvariable=self.recipient_amount_var, width=85,font=("Arial", 9), borderwidth=2, relief="raised")
        self.input_recipient_amount['validatecommand'] = (self.input_recipient_amount.register(self.val_deci),'%P','%d')
        self.input_recipient_amount.pack()
        # Miner's Fee
        self.miner_fee_label = tk.Label(self.frame, text="Enter Miner's Fee (Limit to 8 decimal places)", bg='#8fbc8f', font=("Arial", 9))
        self.miner_fee_label.pack()
        self.input_miner_amount = tk.Entry(self.frame, validate="key", textvariable=self.miner_fee_var, width=85,font=("Arial", 9), borderwidth=2, relief="raised")
        self.input_miner_amount['validatecommand'] = (self.input_miner_amount.register(self.val_deci),'%P','%d')
        self.input_miner_amount.pack()
        # Sender Address
        self.sender_address_label = tk.Label(self.frame, text="Enter Sender Address (Limit to 62 Alphanumeric)", font=("Arial", 9), bg='#8fbc8f')
        self.sender_address_label.pack()
        self.input_sender_address = tk.Entry(self.frame, validate="key", textvariable=self.sender_address_var, width=85, font=("Arial", 9), borderwidth=2, relief="raised")
        self.input_sender_address['validatecommand'] = (self.input_sender_address.register(self.val_addr),'%P','%d')
        self.input_sender_address.pack()
        # Sender Private Key
        self.sender_key_label = tk.Label(self.frame, text="Enter Sender Private Key (Limit to 64 Alphanumeric)", font=("Arial", 9), bg='#8fbc8f')
        self.sender_key_label.pack()
        self.input_sender_key = tk.Entry(self.frame, validate="key", textvariable=self.sender_key_var, width=85, font=("Arial", 9), borderwidth=2, relief="raised", show="*")
        self.input_sender_key['validatecommand'] = (self.input_sender_key.register(self.val_k),'%P','%d')
        self.input_sender_key.pack()
        # Note to Recipient
        self.sender_note_label = tk.Label(self.frame, text="Enter Note to Recipient (Limit to 64 Alphanumeric)", font=("Arial", 9), bg='#8fbc8f')
        self.sender_note_label.pack()
        self.input_note_key = tk.Entry(self.frame, validate="key", textvariable=self.sender_note_var, width=85, font=("Arial", 9), borderwidth=2, relief="raised")
        self.input_note_key['validatecommand'] = (self.input_note_key.register(self.val_k),'%P','%d')
        self.input_note_key.pack()
        # Send Button
        self.send_button = tk.Button(self.root, text= "Send Bitcoin (Disabled)", fg="black", bg='gray', height=1, width=40, font=("Arial", 10, 'bold'), command=self.update_pbar) 
        self.send_button.bind("<Enter>", lambda event, h=self.send_button : h.configure(bg="white"))
        self.send_button.bind("<Leave>", lambda event, h=self.send_button : h.configure(bg="gray"))
        self.send_button.pack(pady=2)
        # Balance
        self.label_check_balance = tk.Label(self.root, text="Step 3: Check address balance. Warning! Address and balance will self-destruct in 5 seconds. ", bg='#0f3d0f', fg="white", font=("Segoe", 9))
        self.label_check_balance.pack(pady=20)
        self.input_balance_label = tk.Label(self.root, text="Enter Bitcoin Address (Limit to 62 Alphanumeric) *", font=("Arial", 9), bg='#8fbc8f')
        self.input_balance_label.pack()
        self.entry_balance = tk.Entry(self.root, validate="key", textvariable=self.address_balance_var, width=85, font=("Arial", 9), borderwidth=2, relief="raised")
        self.entry_balance['validatecommand'] = (self.entry_balance.register(self.val_addr),'%P','%d')
        self.entry_balance.pack(pady=2)
        self.balance_button = tk.Button(self.root, text= "Check Bitcoin Address Balance", fg="black", bg='gray', height=1, width=40, font=("Arial", 10, 'bold'), command=self.show_delete_balance) 
        self.balance_button.bind("<Enter>", lambda event, h=self.balance_button : h.configure(bg="white"))
        self.balance_button.bind("<Leave>", lambda event, h=self.balance_button : h.configure(bg="gray"))
        self.balance_button.pack(pady=2)
        self.text_balance = tk.Text(self.root, bg='#8fbc8f', height=2, width=80, fg="black", font=("Arial", 11))
        self.text_balance.bind("<Key>", lambda e: "break")
        self.text_balance.bind("<Button-1>", self.disable_click_balance)
        self.text_balance.pack(pady=2)

    # Def StringVar
    def var(self):
        self.addr_bal_var = self.address_balance_var.get()
        self.reci_addr_var = self.recipient_address_var.get()
        self.reci_amo_var = self.recipient_amount_var.get()
        self.miner_var = self.miner_fee_var.get()
        self.send_addr_var = self.sender_address_var.get()
        self.sendk_var = self.sender_key_var.get()
        return self.addr_bal_var, self.reci_addr_var, self.reci_amo_var, self.miner_var, self.send_addr_var, self.sendk_var 

       
    # Def FAQ
    def faq_window(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.win_faq = tk.Toplevel(self.root)
        self.win_width = 1000 
        self.win_height = 600
        self.x = (self.screen_width // 2) - (self.win_width // 2)
        self.y = (self.screen_height // 2) - (self.win_height // 2)
        self.win_faq.geometry(f"{self.win_width}x{self.win_height}+{self.x}+{self.y}")
        self.v = tk.Scrollbar(self.win_faq, orient='vertical')
        self.v.pack(side='right', fill='y')        
        self.text_faq = tk.Text(self.win_faq, wrap=WORD, width=115, height=32, font=("Arial", 11), yscrollcommand=self.v.set, )
        self.text_faq.insert(tk.END, 'Frequently Asked Questions(FAQ)\n\nWhat is new with this Bitcoin Payment Service?\n\nBitcoin Payment Service aims to be your very own payment service, attaining the goal of Peer-to-Peer Electronic Cash System as envisioned by Satoshi Nakamoto.\n\nIn the Bitcoin white paper written by Nakamoto, Peer-to-Peer Electronic Cash System is described as allowing online payments to be sent directly from one party to another without going through a financial institution.\n\nThis payment service does not aim to be a financial institution. Rather, this payment service aims to be a means for ordinary folks to send bitcoin, whether as payment or donation, to one another, that is, without an intermediary financial institution.\n\nSpecifically, this payment service will allow ordinary folks to:\n1. Create bitcoin addresses\n2. Check bitcoin address balance using an in-built blockchain explorer\n3. Receive bitcoin\n4. Send bitcoin\n5. Communicate regarding the received or sent satoshis within the Bitcoin blockchain\n\nUnknown to many, Nakamoto built within the Bitcoin infrastracture a means for senders and receivers to communicate with each other. Nakamoto also built within the Bitcoin infrastracture smart contracts. These in-built communication system and smart contracts within the Bitcoin blockchain will be put into use in this novel Bitcoin Payment System.\n\nThis Bitcoin Payment System is a work in progress.')  
        self.text_faq.config(state=tk.DISABLED)
        self.text_faq.pack(padx=5, pady=5)

    
    # Def Terms
    def terms(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.win_faq = tk.Toplevel(self.root)
        self.win_width = 850 
        self.win_height = 450
        self.x = (self.screen_width // 2) - (self.win_width // 2)
        self.y = (self.screen_height // 2) - (self.win_height // 2)
        self.win_faq.geometry(f"{self.win_width}x{self.win_height}+{self.x}+{self.y}")
        self.v = tk.Scrollbar(self.win_faq, orient='vertical')
        self.v.pack(side='right', fill='y')        
        self.text_faq = tk.Text(self.win_faq, wrap=WORD, width=115, height=32, font=("Arial", 11), yscrollcommand=self.v.set, )
        self.text_faq.insert(tk.END, 'Terms of Service\n\nBY USING THIS BITCOIN PAYMENT SERVICE, YOU AGREE THAT YOU WILL NOT USE THIS SERVICE TO COMMIT ILLEGAL ACTIVITIES WITHIN AND OUTSIDE YOUR GEOGRAPHICAL LOCATION.\n\n\n\nPrivacy Policy\n\nBitcoin Payment Service respects your privacy. It doesn’t access, collect, or transmit any information (data that could be used to identify a person). As a user of this service, you have full control over your bitcoin address and private key. What this means is that you are fully responsible for securing your bitcoin address and private key and you have full control over your bitcoin funds.')  
        self.text_faq.config(state=tk.DISABLED)
        self.text_faq.pack(padx=5, pady=5)


    # Def Donate
    def donate(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.win_faq = tk.Toplevel(self.root)
        self.win_width = 750 
        self.win_height = 350
        self.x = (self.screen_width // 2) - (self.win_width // 2)
        self.y = (self.screen_height // 2) - (self.win_height // 2)
        self.win_faq.geometry(f"{self.win_width}x{self.win_height}+{self.x}+{self.y}")
        self.v = tk.Scrollbar(self.win_faq, orient='vertical')
        self.v.pack(side='right', fill='y')        
        self.text_faq = tk.Text(self.win_faq, wrap=WORD, width=115, height=32, font=("Arial", 11), yscrollcommand=self.v.set, )
        self.text_faq.insert(tk.END, 'Support This Bitcoin Payment Service\n\nSupport this endeavor through Github Sponsor program or via bitcoin donation:\n3BfxW1jEHK572XVG7NG62WM4By6fF8P8Yh\nor\nbc1p63fyummqja06a3gyvw6r4khw8puw02p7fxd5wyysmgnmsm47cz0sa363pj')  
        self.text_faq.config(state=tk.DISABLED)
        self.text_faq.pack(padx=5, pady=5)


    # Def Key + Address
    def disable_click_master(self, event):
        if not self.text_key_address.get("1.0", "end-1c"): 
            return "break"
    

    def key_address(self): 
        #addr, priv, tweaked_pub_x = master.iden()
        #self.content_key_address = f'New Bitcoin Address: {addr} \nNew Bitcoin Private Key: {priv}\n' 
        return self.content_key_address 

    
    #def key_dis_but(self, button, delay):
        #self.key_button.config(state='disabled')
        #self.root.after(delay*1000, self.key_enab_but)


    def key_enab_but(self):
        self.key_button.config(state='normal')


    def delete_keyadd(self):
        self.text_key_address.delete('1.0','end')


    def show_delete_keyadd(self):
        #self.key_add = self.key_address()
        #self.disable_button = self.key_dis_but(self.key_button, 3)
        self.text_key_address.tag_configure("center", justify='center')  
        #self.text_key_address.insert(tk.INSERT, self.key_add)
        self.text_key_address.tag_add("center", "1.0", "end")
        self.text_key_address.after(3000, self.delete_keyadd)    
        self.key_button.update()


    # Def Balance
    def disable_click_balance(self, event):
        if not self.text_balance.get("1.0", "end-1c"): 
            return "break" 
    
    
    def balance(self):
        try: 
            self.url = f'https://blockstream.info/testnet/api/address/{self.address_balance_var.get()}' # For now Blockstream is used in the absence of the in-built blockchain explorer 
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
        

    def delete_entry_balance(self):
        self.entry_balance.delete(0, tk.END)


    def delete_text_balance(self):
        self.text_balance.delete('1.0','end')


    def show_delete_balance(self):
        self.balance_def = self.balance()    
        self.balance_button.config(state="disabled")
        self.text_balance.tag_configure("center", justify='center')
        self.text_balance.insert(tk.INSERT, self.balance_def)
        self.text_balance.tag_add("center", "1.0", "end")
        self.text_balance.after(5000, self.delete_text_balance)    
        self.entry_balance.after(5000, self.delete_entry_balance)
        self.balance_button.update()
        self.enable = self.balance_button.config(state="normal")
        self.text_balance.after(5001, self.enable)


    # Def Send
    def disable_click_send(self, event):
        if not self.text_send.get("1.0", "end-1c"): 
            return "break"


    def val_addr(self, value, inp_typ):    
        if inp_typ == '1':
            value_len = len(value)
            if value_len > 62:
                return False  
            if not value.isalnum():
                return False
        return True


    def val_k(self, value, inp_typ):    
        if inp_typ == '1':
            value_len = len(value)
            if value_len > 64:
                return False  
            if not value.isalnum():
                return False
        return True


    def val_deci(self, P, inp_typ):
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

 
    def update_pbar(self):
        pass
   

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Bitcoin Payment Service -- Testnet Version. Copyright © 2024 Ellen Red')
    root.state('zoomed')
    root.config(bg='#8fbc8f')
    top = tk.Frame(root)
    top.pack(side=tk.TOP) 
    app = Home(root)
    root.mainloop()
    

