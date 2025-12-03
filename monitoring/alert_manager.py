class AlertManager:
    def __init__(self, thresholds):
        self.thresholds = thresholds
    
    def check_thresholds(self, metrics):
        """Check for system alerts"""
        alerts = []
        
        if metrics['cpu'] > self.thresholds['cpu']:
            alerts.append(f"High CPU: {metrics['cpu']}%")
        
        if metrics['memory'] > self.thresholds['memory']:
            alerts.append(f"High Memory: {metrics['memory']}%")
        
        if metrics['disk'] > self.thresholds['disk']:
            alerts.append(f"Low Disk: {metrics['disk']}%")
        
        return alerts
    
    def check_services_alerts(self, services_status):
        """Check for service alerts"""
        alerts = []
        for service, status in services_status.items():
            if not status:
                alerts.append(f"Service down: {service}")
        return alerts
    
    def check_all_alerts(self, metrics, services_status):
        """Check all alerts"""
        system_alerts = self.check_thresholds(metrics)
        service_alerts = self.check_services_alerts(services_status)
        return system_alerts + service_alerts