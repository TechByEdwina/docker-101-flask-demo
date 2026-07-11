# ============================================================
# Docker Teaching Demo - Flask App
# ------------------------------------------------------------
# Environment variables:
#
#   APP_GREETING  - The greeting/app name shown on the page.
#                   Change this at runtime to show students how
#                   the same image can behave differently:
#                   docker run -e APP_GREETING="Hello, Room 101!"
#                   Default: "Hello from Docker!"
#
#   PORT          - The port Flask listens on inside the container.
#                   Used to demonstrate port mapping:
#                   docker run -p 8080:8080 (or -p 9000:8080, etc.)
#                   Default: 8080
# ============================================================

import os
import json
from flask import Flask

app = Flask(__name__)

# Read configuration from environment variables
GREETING = os.environ.get("APP_GREETING", "Hello from Docker!")
PORT = int(os.environ.get("PORT", 8080))

# The counter file lives in /app/data so students can mount a
# volume there and watch the count survive container restarts:
#   docker run -v mydata:/app/data ...
COUNTER_FILE = "/app/data/counter.json"


def read_count():
    """Read the current visit count from the counter file."""
    try:
        with open(COUNTER_FILE, "r") as f:
            data = json.load(f)
            return data.get("count", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def write_count(count):
    """Write the updated visit count back to the counter file."""
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)


@app.route("/")
def index():
    # Increment and persist the visit counter
    count = read_count() + 1
    write_count(count)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Docker Demo</title>
    <style>
        body  {{ font-family: monospace; font-size: 1.3em;
                 max-width: 600px; margin: 80px auto; padding: 0 20px; }}
        h1    {{ font-size: 2em; }}
        .label {{ color: #555; }}
        .value {{ font-weight: bold; }}
    </style>
</head>
<body>
    <h1>{GREETING}</h1>
    <p><span class="label">Listening on port: </span>
       <span class="value">{PORT}</span></p>
    <p><span class="label">Visit count: </span>
       <span class="value">{count}</span></p>
    <hr>
    <small>
        Counter file: {COUNTER_FILE}<br>
        Mount a volume to persist the count across container restarts.
    </small>
</body>
</html>
"""
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
