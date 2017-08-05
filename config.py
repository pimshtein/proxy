# you can change this config on runtime
# host to bind socket
host = '127.0.0.1'
# port to bind socket
port = 2323
# max length on request to target url and receive to client
max_request_length = 5 * 1024 * 1024
# timeout on connection to target url
connection_timeout = 3 * 60
# who can connect to proxy
ip_allowed = ['127.0.0.1']

# is log enabled?
log_on = 0
# path to log
log_file = '/var/log/proxy.log'
# format log text. Message is required
log_formatter = '%(asctime)s %(levelname)s %(message)s'
# max size on log file (default 5 Mb)
max_bytes = 5 * 1024 * 1024
# how many log files rotate on disk
backup_count = 3
# date time format to log
date_fmt = '%d.%m.%Y %H:%M:%S'
