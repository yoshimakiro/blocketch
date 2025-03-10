import os
import asyncio
import uuid
import hashlib
import smtplib
from email.message import EmailMessage
from aiosmtpd.controller import Controller
from pqcrypto.sign.dilithium2 import generate_keypair, sign
from opentimestamps.core.op import OpSHA256
from opentimestamps.core.timestamp import DetachedTimestampFile
from opentimestamps.client import OpenTimestampsClient
from threading import Thread
from queue import Queue

class EmailHandler:
    def __init__(self, gui_queue):
        self.gui_queue = gui_queue
        self.ots_client = OpenTimestampsClient()
        self.ots_client.add_calendar('https://btc.calendar.opentimestamps.org')
    
    async def handle_DATA(self, server, session, envelope):
        email_id = str(uuid.uuid4())
        self.gui_queue.put({
            'id': email_id,
            'sender': envelope.mail_from,
            'status': 'Received'
        })
        
        try:
            email_content = envelope.content.decode('utf8')
            self.gui_queue.put({
                'id': email_id,
                'sender': envelope.mail_from,
                'status': 'Processing'
            })
            
            proof = await self.process_email(email_content)
            await self.send_confirmation(envelope.mail_from, proof)
            
            self.gui_queue.put({
                'id': email_id,
                'sender': envelope.mail_from,
                'status': 'Processed'
            })
            return '250 Timestamp scheduled'
        except Exception as e:
            self.gui_queue.put({
                'id': email_id,
                'sender': envelope.mail_from,
                'status': f'Error: {str(e)}'
            })
            return f'451 Error: {str(e)}'

    async def process_email(self, content):
        pqc_hash = self.pqc_hash_content(content)
        detached_ts = DetachedTimestampFile(OpSHA256(), pqc_hash)
        stamped_ts = await self.ots_client.stamp(detached_ts)
        
        proof_path = f"/app/timestamps/{pqc_hash.hex()}.ots"
        with open(proof_path, 'wb') as f:
            stamped_ts.serialize(f)
        
        return proof_path

    def pqc_hash_content(self, content):
        _, secret_key = generate_keypair()
        signature = sign(secret_key, content.encode())
        return hashlib.sha3_256(signature).digest()

    async def send_confirmation(self, sender, proof_path):
        msg = EmailMessage()
        msg['From'] = 'timestamp@blocketch.example'
        msg['To'] = sender
        msg['Subject'] = 'Your Timestamp Proof'
        
        with open(proof_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='proof.ots')
        
        with smtplib.SMTP('localhost') as s:
            s.send_message(msg)

def start_smtp_server(gui_queue):
    controller = Controller(EmailHandler(gui_queue), hostname='0.0.0.0', port=2525)
    controller.start()
    return controller

if __name__ == '__main__':
    from gui import BlocketchGUI
    import tkinter as tk
    from threading import Thread
    from queue import Queue

    # Start GUI
    gui_queue = Queue()
    root = tk.Tk()
    gui = BlocketchGUI(root, gui_queue)
    
    # Start SMTP server in a separate thread
    smtp_thread = Thread(target=start_smtp_server, args=(gui_queue,), daemon=True)
    smtp_thread.start()
    
    # Run GUI main loop
    root.mainloop()