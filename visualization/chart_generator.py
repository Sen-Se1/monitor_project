import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
import os

class ChartGenerator:
    def __init__(self, log_file='./logs/monitor.log'):
        self.log_file = log_file
    
    def read_logs(self, limit=100):
        """Read recent logs from the log file"""
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        logs.append(json.loads(line.strip()))
                    except:
                        continue
        return logs[-limit:] if logs else []
    
    def create_resource_chart(self):
        """Create chart showing CPU, RAM, Disk usage over time"""
        logs = self.read_logs(50)  # Last 50 readings
        if not logs:
            return None
        
        metrics_logs = [log for log in logs if log.get('type') == 'metrics']
        
        if len(metrics_logs) < 2:
            return None
        
        timestamps = []
        cpu_values = []
        memory_values = []
        disk_values = []
        
        for log in metrics_logs:
            data = log.get('data', {})
            if 'cpu' in data and 'memory' in data and 'disk' in data:
                timestamps.append(log.get('timestamp', ''))
                cpu_values.append(data['cpu'])
                memory_values.append(data['memory'])
                disk_values.append(data['disk'])
        
        if not timestamps:
            return None
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CPU Usage Over Time', 'Memory Usage Over Time', 
                          'Disk Usage Over Time', 'Current Resource Usage'),
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        display_timestamps = []
        for ts in timestamps:
            try:
                dt = datetime.fromisoformat(ts)
                display_timestamps.append(dt.strftime("%H:%M:%S"))
            except:
                display_timestamps.append(ts)
        
        fig.add_trace(
            go.Scatter(
                x=display_timestamps,
                y=cpu_values,
                name="CPU %",
                line=dict(color='#ef4444', width=2),
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(239, 68, 68, 0.2)'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=display_timestamps,
                y=memory_values,
                name="Memory %",
                line=dict(color='#10b981', width=2),
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.2)'
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=display_timestamps,
                y=disk_values,
                name="Disk %",
                line=dict(color='#3b82f6', width=2),
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.2)'
            ),
            row=2, col=1
        )
        
        latest_metrics = metrics_logs[-1]['data']
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=latest_metrics.get('cpu', 0),
                title={'text': "CPU"},
                delta={'reference': 80},
                domain={'row': 2, 'column': 2, 'x': [0, 0.33], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                    'bar': {'color': "#ef4444"},
                    'steps': [
                        {'range': [0, 80], 'color': "#475569"},
                        {'range': [80, 90], 'color': "#f59e0b"},
                        {'range': [90, 100], 'color': "#ef4444"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': latest_metrics.get('cpu', 0)
                    }
                }
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=latest_metrics.get('memory', 0),
                title={'text': "Memory"},
                delta={'reference': 85},
                domain={'row': 2, 'column': 2, 'x': [0.33, 0.66], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                    'bar': {'color': "#10b981"},
                    'steps': [
                        {'range': [0, 85], 'color': "#475569"},
                        {'range': [85, 95], 'color': "#f59e0b"},
                        {'range': [95, 100], 'color': "#ef4444"}
                    ]
                }
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=latest_metrics.get('disk', 0),
                title={'text': "Disk"},
                delta={'reference': 90},
                domain={'row': 2, 'column': 2, 'x': [0.66, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                    'bar': {'color': "#3b82f6"},
                    'steps': [
                        {'range': [0, 90], 'color': "#475569"},
                        {'range': [90, 95], 'color': "#f59e0b"},
                        {'range': [95, 100], 'color': "#ef4444"}
                    ]
                }
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="#1e293b",
                bordercolor="#334155",
                borderwidth=1
            ),
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font=dict(family='Inter, sans-serif', color='#f1f5f9', size=10)
        )
        
        fig.update_xaxes(
            title_text="Time",
            showgrid=True,
            gridcolor='#334155',
            zerolinecolor='#334155',
            row=1, col=1
        )
        fig.update_xaxes(
            title_text="Time",
            showgrid=True,
            gridcolor='#334155',
            zerolinecolor='#334155',
            row=1, col=2
        )
        fig.update_xaxes(
            title_text="Time",
            showgrid=True,
            gridcolor='#334155',
            zerolinecolor='#334155',
            row=2, col=1
        )
        
        fig.update_yaxes(
            title_text="Usage %",
            range=[0, 100],
            showgrid=True,
            gridcolor='#334155',
            zerolinecolor='#334155',
            row=1, col=1
        )
        fig.update_yaxes(
            title_text="Usage %",
            range=[0, 100],
            showgrid=True,
            gridcolor='#334155',
            zerolinecolor='#334155',
            row=1, col=2
        )
        fig.update_yaxes(
            title_text="Usage %",
            range=[0, 100],
            showgrid=True,
            gridcolor='#334155',
            zerolinecolor='#334155',
            row=2, col=1
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_simple_resource_chart(self):
        """Simpler version: Separate charts for each resource"""
        logs = self.read_logs(30)  # Last 30 readings
        if not logs:
            return None
        
        metrics_logs = [log for log in logs if log.get('type') == 'metrics']
        
        if len(metrics_logs) < 2:
            return None
        
        timestamps = []
        cpu_values = []
        memory_values = []
        disk_values = []
        
        for log in metrics_logs:
            data = log.get('data', {})
            if 'cpu' in data and 'memory' in data and 'disk' in data:
                try:
                    dt = datetime.fromisoformat(log.get('timestamp', ''))
                    timestamps.append(dt.strftime("%H:%M:%S"))
                except:
                    timestamps.append(log.get('timestamp', ''))
                cpu_values.append(data['cpu'])
                memory_values.append(data['memory'])
                disk_values.append(data['disk'])
        
        if not timestamps:
            return None
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=cpu_values,
            name="CPU %",
            line=dict(color='#ef4444', width=3),
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=memory_values,
            name="Memory %",
            line=dict(color='#10b981', width=3),
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))
        
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=disk_values,
            name="Disk %",
            line=dict(color='#3b82f6', width=3),
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        fig.update_layout(
            title='Resource Usage Over Time',
            xaxis_title='Time',
            yaxis_title='Usage %',
            height=400,
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font=dict(family='Inter, sans-serif', color='#f1f5f9', size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="#1e293b",
                bordercolor="#334155",
                borderwidth=1
            )
        )
        
        fig.update_yaxes(range=[0, 100])
        fig.update_xaxes(showgrid=True, gridcolor='#334155', zerolinecolor='#334155')
        fig.update_yaxes(showgrid=True, gridcolor='#334155', zerolinecolor='#334155')
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def create_incidents_chart(self):
        """Create chart showing incidents by type"""
        logs = self.read_logs(100)
        if not logs:
            return None
        
        alert_counts = {'Service Down': 0, 'High CPU': 0, 'High Memory': 0, 'Low Disk': 0}
        
        for log in logs:
            if log.get('type') == 'alerts':
                alerts = log.get('data', [])
                for alert in alerts:
                    alert_str = str(alert).lower()
                    if 'service down' in alert_str or 'stopped' in alert_str:
                        alert_counts['Service Down'] += 1
                    elif 'cpu' in alert_str:
                        alert_counts['High CPU'] += 1
                    elif 'memory' in alert_str:
                        alert_counts['High Memory'] += 1
                    elif 'disk' in alert_str:
                        alert_counts['Low Disk'] += 1
        
        alert_counts = {k: v for k, v in alert_counts.items() if v > 0}
        
        if not alert_counts:
            return None
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(alert_counts.keys()),
                y=list(alert_counts.values()),
                marker_color=['#ef4444', '#f59e0b', '#10b981', '#3b82f6'][:len(alert_counts)],
                text=list(alert_counts.values()),
                textposition='auto',
                textfont={'color': '#f1f5f9'}
            )
        ])
        
        fig.update_layout(
            title='Incidents by Type',
            xaxis_title='Incident Type',
            yaxis_title='Count',
            height=350,
            paper_bgcolor='#0f172a',
            font=dict(family='Inter, sans-serif', color='#f1f5f9', size=12),
            plot_bgcolor='#1e293b',
            xaxis=dict(showgrid=True, gridcolor='#334155', zerolinecolor='#334155'),
            yaxis=dict(showgrid=True, gridcolor='#334155', zerolinecolor='#334155')
        )
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_actions_chart(self):
        """Create chart showing healing actions"""
        logs = self.read_logs(100)
        if not logs:
            return None
        
        actions_data = []
        for log in logs:
            if log.get('type') == 'healing':
                actions = log.get('data', [])
                for action in actions:
                    if isinstance(action, dict):
                        message = action.get('message', '')
                        success = action.get('success', False)
                        if 'restart' in message.lower():
                            action_type = 'Service Restart'
                        elif 'clean' in message.lower():
                            action_type = 'Cleanup'
                        else:
                            action_type = 'Other'
                        
                        actions_data.append({
                            'type': action_type,
                            'success': success,
                            'timestamp': log.get('timestamp', '')
                        })
        
        if not actions_data:
            return None
        
        success_count = sum(1 for action in actions_data if action['success'])
        failed_count = sum(1 for action in actions_data if not action['success'])
        
        fig = go.Figure(data=[
            go.Pie(
                labels=['Successful', 'Failed'],
                values=[success_count, failed_count],
                hole=0.4,
                marker_colors=['#10b981', '#ef4444'],
                textinfo='label+percent+value',
                hoverinfo='label+percent+value',
                textfont={'color': '#f1f5f9'}
            )
        ])
        
        fig.update_layout(
            title='Healing Actions Success Rate',
            height=350,
            paper_bgcolor='#0f172a',
            font=dict(family='Inter, sans-serif', color='#f1f5f9', size=12),
            showlegend=True,
            plot_bgcolor='#1e293b',
            legend=dict(
                bgcolor="#1e293b",
                bordercolor="#334155",
                borderwidth=1
            )
        )
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_current_metrics_chart(self, current_metrics):
        """Create gauge chart for current metrics"""
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('CPU', 'Memory', 'Disk'),
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=current_metrics.get('cpu', 0),
                title={'text': "CPU Usage", 'font': {'color': '#f1f5f9'}},
                delta={'reference': 80, 'position': "top", 'relative': True, 'valueformat': '.0%', 'font': {'color': '#f1f5f9'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94a3b8', 'tickfont': {'color': '#94a3b8'}},
                    'bar': {'color': "#ef4444"},
                    'steps': [
                        {'range': [0, 80], 'color': "#475569"},
                        {'range': [80, 90], 'color': "#f59e0b"},
                        {'range': [90, 100], 'color': "#ef4444"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': current_metrics.get('cpu', 0)
                    }
                }
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=current_metrics.get('memory', 0),
                title={'text': "Memory Usage", 'font': {'color': '#f1f5f9'}},
                delta={'reference': 85, 'position': "top", 'relative': True, 'valueformat': '.0%', 'font': {'color': '#f1f5f9'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94a3b8', 'tickfont': {'color': '#94a3b8'}},
                    'bar': {'color': "#10b981"},
                    'steps': [
                        {'range': [0, 85], 'color': "#475569"},
                        {'range': [85, 95], 'color': "#f59e0b"},
                        {'range': [95, 100], 'color': "#ef4444"}
                    ]
                }
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=current_metrics.get('disk', 0),
                title={'text': "Disk Usage", 'font': {'color': '#f1f5f9'}},
                delta={'reference': 90, 'position': "top", 'relative': True, 'valueformat': '.0%', 'font': {'color': '#f1f5f9'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#94a3b8', 'tickfont': {'color': '#94a3b8'}},
                    'bar': {'color': "#3b82f6"},
                    'steps': [
                        {'range': [0, 90], 'color': "#475569"},
                        {'range': [90, 95], 'color': "#f59e0b"},
                        {'range': [95, 100], 'color': "#ef4444"}
                    ]
                }
            ),
            row=1, col=3
        )
        
        fig.update_layout(
            height=300,
            paper_bgcolor='#0f172a',
            font=dict(family='Inter, sans-serif', color='#f1f5f9', size=12),
            plot_bgcolor='#1e293b'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def generate_all_charts(self, metrics, services_status):
        """Generate all charts and return HTML"""
        charts_html = {
            'resource_chart': self.create_simple_resource_chart(),
            'current_metrics': self.create_current_metrics_chart(metrics),
            'incidents_chart': self.create_incidents_chart(),
            'actions_chart': self.create_actions_chart()
        }
        
        return charts_html