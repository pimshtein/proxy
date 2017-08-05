host = '127.0.0.1'
port = 2323
max_request_length = 5 * 1024 * 1024
connection_timeout = 3 * 60
# who can connect to proxy
ip_allowed = ['127.0.0.1']

log_on = 0
log_file = 'log'
log_formatter = '%(asctime)s %(levelname)s %(message)s'
max_bytes = 5 * 1024 * 1024
backup_count = 5
date_fmt = '%d.%m.%Y %H:%M:%S'
