CONFIG = {
    'interval': 10,  # seconds between checks
    'cpu_threshold': 80,
    'memory_threshold': 85,
    'disk_threshold': 90,
    'services': ['cron', 'dbus'],
    'auto_heal': True,
    'log_file': './logs/monitor.log',
    'dashboard_port': 8090
}