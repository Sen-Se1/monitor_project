import subprocess

class ServiceHealer:
    @staticmethod
    def restart_service(service_name):
        """Attempt to restart a service"""
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', service_name], 
                         capture_output=True, timeout=10)
            return True, f"Restarted {service_name}"
        except Exception as e:
            return False, f"Failed to restart {service_name}: {e}"
    
    def heal_services(self, services_status):
        """Heal all stopped services"""
        actions = []
        for service, status in services_status.items():
            if not status:
                success, message = self.restart_service(service)
                actions.append({
                    'service': service,
                    'success': success,
                    'message': message
                })
        return actions