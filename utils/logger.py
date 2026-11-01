
from datetime import datetime
from functools import wraps
import json
import os

transaction_logs = []


def log_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            result = func(*args, **kwargs)

            status = "completed"
            if isinstance(result, dict) and not result.get("success", True):
                status = "failed"

            entry = {
                "function": func.__name__,
                "timestamp": timestamp,
                "status": status
            }

            transaction_logs.append(entry)
            _write_log(entry)
            return result

        except Exception as error:
            entry = {
                "function": func.__name__,
                "timestamp": timestamp,
                "status": "failed",
                "error": str(error)
            }

            transaction_logs.append(entry)
            _write_log(entry)
            raise

    return wrapper


def _write_log(entry):
    os.makedirs("logs", exist_ok=True)

    with open("logs/transactions.jsonl", "a") as log_file:
        log_file.write(json.dumps(entry) + "\n")


def get_audit_summary(logs):
    completed = sum(
        1 for entry in logs if entry["status"] == "completed"
    )
    failed = sum(
        1 for entry in logs if entry["status"] == "failed"
    )

    return {
        "total_transactions": len(logs),
        "completed": completed,
        "failed": failed
    }
