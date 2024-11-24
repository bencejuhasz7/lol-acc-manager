import json
import os
from pathlib import Path
import sys

class DataManager:
    """Handles all data operations for the application."""
    
    def __init__(self):
        # Get the application directory (works for both script and exe)
        if getattr(sys, 'frozen', False):
            # Running as executable
            self.root_dir = Path(sys._MEIPASS).parent
        else:
            # Running as script
            self.root_dir = Path(__file__).parent.parent.parent
        
        # Create data directory next to the executable/script
        self.data_dir = self.root_dir / "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.data_file = self.data_dir / "accounts.json"
        
        # Create empty accounts.json if it doesn't exist
        if not self.data_file.exists():
            self.create_empty_accounts_file()
        
        self.accounts_data = self.load_accounts()
        
        # Set initial server if available
        self._current_server = (
            self.accounts_data["servers"][0] 
            if self.accounts_data["servers"] 
            else None
        )
    
    def create_empty_accounts_file(self):
        """Create an empty accounts.json file with initial structure."""
        empty_data = {
            "servers": []
        }
        with open(self.data_file, 'w') as f:
            json.dump(empty_data, f, indent=4)
    
    @property
    def current_server(self):
        """Get the current server."""
        return self._current_server
    
    @current_server.setter
    def current_server(self, server):
        """Set the current server."""
        if server and server != "No servers" and server in self.accounts_data["servers"]:
            self._current_server = server
    
    def add_server(self, server_name):
        """Add a new server."""
        # Convert server name to uppercase
        server_name = server_name.upper()
        
        # Check if server exists (case-insensitive check)
        if server_name not in [s.upper() for s in self.accounts_data["servers"]]:
            self.accounts_data["servers"].append(server_name)
            self.accounts_data[server_name] = []  # Initialize empty account list
            if not self._current_server:
                self._current_server = server_name
            self.save_accounts()
            return True
        return False
    
    def load_accounts(self):
        """Load accounts from JSON file."""
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def save_accounts(self):
        """Save accounts to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.accounts_data, f, indent=4) 