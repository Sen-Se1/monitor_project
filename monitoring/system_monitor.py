import psutil
from datetime import datetime

class SystemMonitor:
    @staticmethod
    def check_system():
        """Get basic system metrics"""
        return {
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }