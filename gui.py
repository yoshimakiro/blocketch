import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from queue import Queue

class BlocketchGUI:
    def __init__(self, root, update_queue):
        self.root = root
        self.root.title("Blocketch Node")
        self.config_file = '/app/config/config.json'
        self.update_queue = update_queue
        self.setup_ui()
        self.load_config()
        self.start_monitor()

    def setup_ui(self):
        # Configuration Panel
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding="10")
        config_frame.grid(row=0, column=0, sticky="ew")
        
        ttk.Label(config_frame, text="IMAP Server:").grid(row=0, column=0)
        self.imap_server = ttk.Entry(config_frame)
        self.imap_server.grid(row=0, column=1)
        
        ttk.Label(config_frame, text="SMTP Server:").grid(row=1, column=0)
        self.smtp_server = ttk.Entry(config_frame)
        self.smtp_server.grid(row=1, column=1)
        
        ttk.Label(config_frame, text="Email Address:").grid(row=2, column=0)
        self.email_address = ttk.Entry(config_frame)
        self.email_address.grid(row=2, column=1)
        
        ttk.Button(config_frame, text="Save", command=self.save_config).grid(row=3, column=1)

        # Processing Monitor
        monitor_frame = ttk.LabelFrame(self.root, text="Processing Monitor", padding="10")
        monitor_frame.grid(row=1, column=0, sticky="ew")
        
        self.processing_tree = ttk.Treeview(monitor_frame, columns=('ID', 'Sender', 'Status'), show='headings')
        self.processing_tree.heading('ID', text='ID')
        self.processing_tree.heading('Sender', text='Sender')
        self.processing_tree.heading('Status', text='Status')
        self.processing_tree.grid(row=0, column=0)
        
        # System Stats
        stats_frame = ttk.LabelFrame(self.root, text="System Statistics", padding="10")
        stats_frame.grid(row=2, column=0, sticky="ew")
        
        self.processed_count = ttk.Label(stats_frame, text="Processed: 0")
        self.processed_count.grid(row=0, column=0)
        
        self.system_status = ttk.Label(stats_frame, text="Status: Running")
        self.system_status.grid(row=0, column=1)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file) as f:
                config = json.load(f)
                self.imap_server.insert(0, config.get('imap_server', ''))
                self.smtp_server.insert(0, config.get('smtp_server', ''))
                self.email_address.insert(0, config.get('email_address', ''))

    def save_config(self):
        config = {
            'imap_server': self.imap_server.get(),
            'smtp_server': self.smtp_server.get(),
            'email_address': self.email_address.get()
        }
        
        os.makedirs('/app/config', exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        
        messagebox.showinfo("Success", "Configuration saved and applied!")

    def start_monitor(self):
        def monitor_loop():
            while True:
                if not self.update_queue.empty():
                    update = self.update_queue.get()
                    self.process_update(update)
        
        from threading import Thread
        Thread(target=monitor_loop, daemon=True).start()

    def process_update(self, update):
        self.processing_tree.insert('', 'end', values=(
            update.get('id'),
            update.get('sender'),
            update.get('status')
        ))
        
        if update.get('status') == 'Processed':
            current = int(self.processed_count['text'].split(': ')[1])
            self.processed_count.config(text=f"Processed: {current + 1}")