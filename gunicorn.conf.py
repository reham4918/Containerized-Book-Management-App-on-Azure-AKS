# Gunicorn configuration file
import multiprocessing
max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "0.0.0.0:5000"
workers = (multiprocessing.cpu_count() * 2) + 1
threads = workers
timeout=120