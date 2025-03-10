# Blocketch: Email Timestamping on Bitcoin via OpenTimestamps, in a trust minimized, quantum resilienct, and privacy focus manner.

Blocketch is a free, open-source service that timestamps emails using Bitcoin's blockchain through the OpenTimestamps (OTS) protocol. No signup or registration or fees(opional) required. Just send an email to the service, and receive a cryptographic proof of existence anchored to Bitcoin’s immutable ledger. Ideal for legal proofs, archival records, or securing intellectual property.



## Features
- **Simple Email Timestamping**: Send an email, get a timestamp proof—no accounts needed.
- **Bitcoin Anchoring via OpenTimestamps**: Leverages OTS to embed timestamps in Bitcoin transactions efficiently.
- **Tkinter GUI**: Monitor email processing and configure IMAP/SMTP settings with a user-friendly interface.
- **Dockerized Deployment**: Easy to set up and run with Docker, supporting both GUI and CLI modes.
- **Preliminary Post-Quantum Hashing**: Optional use of post-quantum cryptography (Dilithium2) for future-proofing (configurable).

---

## Status
This is a preliminary implementation with working code for email ingestion, timestamping, and proof delivery. It’s functional but rough around the edges—we’re looking for collaborators to help polish, secure, and scale it. Current version handles:
- Receiving emails via `aiosmtpd` on port `2525`.
- Hashing and timestamping email content using OpenTimestamps.
- Saving emails (`/app/emails`) and proofs (`/app/timestamps`).
- Sending confirmation emails with `.ots` proof files.
- Monitoring via a Tkinter GUI or CLI output.

---

## How to Run
Follow these steps to set up and test Blocketch locally.

### Prerequisites
- **Docker** (for containerized setup).
- **Python 3.10+** (if running directly).
- An **SMTP server** for sending confirmation emails (e.g., Gmail, SendGrid).
- For **GUI mode**: A display environment (e.g., X11 forwarding on Linux).

---

### Directory Structure
blocketch/
├── Dockerfile
├── requirements.txt
├── main.py
├── gui.py
├── config/
│ └── config.json
├── timestamps/
├── emails/
├── .env
└── README.md



---

### Build the Docker Image
```bash
docker build -t blocketch .
Run the Container
GUI Mode (requires display setup)
For Linux with X11 forwarding or a local display:


```
```bash
docker run -it -p 2525:2525 \
  -v ./config:/app/config \
  -v ./timestamps:/app/timestamps \
  -v ./emails:/app/emails \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  blocketch
```
On macOS/Windows, you may need a VNC viewer or XQuartz setup—see Troubleshooting for details.

CLI Mode (headless, no GUI required)
```bash
Copy
docker run -it -p 2525:2525 \
  -v ./config:/app/config \
  -v ./timestamps:/app/timestamps \
  -v ./emails:/app/emails \
  blocketch --no-gui
```
Configure the System
GUI Mode: The Tkinter GUI will launch automatically. Enter your IMAP/SMTP details and email address, then click "Save".

CLI Mode: Configure SMTP settings in .env:
```
plaintext
Copy
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
EMAIL_FROM=timestamp@blocketch.example
```
Ensure port 2525 is accessible for incoming emails.

Test the System
Send an email to the configured address (e.g., localhost:2525 if testing locally).

Example: Use a mail client or CLI tool like swaks:


```bash
swaks --to test@example.com --from your-email@example.com --server localhost:2525
```
Watch the GUI (GUI mode) or logs (CLI mode) for processing updates.

Check /app/emails for saved .eml files and /app/timestamps for .ots proof files.

You’ll receive a confirmation email with the .ots proof attached (if SMTP is configured).

Collaboration Opportunities
Blocketch is in its early stages, and we’re looking for contributors to help take it to the next level. As a contributor (not inventor) with 10+ years as a CTO/co-founder in tech projects, I’m excited to collaborate with others who share a passion for trust-minimized systems and practical Bitcoin applications.

What We Need
Bitcoin Devs: Optimize OpenTimestamps integration, reduce latency, or explore direct Bitcoin transaction embedding.

Security Experts: Harden the email pipeline (rate-limiting, spam prevention, input validation).

UI/UX Folks: Enhance the Tkinter GUI or build a web interface for broader accessibility.

Legal/Archival Tech Enthusiasts: Explore use cases (e.g., legal proofs, IP protection) and integrations.

Documentation Writers: Improve setup guides, add tutorials, or create demo videos.

Why Collaborate?
Practical Bitcoin Use Case: Blocketch shows how Bitcoin’s immutability can solve real-world problems without chain bloat.

Low Barrier to Entry: Small codebase, Dockerized setup—easy to jump in and experiment.

Future-Proofing: Optional post-quantum cryptography opens doors for innovation.

Community-Driven: Open to ideas—let’s shape this together!

Contribute: Fork this repo, submit a PR, or open an issue with ideas.

Current Limitations
This is a preliminary implementation—expect some rough edges. Known areas to improve:

SMTP Setup: Confirmation emails assume a local SMTP server; needs better configuration (e.g., .env support).

Security: Email pipeline lacks rate-limiting and spam protection—vulnerable to abuse.

GUI Display: Tkinter GUI requires a display; headless setups need CLI mode or web UI.

Scalability: No cleanup for old files in /app/emails or /app/timestamps—could fill disk over time.

Verification: Users can’t easily verify .ots proofs without external tools—needs in-app support.

Security Notes
The email server (aiosmtpd) listens on port 2525 without authentication. Deploy with caution (e.g., behind a firewall) until rate-limiting and spam protection are added.

Post-quantum hashing (Dilithium2) is included but optional—currently overkill for OTS, which uses SHA-256. Future versions may use it for proof signing.

Always audit dependencies and review code before deploying in production.

Dependencies
See requirements.txt for the full list:

aiosmtpd==1.4.4.post2: SMTP server for email ingestion.

opentimestamps==0.4.5: Timestamping via Bitcoin.

pqcrypto==0.2.1: Post-quantum cryptography (optional).

python-dotenv==0.19.0: Environment variable management.

aiohttp==3.8.1: Async HTTP requests.

email-validator==1.3.0: Email address validation.

Troubleshooting
GUI Not Displaying: If the Tkinter GUI fails to launch (e.g., “no display” error), ensure X11 forwarding is set up or use --no-gui mode.

On Linux: Ensure $DISPLAY is set and /tmp/.X11-unix is mounted.

On macOS/Windows: Use XQuartz or a VNC viewer.

SMTP Errors: If confirmation emails fail, check .env settings or ensure a local SMTP relay is running.

OTS Failures: If timestamping fails, verify the OTS calendar (btc.calendar.opentimestamps.org) is reachable. Additional calendars can be added in main.py.


Acknowledgments

OpenTimestamps team for their awesome protocol.

Contributors to the Bitcoin ecosystem for enabling trust-minimized solutions.



Contact Information
For any queries or support, c
ontact us here on GitHub or me at yoshimakiro@proton.me.



---

### How to Use
1. Copy the entire content above.
2. Paste it into your `README.md` file.
3. Commit and push the changes to your repository.

Let me know if you need further adjustments! 
