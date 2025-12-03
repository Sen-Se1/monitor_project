import time
from config import CONFIG
from monitoring.system_monitor import SystemMonitor
from monitoring.service_monitor import ServiceMonitor
from monitoring.alert_manager import AlertManager
from autohealing.service_healer import ServiceHealer
from autohealing.system_healer import SystemHealer
from utils.logger import Logger
from visualization.dashboard import Dashboard
import webbrowser

class SystemMonitorApp:
    def __init__(self, config):
        self.config = config
        self.monitor = SystemMonitor()
        self.service_monitor = ServiceMonitor(config['services'])
        self.alert_manager = AlertManager({
            'cpu': config['cpu_threshold'],
            'memory': config['memory_threshold'],
            'disk': config['disk_threshold']
        })
        self.service_healer = ServiceHealer()
        self.system_healer = SystemHealer()
        self.logger = Logger(config['log_file'])
        self.dashboard = Dashboard(config['dashboard_port'])
        self.cycle_count = 0
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        self.cycle_count += 1
        print(f"\n=== Cycle #{self.cycle_count} ===")
        
        # 1. Collect metrics
        metrics = self.monitor.check_system()
        services_status = self.service_monitor.check_all_services()
        
        print(f"Metrics :\n   CPU: {metrics['cpu']:.1f}%, Mem: {metrics['memory']:.1f}%, Disk: {metrics['disk']:.1f}%")
        
        # 2. Display services status
        print("Services :")
        for service, status in services_status.items():
            print(f"   {service}: {'Running' if status else 'Stopped'}")
        
        # 3. Check for alerts
        alerts = self.alert_manager.check_all_alerts(metrics, services_status)
        if alerts:
            print("Alerts :")
            for alert in alerts:
                print(f"   {alert}")
        else:
            print("No alerts")
        
        # 4. Auto-healing
        healing_actions = []
        if self.config['auto_heal']:
            # Heal services
            service_actions = self.service_healer.heal_services(services_status)
            healing_actions.extend(service_actions)
            
            # Heal system
            system_actions = self.system_healer.heal_system(metrics, self.config['disk_threshold'])
            healing_actions.extend(system_actions)
            
            # Display healing actions
            if healing_actions:
                print("Auto-healing actions :")
                for action in healing_actions:
                    if isinstance(action, dict):
                        print(f"   {action['message']}")
                    else:
                        print(f"   {action}")
        
        # 5. Log everything
        self.logger.log_event('metrics', metrics)
        self.logger.log_event('services', services_status)
        if alerts:
            self.logger.log_event('alerts', alerts)
        if healing_actions:
            self.logger.log_event('healing', healing_actions)
        
        # 6. Update dashboard
        self.dashboard.generate_dashboard(metrics, alerts, healing_actions)
        
        print("-" * 40)
        
        return metrics, alerts, healing_actions
    
    def run_continuous(self):
        """Run monitoring continuously"""
        print("Starting System Monitor")
        print(f"Interval: {self.config['interval']} seconds")
        print(f"Auto-healing: {'Enabled' if self.config['auto_heal'] else 'Disabled'}")
        print(f"Dashboard: http://localhost:{self.config['dashboard_port']}")
        print("=" * 50)

        self.dashboard.start_in_background()

        time.sleep(5)
        
        try:
            webbrowser.open(f'http://localhost:{self.config["dashboard_port"]}')
        except:
            pass
        
        try:
            while True:
                self.run_monitoring_cycle()
                time.sleep(self.config['interval'])
        except KeyboardInterrupt:
            print("\nMonitor stopped by user")
        except Exception as e:
            print(f"\nError: {e}")

def main():
    """Main function"""
    monitor = SystemMonitorApp(CONFIG)
    monitor.run_continuous()

if __name__ == "__main__":
    main()