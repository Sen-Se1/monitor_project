import subprocess

class SystemHealer:
    @staticmethod
    def cleanup_temp():
        """Clean temp files"""
        try:
            subprocess.run(['find', '/tmp', '-type', 'f', '-mtime', '+1', '-delete'], 
                         capture_output=True)
            return True, "Cleaned temp files"
        except Exception as e:
            return False, f"Cleanup failed: {e}"
    
    def heal_system(self, metrics, disk_threshold):
        """Heal system based on metrics"""
        actions = []
        
        if metrics['disk'] > disk_threshold:
            success, message = self.cleanup_temp()
            actions.append({
                'type': 'cleanup_temp',
                'success': success,
                'message': message
            })
        
        return actions