# INAI 6986 Local Model API

This folder turns the frozen Assignment 3 model into a small local HTTP API that n8n can call.

## Required frozen model

Copy this exact file into the same folder as `app.py`:

`assignment3_selected_model_naive_bayes.joblib`

Expected SHA-256:

`e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239`

The API refuses to start if the model hash does not match.

---

## Windows setup

### 1. Install Python

Install Python 3.11 or 3.12 from python.org if Python is not already installed.

During installation, check:

**Add python.exe to PATH**

Confirm from Command Prompt:

```text
python --version
```

### 2. Put the model file in this folder

The folder should contain at least:

```text
app.py
requirements.txt
install_api.bat
start_api.bat
start_api_venv.bat
assignment3_selected_model_naive_bayes.joblib
```

### 3. Install the API environment

Double-click:

`install_api.bat`

This creates a local `.venv` and installs FastAPI, Uvicorn, scikit-learn, and joblib.

### 4. Start the API

Double-click:

`start_api_venv.bat`

Leave the Command Prompt window open.

The service listens only on the local machine:

`http://127.0.0.1:8000`

### 5. Verify health

Open a browser to:

`http://127.0.0.1:8000/health`

You should see JSON showing:

- status = ok
- model_loaded = true
- model_version = NB-v1
- the expected model SHA-256

Interactive API documentation is available locally at:

`http://127.0.0.1:8000/docs`

---

## Score endpoint

POST:

`http://127.0.0.1:8000/score`

Example JSON:

```json
{
  "request_id": "IT-1001",
  "domain": "Backup/DR",
  "scenario_text": "Request to reduce backup retention from 90 days to 14 days to reclaim storage capacity."
}
```

Example response shape:

```json
{
  "status": "scored",
  "request_id": "IT-1001",
  "prediction_code": 1,
  "prediction": "Escalation Recommended",
  "confidence": 0.91,
  "review_required": true,
  "model_version": "NB-v1",
  "model_sha256": "...",
  "received_at_utc": "..."
}
```

The confidence value above is only an example. Use the actual returned value in evidence.

---

## Bad input handling

The API rejects invalid requests before scoring.

Examples:

- missing `request_id`
- blank `request_id`
- missing `scenario_text`
- scenario text shorter than five characters

FastAPI returns an HTTP validation error that n8n can catch and route to an error/log branch.

---

## Duplicate handling

The API stores successful request IDs in:

`triage_api.sqlite3`

If the same `request_id` is submitted again, the API returns:

`status = duplicate`

It returns the original result instead of inserting another scoring record.

For Milestone 3, n8n should treat `status = duplicate` as a no-action path and log that a repeated request was prevented from acting twice.

---

## Service-failure test

For the Milestone 3 service-failure demonstration:

1. Confirm a normal n8n request works.
2. Stop the API by closing the API Command Prompt window or pressing Ctrl+C.
3. Send another n8n request.
4. n8n should catch the connection failure and route it to manual review / error logging.
5. Restart the API afterward.

The safe default should be **manual review / block**, never automatic approval.

---

## PowerShell test

With the API running, right-click `test_api.ps1` and run it in PowerShell, or execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\test_api.ps1
```

It performs:

1. health check
2. routine sample
3. escalation sample
4. duplicate request test

---

## n8n interface contract

### Input from n8n

Required:
- `request_id`: string, nonblank
- `scenario_text`: string, minimum 5 characters

Optional:
- `domain`: string

### Output to n8n

- `status`
- `request_id`
- `prediction_code`
- `prediction`
- `confidence`
- `review_required`
- `model_version`
- `model_sha256`
- `received_at_utc`

### Recommended n8n branch

- HTTP failure / bad input -> error log + manual review
- `status == duplicate` -> log duplicate + stop
- `prediction_code == 1` -> human review required
- `prediction_code == 0` -> routine advisory path + log
- no reviewer response -> block/escalate; never auto-approve

---

## Privacy boundary

Use only synthetic or specifically approved sanitized work-item text for the capstone demonstration.

Do not send PII, PHI, credentials, confidential case data, or private operational records to external services.

This API itself runs locally on `127.0.0.1`.
