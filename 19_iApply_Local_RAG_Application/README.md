Here are both complete documents, ready to copy and deploy.

---

## **DOCUMENT 1: iApply `README.md`**

Replace the entire contents of `/mnt/c/Users/rduck/Iapply/README.md` with:

````markdown
# iApply

> AI-powered LinkedIn job application assistant. Runs 100% on your local machine.

Built by **[Aspida Security](https://github.com/aspida-security)**.

---

## What It Does

iApply automates LinkedIn Easy Apply forms using your resume vault and a locally-stored learned memory system. The more it runs, the smarter it gets  -  new questions are answered by AI and saved locally so they are never sent to the LLM again.

- Fills every Easy Apply field automatically
- Matches the best resume from your vault to each job description
- Learns your answers over time  -  zero repeated API calls for known questions
- Never stores or transmits your LinkedIn password
- Runs a local HUD showing every action in real time
- Built-in anti-detection: human keystroke timing, randomized pacing, daily caps

---

## Requirements

| Requirement   | Version                                              |
| ------------- | ---------------------------------------------------- |
| Python        | 3.11+                                                |
| Google Chrome | Latest stable                                        |
| OS            | Windows 10/11, macOS 13+, Ubuntu 22.04+              |
| Groq API Key  | Free at [console.groq.com](https://console.groq.com) |

---

## Quick Start

### Windows

```bash
Double-click start.bat
```
````

### Mac / Linux

```bash
chmod +x start.sh && ./start.sh
```

The launcher will:

1. Create a Python virtual environment
2. Install all dependencies from `requirements.txt`
3. Run database migrations automatically
4. Start the Flask backend on `http://127.0.0.1:5000`
5. Open the UI at `http://127.0.0.1:5173`

---

## First Run  -  Onboarding Wizard

On first launch the Onboarding Wizard walks you through four steps:

1. **Create your vault passphrase**  -  encrypts all local data at rest
2. **Upload your resume(s)**  -  PDF, up to 5 files
3. **Enter your Groq API key**  -  starts with `gsk_`
4. **LinkedIn session**  -  iApply opens Chrome and waits for you to log in manually. Once detected, your session is saved and login is never required again.

iApply never sees or stores your LinkedIn password.

---

## How the Answer Pipeline Works

```
Question received
       │
       ▼
┌─────────────────────────┐
│  1. Master Profile      │  Name, email, phone  -  always correct
└──────────┬──────────────┘
           │ no match
           ▼
┌─────────────────────────┐
│  2. Memory Vault        │  Your past answers, retrieved via
│  (confidence > 80%)     │  semantic similarity (FAISS + embeddings)
└──────────┬──────────────┘
           │ not found
           ▼
┌─────────────────────────┐
│  3. AI (Groq / Llama 3) │  Answer generated, saved to vault
└─────────────────────────┘
```

After a few sessions the LLM is rarely called  -  the vault handles almost everything through local vector retrieval.

---

## Security Architecture

iApply was designed from the ground up with a security-first mindset. The following controls are implemented across every layer of the application.

### Encryption at Rest

All sensitive user data is stored in an AES-256-GCM encrypted SQLite database (`vault.db`) using `pysqlcipher3`. Encryption keys are derived from the user's passphrase using **Argon2id**  -  a memory-hard key derivation function that resists brute-force and GPU-accelerated dictionary attacks. A unique random salt is generated per installation and stored separately from the encrypted data.

| Data                | Storage Location       | Encryption                         |
| ------------------- | ---------------------- | ---------------------------------- |
| Resume text         | `data/vault/vault.db`  | AES-256-GCM (Argon2id)             |
| Learned answers     | `data/vault/vault.db`  | AES-256-GCM (Argon2id)             |
| Application history | `data/vault/vault.db`  | AES-256-GCM (Argon2id)             |
| API keys            | OS credential store    | Fernet (AES-128-CBC + HMAC-SHA256) |
| LinkedIn session    | Chrome profile (local) | Chrome-managed                     |

### Credential Handling  -  BYOS Model

iApply operates on a **Bring Your Own Session (BYOS)** model. The user logs into LinkedIn manually in a controlled Chrome profile. iApply captures and reuses the resulting session cookie  -  it never receives, processes, or stores the user's LinkedIn password at any point. This eliminates an entire credential theft attack surface.

### API Key Security

The Groq API key is stored using the OS-native credential store (`keyring` library):

- **Windows:** Windows Credential Manager (DPAPI-backed)
- **macOS:** Keychain
- **Linux:** libsecret / GNOME Keyring

Keys are never written to `.env` files, `config.yaml`, or any plaintext file on disk.

### Network Isolation

The Flask backend binds exclusively to `127.0.0.1`  -  never `0.0.0.0`. This ensures the API surface is not exposed on any network interface, preventing lateral movement or remote exploitation in shared network environments.

### LLM Prompt Injection Defense

All prompts sent to the LLM are prefixed with a **SECURITY DIRECTIVE** that instructs the model to:

- Ignore instructions embedded in job description text
- Only respond within its defined response schema
- Never output system internals, file paths, or credential data

This mitigates indirect prompt injection attacks that can occur when adversarial job descriptions attempt to hijack the AI response.

### Input Sanitization

All user-supplied inputs (resume text, form field values, passphrase hints) are sanitized before being written to the database. Parameterized queries are used throughout  -  raw string interpolation into SQL is prohibited by design.

### Anti-Fingerprinting & Rate Control

iApply implements behavioral controls to reduce automation detection risk:

- **Human keystroke timing:** Randomized inter-key delay modeled on human typing distributions
- **Randomized pacing:** Variable delay between applications (`min_delay` / `max_delay` in config)
- **Daily application caps:** Hard limit enforced in `settings.yaml` (`daily_limit`)
- **Undetected ChromeDriver:** Browser launched via `undetected-chromedriver` to suppress automation flags

---

## RAG Pipeline Design

iApply's answer retrieval system is a production Retrieval-Augmented Generation (RAG) pipeline:

1. **Document ingestion:** Resume PDFs are chunked and embedded using a local embedding model at setup time.
2. **Vector store:** Embeddings are stored in a FAISS index (`faiss-cpu`) persisted to disk alongside `vault.db`.
3. **Retrieval:** On each form question, the question text is embedded and a similarity search is run against the vault. Answers with cosine similarity above 0.80 are returned directly without calling the LLM.
4. **Generation:** Below the confidence threshold, the question + resume context is sent to Groq (Llama 3). The response is embedded and stored in the vault for future retrieval.
5. **Chain:** Built with LangChain  -  `ChatPromptTemplate → LLM → StrOutputParser`  -  with retry logic and rate-limit backoff.

---

## Data & Privacy

Nothing leaves your machine except the Groq API call. The payload contains only:

- The job description text (scraped from the current page)
- The form question being answered
- Relevant resume context (no name, email, phone, or PII)

No telemetry, analytics, or usage data is collected or transmitted.

---

## Configuration

Edit `config/settings.yaml` to adjust behavior:

```yaml
daily_limit: 50 # Max applications per day
min_delay: 30 # Minimum seconds between applications
max_delay: 120 # Maximum seconds between applications
title_blacklist: # Job titles to skip
  - "Senior"
  - "Staff"
  - "Principal"
min_experience_years: 0 # Skip jobs requiring more than X years
```

---

## Updating

```bash
git pull origin main
pip install -r requirements.txt
python run.py  # Migrations run automatically
```

---

## Support

See [SUPPORT.md](./SUPPORT.md) for troubleshooting and contact information.

- **Issues:** Open a GitHub Issue in this repo
- **Email:** [support@aspidasecurity.io](mailto:support@aspidasecurity.io)

---

## Security Policy

See [SECURITY.md](./SECURITY.md) for responsible disclosure procedures.

---

## Terms of Service

See [TERMS_OF_SERVICE.md](./TERMS_OF_SERVICE.md) for license and usage terms.

---

## License

Proprietary. See [LICENSE](./LICENSE).
© 2026 Aspida Security LLC. All rights reserved.
