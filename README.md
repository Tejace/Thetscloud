[README.md](https://github.com/user-attachments/files/34217240/README.md)
# Thetscloud# Thetscloud

A self-hosted, multi-user cloud storage app built with FastAPI and MySQL. Users register and log in, then upload and download their own files through a simple web interface, while the owner controls the storage on their own hardware (for example, a Raspberry Pi with an SSD).

## Features

- **Multi-user registration and login** with token-based authentication (JWT)
- **Password hashing** with Argon2
- **Per-user file storage** with uploads kept on disk and tracked in the database
- **Task management** linked to users and files
- **Email support** for account-related messages (via `fastapi-mail`)
- **Database migrations** with Alembic
- **Simple static front end** served by the app itself
- **Interactive API docs** generated automatically by FastAPI at `/docs`

## Tech stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI, served by Uvicorn |
| Database | MySQL / MariaDB via SQLAlchemy and PyMySQL |
| Migrations | Alembic |
| Auth | PyJWT, Argon2 (`pwdlib` / `argon2-cffi`) |
| Mail | fastapi-mail |
| Front end | Static HTML in `static/` |

## Project structure

```
Thetscloud/
├── app.py                # FastAPI entry point, router registration
├── alembic.ini           # Alembic configuration
├── migrations/           # Database migrations
├── requirements.txt
├── .env.example          # Template for your environment variables
├── static/
│   └── index.html        # Front end
└── src/
    ├── user/             # Registration, login, user models
    ├── tasks/            # Task routes, models, schemas
    ├── files/            # Upload / download routes and models
    └── utils/            # DB setup, settings, helpers, mail, constants
```

## Getting started

### Requirements

- Python 3.10 or newer
- MySQL or MariaDB
- Optional: a Raspberry Pi or other always-on machine, and a Tailscale account if you want to expose the app publicly (see below)

### 1. Clone and install

```bash
git clone https://github.com/Tejace/Thetscloud.git
cd Thetscloud
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create the database

```sql
CREATE DATABASE thetscloud CHARACTER SET utf8mb4;
CREATE USER 'thetscloud'@'localhost' IDENTIFIED BY 'choose-a-strong-password';
GRANT ALL PRIVILEGES ON thetscloud.* TO 'thetscloud'@'localhost';
FLUSH PRIVILEGES;
```

Use a dedicated database user rather than `root`, and keep MySQL bound to `127.0.0.1`.

### 3. Configure environment variables

Copy the template and fill it in:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `DB_CONNECTION` | SQLAlchemy URL, e.g. `mysql+pymysql://thetscloud:password@127.0.0.1/thetscloud` |
| `SECRET_KEY` | Long random string used to sign tokens. Generate one with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | JWT signing algorithm, e.g. `HS256` |
| `TOKEN_EXPIRY_TIME` | Token lifetime in minutes |
| `UPLOAD_DIR` | Where uploaded files are stored, e.g. `storage/uploads` |
| `MAIL_PASS` | Password for the outgoing mail account |

Never commit `.env`. It is listed in `.gitignore`.

### 4. Create the tables

On first start the app creates the tables automatically. To keep Alembic in sync afterwards, mark the database as up to date:

```bash
alembic stamp head
```

For later schema changes, use:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

### 5. Run it

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000> for the interface and <http://127.0.0.1:8000/docs> for the API documentation.

Binding to `127.0.0.1` keeps the app reachable only from the machine itself, which is what you want when it sits behind a tunnel or reverse proxy.

## Exposing it to the internet

If your ISP uses CGNAT or blocks inbound connections, you can publish the app without port forwarding using [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel):

```bash
sudo tailscale up
sudo tailscale funnel --bg 8000
tailscale funnel status
```

Funnel gives you a public HTTPS address on your `ts.net` domain. Anyone with the URL can reach the app, so your own authentication is what protects it.

Alternatives include Cloudflare Tunnel (needs a domain) or a small VPS relaying to your machine over WireGuard.

## Running as a service (Linux)

Create `/etc/systemd/system/thetscloud.service`:

```ini
[Unit]
Description=Thetscloud
After=network.target mysql.service

[Service]
User=thetscloud
WorkingDirectory=/home/thetscloud/Thetscloud
EnvironmentFile=/home/thetscloud/Thetscloud/.env
ExecStart=/home/thetscloud/Thetscloud/venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now thetscloud
```

## Security notes

- Keep secrets only in `.env`, never in code or the repository.
- Run the app and database as unprivileged users, and give the app a database user limited to its own database.
- Keep the upload directory outside the web root, and back it up somewhere other than the device it lives on.
- If you expose the app publicly, use HTTPS only (Funnel and Cloudflare Tunnel both provide this) and keep dependencies updated.
- Review file size limits and user quotas before inviting other people.

## Roadmap

- [ ] Two-factor authentication (TOTP)
- [ ] Per-user storage quotas
- [ ] Rate limiting on login attempts
- [ ] Tests and CI

## License

Add a license file (for example MIT) to state how others may use this code.

Locally served cloud Storage app with security controls, IAM and multiuser registration 
