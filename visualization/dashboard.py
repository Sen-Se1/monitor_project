import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

class Dashboard:
    def __init__(self, port=8080):
        self.port = port
        self.server_thread = None
    
    def _format_alerts(self, alerts):
        if not alerts:
            return '<div class="ok-item">✅ All systems normal</div>'
        
        html = ''
        for alert in alerts:
            html += f'<div class="alert-item">{alert}</div>'
        return html
    
    def _format_actions(self, actions):
        if not actions:
            return '<div class="ok-item">No recent actions</div>'
        
        html = ''
        for action in actions:
            if isinstance(action, dict):
                html += f'<div class="action-item">{action["message"]}</div>'
            else:
                html += f'<div class="action-item">{action}</div>'
        return html
    
    def generate_dashboard(self, metrics, alerts, healing_actions):
        """Generate HTML dashboard"""
        
        cpu_status = "Good" if metrics['cpu'] < 80 else "Warning" if metrics['cpu'] < 90 else "Critical"
        cpu_color = "#2ecc71" if metrics['cpu'] < 80 else "#f39c12" if metrics['cpu'] < 90 else "#e74c3c"
        
        mem_status = "Good" if metrics['memory'] < 85 else "Warning" if metrics['memory'] < 95 else "Critical"
        mem_color = "#2ecc71" if metrics['memory'] < 85 else "#f39c12" if metrics['memory'] < 95 else "#e74c3c"
        
        disk_status = "Good" if metrics['disk'] < 90 else "Warning" if metrics['disk'] < 95 else "Critical"
        disk_color = "#2ecc71" if metrics['disk'] < 90 else "#f39c12" if metrics['disk'] < 95 else "#e74c3c"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>System Monitor</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .metrics {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
                .metric-card {{ 
                    flex: 1; min-width: 200px; background: white; padding: 20px; 
                    border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .metric-value {{ font-size: 24px; font-weight: bold; margin: 10px 0; }}
                .metric-label {{ color: #666; }}
                .alerts {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .alert-item {{ padding: 10px; margin: 5px 0; border-left: 4px solid #e74c3c; background: #fff5f5; }}
                .ok-item {{ padding: 10px; margin: 5px 0; border-left: 4px solid #2ecc71; background: #f0fff4; }}
                .actions {{ background: white; padding: 20px; border-radius: 5px; }}
                .action-item {{ padding: 10px; margin: 5px 0; border-left: 4px solid #3498db; background: #f0f8ff; }}
                .status {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 12px; color: white; }}
                .refresh-btn {{ 
                    background: #3498db; color: white; border: none; 
                    padding: 10px 20px; border-radius: 5px; cursor: pointer;
                    margin: 10px 0;
                }}
                .timestamp {{ color: #666; font-size: 12px; text-align: right; }}
                h1, h2 {{ margin-top: 0; }}
                @media (max-width: 768px) {{
                    .metrics {{ flex-direction: column; }}
                    .metric-card {{ min-width: auto; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 System Monitor</h1>
                    <p>Real-time system monitoring and auto-healing</p>
                    <div class="timestamp">Last update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
                </div>
                
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-label">CPU Usage</div>
                        <div class="metric-value" style="color: {cpu_color}">
                            {metrics['cpu']:.1f}%
                        </div>
                        <span class="status" style="background: {cpu_color}">
                            {cpu_status}
                        </span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">Memory Usage</div>
                        <div class="metric-value" style="color: {mem_color}">
                            {metrics['memory']:.1f}%
                        </div>
                        <span class="status" style="background: {mem_color}">
                            {mem_status}
                        </span>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">Disk Usage</div>
                        <div class="metric-value" style="color: {disk_color}">
                            {metrics['disk']:.1f}%
                        </div>
                        <span class="status" style="background: {disk_color}">
                            {disk_status}
                        </span>
                    </div>
                </div>
                
                <div class="alerts">
                    <h2>🚨 Active Alerts</h2>
                    {self._format_alerts(alerts)}
                </div>
                
                <div class="actions">
                    <h2>⚡ Auto-Healing Actions</h2>
                    {self._format_actions(healing_actions)}
                </div>
                
                <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
                <p><small>Auto-refreshes every 11 seconds</small></p>
            </div>
            
            <script>
                // Auto-refresh every 11 seconds
                setTimeout(function() {{
                    location.reload();
                }}, 1000);
            </script>
        </body>
        </html>
        """
        
        with open('dashboard.html', 'w') as f:
            f.write(html)
        
        return html

    def run_server(self):
        """Run dashboard server"""
        os.chdir('.')
        
        class DashboardHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.path = '/dashboard.html'
                return SimpleHTTPRequestHandler.do_GET(self)
        
        server = HTTPServer(('localhost', self.port), DashboardHandler)
        print(f"Dashboard available at: http://localhost:{self.port}")
        print("   Press Ctrl+C to stop")
        server.serve_forever()
    
    def start_in_background(self):
        """Start dashboard in background thread"""
        self.server_thread = Thread(target=self.run_server, daemon=True)
        self.server_thread.start()