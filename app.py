r"""
___  ____  _____   ____  _____ ____ _ __ _____
\  \/ (__)/  ___)_/    \/  _  )    | |  | ____)
 \    |  |  |(_  _) () |     (  () | |  |___  \
  \   |__|____   |\____|__|\  \____|____|      )
   \_/        `--'          `--'         \____/
        P  R  o  G  R  A  M  M  i  N  G
<========================================[KCS]=>
  Developer: Ken C. Soukup
  Project  : Flask Hello World Image
  Purpose  : A very simple web app to use for research and development
<=================================[10/21/2025]=>

  Updated 10/25/2025 -- Ken C. Soukup
    . Version bump: 1.1
    . Added comprehensive server, client, and request information display
    . Server info: Container ID, Python/Flask versions
    . Client info: IP address, X-Forwarded-For, User-Agent
    . Request info: HTTP method and protocol
    . Enhanced HTML template with organized sections
    . Fixed Pylance type checking error for sys.stdout.reconfigure

  Updated 10/21/2025 -- Ken C. Soukup
    . Version bump: 1.0
    . Initial development

"""

__project__ = "Flask Hello World Image"
__version__ = "1.1"
__author__ = "Ken C. Soukup"
__company__ = "Vigorous Programming"
__minted__ = "2025"

from flask import Flask, render_template_string, request, __version__ as flask_version
import socket
from datetime import datetime
import logging
import time
import sys

# Configure logging to match gunicorn format with immediate flush
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
# Force unbuffered output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
logger = logging.getLogger(__name__)

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask Hello World</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 800px;
        }
        h2 { color: #333; margin-bottom: 20px; }
        h3 { color: #555; margin-top: 20px; margin-bottom: 10px; font-size: 1.1em; border-bottom: 2px solid #f0f0f0; padding-bottom: 5px; }
        .info { margin: 8px 0; }
        .label { font-weight: bold; color: #666; min-width: 150px; display: inline-block; }
        .value { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Hello World!</h2>

        <h3>Server Information</h3>
        <div class="info"><span class="label">Hostname:</span> <span class="value">{{ hostname }}</span></div>
        <div class="info"><span class="label">Container ID:</span> <span class="value">{{ container_id }}</span></div>
        <div class="info"><span class="label">IP Address:</span> <span class="value">{{ ip_address }}</span></div>
        <div class="info"><span class="label">Python Version:</span> <span class="value">{{ python_version }}</span></div>
        <div class="info"><span class="label">Flask Version:</span> <span class="value">{{ flask_version }}</span></div>
        <div class="info"><span class="label">Date/Time:</span> <span class="value">{{ current_time }}</span></div>

        <h3>Client Information</h3>
        <div class="info"><span class="label">Your IP:</span> <span class="value">{{ client_ip }}</span></div>
        <div class="info"><span class="label">X-Forwarded-For:</span> <span class="value">{{ x_forwarded_for }}</span></div>
        <div class="info"><span class="label">User-Agent:</span> <span class="value">{{ user_agent }}</span></div>

        <h3>Request Information</h3>
        <div class="info"><span class="label">Method:</span> <span class="value">{{ request_method }}</span></div>
        <div class="info"><span class="label">Protocol:</span> <span class="value">{{ request_protocol }}</span></div>
    </div>
</body>
</html>
"""


def get_local_ip():
    """Get local IP address safely with timeout."""
    start = time.time()
    logger.info("Getting local IP - START")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            logger.info(
                f"Getting local IP - SUCCESS ({time.time() - start:.3f}s): {ip}"
            )
            return ip
    except Exception as e:
        logger.error(f"Getting local IP - FAILED ({time.time() - start:.3f}s): {e}")
        return "127.0.0.1"


@app.before_request
def before_request():
    logger.info(
        f"BEFORE_REQUEST - Method: {request.method}, Path: {request.path}, Remote: {request.remote_addr}"
    )


@app.after_request
def after_request(response):
    logger.info(
        f"AFTER_REQUEST - Status: {response.status_code}, Remote: {request.remote_addr}"
    )
    return response


@app.teardown_request
def teardown_request(exception=None):
    if exception:
        logger.error(f"TEARDOWN_REQUEST - Exception: {exception}")
    else:
        logger.info(f"TEARDOWN_REQUEST - Clean teardown for {request.remote_addr}")


@app.route("/")
def hello_world():
    start = time.time()
    logger.info(f"ROUTE_START - Request from {request.remote_addr}")

    logger.info("Getting hostname - START")
    hostname = socket.gethostname()
    logger.info(f"Getting hostname - SUCCESS ({time.time() - start:.3f}s): {hostname}")

    # Container ID is typically the first 12 chars of hostname in Docker
    container_id = hostname[:12] if len(hostname) >= 12 else hostname

    ip_address = get_local_ip()

    logger.info("Formatting time - START")
    current_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    logger.info(f"Formatting time - SUCCESS ({time.time() - start:.3f}s)")

    # Get Python and Flask versions
    python_version = sys.version.split()[0]
    flask_ver = flask_version

    # Get client information
    user_agent = request.headers.get("User-Agent", "Unknown")
    x_forwarded_for = request.headers.get("X-Forwarded-For", "Not proxied")

    # Get request information
    request_method = request.method
    request_protocol = request.environ.get("SERVER_PROTOCOL", "Unknown")

    logger.info("Rendering template - START")
    response = render_template_string(
        HTML_TEMPLATE,
        hostname=hostname,
        container_id=container_id,
        ip_address=ip_address,
        current_time=current_time,
        python_version=python_version,
        flask_version=flask_ver,
        client_ip=request.remote_addr,
        user_agent=user_agent,
        x_forwarded_for=x_forwarded_for,
        request_method=request_method,
        request_protocol=request_protocol,
    )
    logger.info(f"ROUTE_END - Request complete ({time.time() - start:.3f}s)")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
