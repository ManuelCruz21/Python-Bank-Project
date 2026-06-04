# 🏦 PyBank - Secure Digital Homebanking Suite

## 📄 1. README.md (System Documentation)

# 🏦 PyBank - Secure Digital Homebanking Suite

PyBank is a lightweight, cybersecure full-stack digital banking and auditing application built using Python (Flask), SQLAlchemy, and Tailwind CSS, with database persistence on Supabase (PostgreSQL). 

The platform implements strict role-based access control (RBAC), dividing functionalities between regular **Clients** (who can manage their personal accounts and transfer funds) and **Managers/Auditors** (who possess supervisor privileges to oversee the system's global health and audit transactions).

---

## 🔒 Key Security Architecture Features

* **Role-Based Access Control (RBAC):** Users are strongly decoupled upon authentication. Clients have isolated access to their financial charts, while Managers gain access to the administrative dashboard.
* **Input Sanitization & Type Safety:** Financial calculations utilize Python's `Decimal` library instead of standard floating-point numbers to strictly prevent rounding attack vulnerabilities and floating-point injection errors.
* **SIEM-Inspired Transaction Logs:** Every transactional event (Deposits, Withdrawals, Transfers) automatically generates centralized cryptographic-like timeline records stored natively in the cloud database for auditing.
* **Server-Side State Protection:** Strict session validation (`verificar_autenticacao`) checks prevent horizontal and vertical privilege escalation (Insecure Direct Object References - IDOR).

---

## 🚀 App Features

### 👤 Client Dashboard
* **Real-time Balance Monitor:** Displays current liquid assets in Euros.
* **Interactive ATM Terminal:** Perform instant virtual deposits and withdrawals with comprehensive account-limit checks.
* **Secure Wire Transfers:** Peer-to-peer digital money transfers with structural database rolling updates (Rollback on exception).
* **Personal Statement Table:** Chronological timeline showing transaction history, item descriptions, and color-coded balance impact.
* **Self-Termination Zone:** Secure option to permanently wipe personal data off the cloud cluster under compliance standards.

### 👩‍💼 Manager Audit Dashboard
* **Total Assets Custody Counter:** High-level summary displaying the absolute financial health sum of the entire banking system.
* **Active Accounts Registry:** Complete live viewport of all active client accounts, their current standing balances, and holder identifiers.
* **Exceptional Administrative Revocation:** Supervisors can manually terminate any malicious/compromised banking accounts instantly during an audit.
* **SIEM Transaction Log Monitor:** Real-time stream of all structural operations taking place across the backend network for anomaly tracking.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Flask (Microframework)
* **ORM / Database Layer:** SQLAlchemy
* **Database Cloud Host:** Supabase (Relational PostgreSQL Engine)
* **Frontend UI:** Jinja2 Templates engine styled with Tailwind CSS v3

---

## 💻 Local Installation & Setup

Follow these steps to spin up the secure bank suite environment on your local server machine:

### 1. Clone the Repository
git clone https://github.com/ManuelCruz21/Python-Bank-Project.git


### 2. Set Up a Virtual Environment & Install Dependencies

# Create the virtual environment
python -m venv .venv

# Activate the environment (Windows)
.venv\Scripts\activate

# Activate the environment (Linux/Mac)
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt


### 3. Configure Environment Variables
To run the project locally, you need to set up your local environment variables. Create a file named ".env" in the root folder of your project (this file is ignored by Git for security reasons) and add your database configuration. We used Supabase for this:


SECRET_KEY=your_local_secure_session_key
# Local development string (or use the cloud production string below)
DATABASE_URL=postgresql://postgres.wpnszvkfopsfrpxchqnz:[YOUR_SUPABASE_PASSWORD]@[aws-0-eu-central-1.pooler.supabase.com:6543/postgres?sslmode=require&prepare_threshold=0](https://aws-0-eu-central-1.pooler.supabase.com:6543/postgres?sslmode=require&prepare_threshold=0)


### 4. Run the Application Locally
Once the dependencies are installed and the .env file is configured, launch the Flask local development server by executing:

python app.py

After running the command, open your preferred web browser and navigate to: http://127.0.0.1:5000


### 5. Cloud Production Deployment (Render)
The live production environment is completely configured and hosted on Render linked to Supabase. For the online application, the environment variables were configured directly inside the Render Dashboard -> Environment Settings panel to keep production credentials safe and separate from the source code:

PYTHON_VERSION: Set to 3.11.8 to ensure absolute runtime and package compatibility.

SECRET_KEY: A high-entropy production key used to encrypt active Flask client sessions.

DATABASE_URL: Hosted secure connection string pointing to the live Supabase PostgreSQL instance using the Transaction Pooler (port 6543) with sslmode=require.

The online deployed version is the following url: https://python-bank-project-9mqy.onrender.com/