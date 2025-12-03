
# 🔧 Monitor Project

A comprehensive monitoring and auto-healing system for services and infrastructure.

## ✨ Features

- **Real-time Monitoring**: Track system and service health with customizable metrics
- **Auto-healing**: Automated recovery for common service failures
- **Alert Management**: Configurable alerting system with multiple notification channels
- **Visualization**: Interactive dashboards and chart generation
- **Centralized Logging**: Structured logging with easy query capabilities

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.8 or higher
- **Bash**: For running setup scripts (Unix/Linux/macOS)
- **Git**: For cloning the repository

### Automated Setup (Recommended)

Use the provided setup script for a complete installation:

```bash
# Make the script executable
chmod +x start.sh

# Run the automated setup
./start.sh
```

The script will:
1. Verify Python version
2. Create a virtual environment
3. Install all dependencies
4. Validate the installation
5. Start the monitoring system

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sen-Se1/monitor_project
   cd monitor_project
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the system**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
monitor_project/
├── .gitignore               
├── README.md               
├── config.py              
├── main.py              
├── requirements.txt      
├── start.sh              
│
├── autohealing/          
│   ├── __init__.py
│   ├── service_healer.py
│   └── system_healer.py 
│
├── monitoring/          
│   ├── __init__.py
│   ├── alert_manager.py
│   ├── service_monitor.py 
│   └── system_monitor.py
│
├── utils/                
│   ├── __init__.py
│   └── logger.py        
│
├── visualization/       
│   ├── __init__.py
│   ├── chart_generator.py
│   └── dashboard.py    
│
└── logs/                
    └── monitor.log
```

## 🛠️ Configuration

Edit `config.py` to customize the system:

```python
# Example configuration
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
```

## 🔍 Monitoring Capabilities

### System Metrics
- CPU usage and load averages
- Memory consumption and swap usage
- Disk I/O and space utilization
- Network traffic and connectivity
- Process monitoring and management

### Service Health Checks
- HTTP/HTTPS endpoint availability
- TCP port connectivity
- Database connection validation
- API response time monitoring
- Custom script execution checks

## ⚡ Auto-healing Actions

### Service Recovery
- Automatic service restart
- Configuration validation and repair
- Dependency verification
- Resource allocation adjustment

### System Optimization
- Log rotation and cleanup
- Temporary file removal
- Cache management
- Connection pool optimization

## 📈 Visualization Features

### Dashboard
- Real-time metrics display
- Historical trend analysis
- Alert summary and history
- Service health status overview

### Reports
- Daily/Weekly/Monthly summaries
- Performance trend analysis
- Incident reports
- Resource utilization charts

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🔧 Troubleshooting

### Common Issues

1. **Permission Denied** on `start.sh`
   ```bash
   chmod +x start.sh
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration Errors**
   - Verify `config.py` exists and is properly formatted
   - Check environment variables if used

### Getting Help
- Check the `logs/` directory for error details
- Review the configuration in `config.py`
- Open an issue on GitHub with relevant logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.