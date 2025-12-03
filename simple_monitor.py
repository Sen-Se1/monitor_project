import time
import psutil
import subprocess
from datetime import datetime

INTERVAL = 10  # seconds
SERVICES = ['cron', 'dbus']

def check_metrics():
    """Get system metrics"""
    return {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'time': datetime.now().strftime("%H:%M:%S")
    }

def check_service(service):
    """Check if a service is running"""
    try:
        result = subprocess.run(['systemctl', 'is-active', service],
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def main():
    print("📊 Simple System Monitor Started")
    print("Press Ctrl+C to stop\n")
    
    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\nCheck #{cycle} ({datetime.now().strftime('%H:%M:%S')})")
            
            metrics = check_metrics()
            print(f"CPU: {metrics['cpu']:.1f}% | "
                  f"Memory: {metrics['memory']:.1f}% | "
                  f"Disk: {metrics['disk']:.1f}%")
            
            for service in SERVICES:
                status = check_service(service)
                icon = "✅" if status else "❌"
                print(f"{icon} {service}: {'Running' if status else 'Stopped'}")
            
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped")
    except Exception as e:
        print(f"\n⚠️ Error: {e}")

if __name__ == "__main__":
    main()