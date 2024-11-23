import json
import os
from pathlib import Path

class DataManager:
    """Handles all data operations for the application."""
    
    def __init__(self):
        # Get the root directory of the project
        self.root_dir = Path(__file__).parent.parent.parent
        self.data_file = self.root_dir / "data" / "accounts.json"
        
        # Create data directory and empty accounts.json if they don't exist
        os.makedirs(self.root_dir / "data", exist_ok=True)
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
        
        if server_name not in self.accounts_data["servers"]:
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