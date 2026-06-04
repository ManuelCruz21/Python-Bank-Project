# 🏦 ApexTrust - Secure Digital Homebanking Suite

## 📄 1. README.md (System Documentation)

```markdown
# 🏦 ApexTrust - Secure Digital Homebanking Suite

ApexTrust is a lightweight, cybersecure full-stack digital banking and auditing application built using Python (Flask), SQLAlchemy, and Tailwind CSS, with database persistence on Supabase (PostgreSQL). 

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
```bash
git clone https://github.com/ManuelCruz21/Python-Bank-Project.git
```



