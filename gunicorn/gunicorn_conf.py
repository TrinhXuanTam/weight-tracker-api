import multiprocessing
import os

# Fetch configuration values from environment variables, with sensible defaults.
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "9000")
bind_env = os.getenv("BIND", None)

# Determine the binding address and port. If `BIND` is set, use it directly.
use_bind = bind_env if bind_env else f"{host}:{port}"

# Set the number of workers per core and maximum workers.
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

# Count the available CPU cores and calculate workers per core.
cores = multiprocessing.cpu_count()
workers_per_core = int(workers_per_core_str)
default_web_concurrency = workers_per_core * cores + 1

# Calculate the desired web concurrency based on environment variables or defaults.
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if max_workers_str:
        use_max_workers = int(max_workers_str)
        web_concurrency = min(web_concurrency, use_max_workers)

# Retrieve additional configuration parameters from environment variables.
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")
use_loglevel = os.getenv("LOG_LEVEL", "info")

# Gunicorn configuration variables
loglevel = use_loglevel  # Logging level for Gunicorn
workers = web_concurrency  # Number of worker processes to handle requests

# Temporary directory for Gunicorn workers
worker_tmp_dir = "/dev/shm"
# Time allowed for graceful termination of workers
graceful_timeout = int(graceful_timeout_str)
# Hard timeout for worker responses
timeout = int(timeout_str)
# HTTP Keep-Alive timeout for client connections
keepalive = int(keepalive_str)
# Logging configuration file path
logconfig = os.getenv("LOG_CONFIG", "/src/logging_production.ini")