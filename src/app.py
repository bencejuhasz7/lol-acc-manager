import customtkinter as ctk
from src.ui.frames import AccountsFrame, ServerFrame
from src.utils.data_manager import DataManager
from src.utils.constants import DIMENSIONS, COLORS, PADDING

class ModernApp:
    """Main application class that initializes and manages the GUI."""
    
    def __init__(self):
        # Create and configure main window
        self.window = ctk.CTk()
        self.window.title("LoL Account Manager")
        self.window.geometry(DIMENSIONS["WINDOW_SIZE"])
        
        # Set application theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Create main container frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=PADDING["DEFAULT"], padx=PADDING["DEFAULT"], fill="both", expand=True)
        
        # Setup UI components
        self.server_frame = ServerFrame(self.main_frame, self.data_manager)
        self.accounts_frame = AccountsFrame(self.main_frame, self.data_manager, self.server_frame)
        
        # Connect server changes to account refresh
        self.server_frame.set_refresh_callback(
            lambda _: self.accounts_frame.refresh_accounts(self.server_frame.get_current_server())
        )
        
        # Load initial accounts
        self.accounts_frame.refresh_accounts(self.server_frame.get_current_server())
    
    def run(self):
        """Start the application main loop."""
        self.window.mainloop() 