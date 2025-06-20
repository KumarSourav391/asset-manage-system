# Asset Manage System

This project is a simple **Flask REST API** to manage assets with:
- **Service Time** (when maintenance is due)
- **Expiration Time** (when the asset is no longer valid)

The system:
- Sends reminders **15 minutes before** service or expiration.
- Logs **notifications**.
- Logs **violations** if the asset is not serviced on time or is expired.
- Uses **SQLite** and a manual `/run-checks` endpoint instead of Celery.

---
## Features
- Create, update, get assets
- Automatic reminders and violations
- SQLite storage
- Unit tests with pytest

---

## ⚙️ Setup

```bash
# 1️⃣ Clone the repo
git clone https://github.com/KumarSourav391/asset-manage-system.git
cd asset-manage-system

# 2️⃣ Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate    

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the server
python app.py

```
## Run Tests

```bash
pytest test/test_assets.py
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | /api/assets | Create asset |
| GET | /api/assets | Get all assets |
| PATCH | /api/assets/<id> | Update asset |
| POST | /api/run-checks | Run reminders & violations |
