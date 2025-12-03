import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from visualization.chart_generator import ChartGenerator

class Dashboard:
    def __init__(self, port=8080):
        self.port = port
        self.server_thread = None
        self.chart_generator = ChartGenerator()
    
    def _format_alerts(self, alerts):
        if not alerts:
            return '<div class="ok-item">✅ All systems normal</div>'
        
        html = ''
        for alert in alerts:
            html += f'<div class="alert-item">{alert}</div>'
        return html

    def _format_actions(self, actions):
        if not actions:
            return '<div class="ok-item">✅ No recent auto-healing actions</div>'
        
        html = ''
        for action in actions:
            if isinstance(action, dict):
                success = action.get('success')
                message = action.get('message', '')
                service = action.get('service', 'Unknown')
                
                if success is True:
                    color_class = "success-action"
                    border_color = "#10b981"
                    bg_gradient = "linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, transparent 100%)"
                    icon = "✅"
                    status_text = "Success"
                elif success is False:
                    color_class = "error-action"
                    border_color = "#ef4444"
                    bg_gradient = "linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, transparent 100%)"
                    icon = "❌"
                    status_text = "Failed"
                else:
                    color_class = "neutral-action"
                    border_color = "#3b82f6"
                    bg_gradient = "linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%)"
                    icon = "⚡"
                    status_text = "Unknown"
                
                if len(message) > 80:
                    display_message = message[:77] + "..."
                    title_attr = f'title="{message}"'
                else:
                    display_message = message
                    title_attr = ""
                
                html += f'''
                <div class="action-item {color_class}" 
                     style="border-left-color: {border_color}; background: {bg_gradient};"
                     {title_attr}>
                    <div style="display: flex; align-items: flex-start; gap: 10px; width: 100%;">
                        <span style="font-size: 1.1em; flex-shrink: 0;">{icon}</span>
                        <div style="flex-grow: 1;">
                            <div style="font-weight: 500; margin-bottom: 4px; color: var(--text-primary);">
                                {display_message}
                            </div>
                            <div style="font-size: 0.85em; opacity: 0.7; display: flex; justify-content: space-between;">
                                <span>Service: <strong>{service}</strong></span>
                                <span style="color: {border_color}; font-weight: 600;">{status_text}</span>
                            </div>
                        </div>
                    </div>
                </div>
                '''
            else:
                action_text = str(action)
                if len(action_text) > 80:
                    display_text = action_text[:77] + "..."
                    title_attr = f'title="{action_text}"'
                else:
                    display_text = action_text
                    title_attr = ""
                
                html += f'''
                <div class="action-item" {title_attr}>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>⚡</span>
                        <span>{display_text}</span>
                    </div>
                </div>
                '''
        
        return html

    def generate_dashboard(self, metrics, alerts, healing_actions):
        """Generate HTML dashboard with charts"""
        
        charts_html = self.chart_generator.generate_all_charts(metrics, {})
        
        cpu_status = "Good" if metrics['cpu'] < 80 else "Warning" if metrics['cpu'] < 90 else "Critical"
        cpu_color = "#10b981" if metrics['cpu'] < 80 else "#f59e0b" if metrics['cpu'] < 90 else "#ef4444"
        
        mem_status = "Good" if metrics['memory'] < 85 else "Warning" if metrics['memory'] < 95 else "Critical"
        mem_color = "#10b981" if metrics['memory'] < 85 else "#f59e0b" if metrics['memory'] < 95 else "#ef4444"
        
        disk_status = "Good" if metrics['disk'] < 90 else "Warning" if metrics['disk'] < 95 else "Critical"
        disk_color = "#10b981" if metrics['disk'] < 90 else "#f59e0b" if metrics['disk'] < 95 else "#ef4444"
        
        current_time = datetime.now()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>System Monitor</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
            <meta http-equiv="Pragma" content="no-cache">
            <meta http-equiv="Expires" content="0">
            <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --primary: #0f172a;
                    --secondary: #1e293b;
                    --accent: #3b82f6;
                    --success: #10b981;
                    --warning: #f59e0b;
                    --error: #ef4444;
                    --bg-primary: #f8fafc;
                    --bg-secondary: #ffffff;
                    --text-primary: #0f172a;
                    --text-secondary: #64748b;
                    --border: #e2e8f0;
                    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
                    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                }}

                * {{
                    box-sizing: border-box;
                }}

                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, var(--bg-primary) 0%, #e2e8f0 100%);
                    color: var(--text-primary);
                    line-height: 1.6;
                }}

                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 0 1rem;
                }}

                .header {{
                    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
                    color: white;
                    padding: 2rem;
                    border-radius: 1rem;
                    margin-bottom: 2rem;
                    box-shadow: var(--shadow-lg);
                    position: relative;
                    overflow: hidden;
                }}

                .header::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                    opacity: 0.05;
                }}

                .header h1 {{
                    margin: 0 0 0.5rem 0;
                    font-size: 2.5rem;
                    font-weight: 700;
                    letter-spacing: -0.025em;
                }}

                .header p {{
                    margin: 0 0 1rem 0;
                    font-size: 1.1rem;
                    opacity: 0.9;
                }}

                .timestamp {{
                    color: rgba(255, 255, 255, 0.8);
                    font-size: 0.875rem;
                    text-align: right;
                    margin: 0;
                }}

                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 1.5rem;
                    margin-bottom: 2rem;
                }}

                .metric-card {{
                    background: var(--bg-secondary);
                    padding: 1.5rem;
                    border-radius: 1rem;
                    box-shadow: var(--shadow);
                    text-align: center;
                    transition: all 0.3s ease;
                    border: 1px solid var(--border);
                }}

                .metric-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: var(--shadow-lg);
                }}

                .metric-label {{
                    font-size: 0.875rem;
                    font-weight: 500;
                    color: var(--text-secondary);
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }}

                .metric-value {{
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin: 0.5rem 0;
                    line-height: 1;
                }}

                .status {{
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    border-radius: 9999px;
                    font-size: 0.75rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    color: white;
                }}

                .alerts, .actions {{
                    background: var(--bg-secondary);
                    padding: 1.5rem;
                    border-radius: 1rem;
                    margin-bottom: 2rem;
                    box-shadow: var(--shadow);
                    border: 1px solid var(--border);
                }}

                .alerts h2, .actions h2 {{
                    margin: 0 0 1rem 0;
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }}

                .alert-item {{
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-left: 4px solid var(--error);
                    background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, transparent 100%);
                    border-radius: 0.5rem;
                    transition: all 0.2s ease;
                }}

                .alert-item:hover {{
                    background: linear-gradient(90deg, rgba(239, 68, 68, 0.15) 0%, transparent 100%);
                }}

                .ok-item {{
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-left: 4px solid var(--success);
                    background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, transparent 100%);
                    border-radius: 0.5rem;
                    color: var(--text-primary);
                    font-weight: 500;
                }}

                .action-item {{
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-left: 4px solid var(--accent);
                    background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%);
                    border-radius: 0.5rem;
                    transition: all 0.2s ease;
                }}

                .action-item:hover {{
                    background: linear-gradient(90deg, rgba(59, 130, 246, 0.15) 0%, transparent 100%);
                }}

                .refresh-btn {{
                    background: linear-gradient(135deg, var(--accent) 0%, #1d4ed8 100%);
                    color: white;
                    border: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 0.5rem;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 0.875rem;
                    transition: all 0.3s ease;
                    box-shadow: var(--shadow);
                    display: block;
                    margin: 0 auto 1rem auto;
                }}

                .refresh-btn:hover {{
                    transform: translateY(-1px);
                    box-shadow: var(--shadow-lg);
                }}

                .chart-container {{
                    background: var(--bg-secondary);
                    padding: 1.5rem;
                    border-radius: 1rem;
                    box-shadow: var(--shadow);
                    margin-bottom: 2rem;
                    border: 1px solid var(--border);
                }}

                .chart-title {{
                    font-size: 1.25rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    border-bottom: 2px solid var(--border);
                    padding-bottom: 0.75rem;
                }}

                .charts-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                    gap: 1.5rem;
                    margin-bottom: 2rem;
                }}

                .small-charts-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                    gap: 1.5rem;
                    margin-bottom: 2rem;
                }}

                .footer-note {{
                    text-align: center;
                    color: var(--text-secondary);
                    font-size: 0.875rem;
                    margin-top: 1rem;
                }}

                /* Dark mode support (optional, can be toggled) */
                @media (prefers-color-scheme: dark) {{
                    :root {{
                        --bg-primary: #0f172a;
                        --bg-secondary: #1e293b;
                        --text-primary: #f1f5f9;
                        --text-secondary: #94a3b8;
                        --border: #334155;
                    }}
                    
                    body {{
                        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                    }}
                }}

                @media (max-width: 768px) {{
                    .container {{
                        padding: 0 0.5rem;
                    }}
                    
                    .header h1 {{
                        font-size: 2rem;
                    }}
                    
                    .metrics {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .charts-grid, .small-charts-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}

                /* Smooth transitions for Plotly charts */
                .js-plotly-plot {{
                    border-radius: 0.5rem;
                    overflow: hidden;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 System Monitor Dashboard</h1>
                    <p>Real-time monitoring, auto-healing, and analytics</p>
                    <div class="timestamp">Last update: {current_time.strftime("%Y-%m-%d %H:%M:%S")}</div>
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
                
                <!-- Current Metrics Gauges -->
                <div class="chart-container">
                    <div class="chart-title">📊 Current Resource Usage</div>
                    {charts_html.get('current_metrics', '<p style="text-align: center; color: var(--text-secondary);">Loading current metrics...</p>')}
                </div>
                
                <!-- Charts Section -->
                <div class="charts-grid">
                    <div class="chart-container">
                        <div class="chart-title">📈 Resource Usage History</div>
                        {charts_html.get('resource_chart', '<p style="text-align: center; color: var(--text-secondary);">Collecting data...</p>')}
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">⚡ Healing Actions Success Rate</div>
                        {charts_html.get('actions_chart', '<p style="text-align: center; color: var(--text-secondary);">No healing actions recorded</p>')}
                    </div>
                </div>
                
                <div class="small-charts-grid">
                    <div class="chart-container">
                        <div class="chart-title">🚨 Incidents by Type</div>
                        {charts_html.get('incidents_chart', '<p style="text-align: center; color: var(--text-secondary);">No incidents recorded</p>')}
                    </div>
                </div>
                
                <div class="alerts">
                    <h2>🚨 Active Alerts</h2>
                    {self._format_alerts(alerts)}
                </div>
                
                <div class="actions">
                    <h2>⚡ Recent Auto-Healing Actions</h2>
                    {self._format_actions(healing_actions)}
                </div>
                
                <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Dashboard</button>
                <p class="footer-note">Auto-refreshes every 13 seconds • Charts update automatically</p>
            </div>
            
            <script>
                // Auto-refresh every 13 seconds
                setTimeout(function() {{
                    location.reload();
                }}, 13000);
            </script>
        </body>
        </html>
        """
        
        with open('dashboard.html', 'w', encoding='utf-8') as f:
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
        
        server = HTTPServer(('0.0.0.0', self.port), DashboardHandler)
        print(f"Dashboard available at: http://localhost:{self.port}")
        print("   Press Ctrl+C to stop")
        server.serve_forever()
    
    def start_in_background(self):
        """Start dashboard in background thread"""
        self.server_thread = Thread(target=self.run_server, daemon=True)
        self.server_thread.start()