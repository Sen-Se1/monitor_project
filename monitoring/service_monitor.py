import subprocess

class ServiceMonitor:
    def __init__(self, services_to_monitor):
        self.services = services_to_monitor
    
    def check_service(self, service_name):
        """Check if a service is running"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def check_all_services(self):
        """Check all configured services"""
        results = {}
        for service in self.services:
            results[service] = self.check_service(service)
        return results