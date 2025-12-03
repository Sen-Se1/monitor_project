import json
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    def log_event(self, event_type, data):
        """Log event to file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': data
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')