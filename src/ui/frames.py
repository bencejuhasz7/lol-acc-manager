import customtkinter as ctk
from src.ui.widgets import AccountWidget
from src.ui.dialogs import InputDialog, LoadingDialog, OptionsDialog
from src.utils.constants import (
    DIMENSIONS, COLORS, PADDING, FONTS, 
    DROPDOWN_STYLE, REGULAR_BUTTON_STYLE, 
    ICON_BUTTON_STYLE, DARK_BUTTON_STYLE, 
    CANCEL_BUTTON_STYLE, DELETE_BUTTON_STYLE
)
import threading
import json

class ServerFrame:
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
        
        # Create server label
        self.server_label = ctk.CTkLabel(
            parent, 
            text="SERVER", 
            font=FONTS["HEADER"]
        )
        self.server_label.pack(pady=(PADDING["DEFAULT"], PADDING["TINY"]))
        
        # Create server selection frame
        server_frame = ctk.CTkFrame(parent)
        server_frame.pack(pady=(0, PADDING["DEFAULT"]))
        
        # Get initial server value
        initial_server = (self.data_manager.accounts_data["servers"][0] 
                        if self.data_manager.accounts_data["servers"] 
                        else "No servers")
        
        # Create server dropdown with custom styling
        self.server_var = ctk.StringVar(value=initial_server)
        self.server_dropdown = ctk.CTkOptionMenu(
            server_frame,
            values=self.data_manager.accounts_data["servers"] or ["No servers"],
            variable=self.server_var,
            state="disabled" if not self.data_manager.accounts_data["servers"] else "normal",
            **DROPDOWN_STYLE
        )
        self.server_dropdown.pack(side="left", padx=(0, PADDING["TINY"]))
        
        # Add server button
        self.add_server_btn = ctk.CTkButton(
            server_frame,
            text="+",
            **ICON_BUTTON_STYLE
        )
        self.add_server_btn.configure(command=self.show_add_server_dialog)
        self.add_server_btn.pack(side="left", padx=(0, PADDING["TINY"]))
        
        # Remove server button
        self.remove_server_btn = ctk.CTkButton(
            server_frame,
            text="-",
            command=self.remove_current_server,
            **ICON_BUTTON_STYLE
        )
        self.remove_server_btn.pack(side="left")

    def show_add_server_dialog(self):
        server_name = InputDialog(
            self.parent,
            "Add Server",
            "Enter server name..."
        ).show()
        
        if server_name:
            if self.data_manager.add_server(server_name):
                self.server_dropdown.configure(
                    values=self.data_manager.accounts_data["servers"],
                    state="normal"
                )
                self.server_var.set(server_name)
                if self.refresh_callback:
                    self.refresh_callback(server_name)
    
    def get_current_server(self):
        return self.server_var.get()
    
    def set_refresh_callback(self, callback):
        self.refresh_callback = callback
        
        def on_server_change(value):
            self.data_manager.current_server = value
            callback(value)
        
        self.server_dropdown.configure(command=on_server_change)
    
    def remove_current_server(self):
        """Remove the currently selected server and its data."""
        current_server = self.server_var.get()
        if current_server and current_server != "No servers":
            # Create confirmation dialog
            dialog = ctk.CTkToplevel(self.parent)
            dialog.title("Confirm Delete")
            dialog.geometry(DIMENSIONS["INPUT_DIALOG_SIZE"])
            dialog.transient(self.parent)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = self.parent.winfo_x() + (self.parent.winfo_width() - dialog.winfo_width()) // 2
            y = self.parent.winfo_y() + (self.parent.winfo_height() - dialog.winfo_height()) // 2
            dialog.geometry(f"+{x}+{y}")
            
            # Warning message
            warning_label = ctk.CTkLabel(
                dialog,
                text=f"Are you sure you want to delete\n{current_server} server?\n\nAll data will be lost!",
                font=FONTS["DIALOG"]
            )
            warning_label.pack(pady=PADDING["DIALOG_TOP"])
            
            def confirm_delete():
                # Remove server from servers list
                self.data_manager.accounts_data["servers"].remove(current_server)
                # Remove server's data
                del self.data_manager.accounts_data[current_server]
                # Save changes
                self.data_manager.save_accounts()
                
                # Update dropdown
                if self.data_manager.accounts_data["servers"]:
                    # Set to first available server
                    new_server = self.data_manager.accounts_data["servers"][0]
                    self.server_dropdown.configure(
                        values=self.data_manager.accounts_data["servers"]
                    )
                    self.server_var.set(new_server)
                    if self.refresh_callback:
                        self.refresh_callback(new_server)
                else:
                    # No servers left
                    self.server_dropdown.configure(
                        values=["No servers"],
                        state="disabled"
                    )
                    self.server_var.set("No servers")
                    if self.refresh_callback:
                        self.refresh_callback("No servers")
                
                dialog.destroy()
            
            # Button frame
            button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            button_frame.pack(pady=PADDING["DEFAULT"])
            
            # Yes button (using delete style)
            yes_btn = ctk.CTkButton(
                button_frame,
                text="Yes",
                command=confirm_delete,
                fg_color=COLORS["BUTTON_DELETE"],
                hover_color=COLORS["BUTTON_DELETE_HOVER"],
                width=DIMENSIONS["BUTTON_WIDTH"]
            )
            yes_btn.pack(side="left", padx=PADDING["DEFAULT"], expand=True)
            
            # No button (using cancel style)
            no_btn = ctk.CTkButton(
                button_frame,
                text="No",
                command=dialog.destroy,
                fg_color=COLORS["CANCEL_BUTTON"],
                hover_color=COLORS["CANCEL_BUTTON_HOVER"],
                width=DIMENSIONS["BUTTON_WIDTH"]
            )
            no_btn.pack(side="right", padx=PADDING["DEFAULT"], expand=True)
            
            dialog.bind("<Escape>", lambda e: dialog.destroy())

class AccountsFrame:
    def __init__(self, parent, data_manager, server_frame):
        self.parent = parent
        self.data_manager = data_manager
        self.server_frame = server_frame
        self.accounts = {}
        
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            parent, 
            height=DIMENSIONS["SCROLLABLE_FRAME_HEIGHT"]
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=PADDING["SMALL"])
        
        # Create button frame with dark background
        self.button_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["BUTTON_DARK"]
        )
        self.button_frame.pack(fill="x", pady=PADDING["DEFAULT"])
        
        # Create get ranks button (LEFT)
        self.ranks_button = ctk.CTkButton(
            self.button_frame,
            text="Get Ranks",
            command=self.show_loading,
            height=DIMENSIONS["BUTTON_HEIGHT"],
            width=DIMENSIONS["BUTTON_WIDTH"],
            **REGULAR_BUTTON_STYLE
        )
        self.ranks_button.pack(side="left", padx=PADDING["BUTTON_X"], expand=True)
        
        # Create add account button (MIDDLE)
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add Account",
            command=self.add_account,
            height=DIMENSIONS["BUTTON_HEIGHT"],
            width=DIMENSIONS["BUTTON_WIDTH"]
        )
        self.add_button.pack(side="left", padx=PADDING["BUTTON_X"], expand=True)
        
        # Create order by button (RIGHT)
        self.order_button = ctk.CTkButton(
            self.button_frame,
            text="Order By",
            command=self.show_order_dialog,
            height=DIMENSIONS["BUTTON_HEIGHT"],
            width=DIMENSIONS["BUTTON_WIDTH"],
            **REGULAR_BUTTON_STYLE
        )
        self.order_button.pack(side="right", padx=PADDING["BUTTON_X"], expand=True)

    def add_account(self):
        """Handle the process of adding a new account."""
        # Check if we have a valid server selected
        current_server = self.data_manager.current_server
        if not current_server:
            # If no server exists, prompt to create one
            server_name = InputDialog(
                self.parent,
                "No Server Found",
                "Please enter a server name first..."
            ).show()
            
            if server_name:
                # Convert to uppercase before adding
                server_name = server_name.upper()
                if self.data_manager.add_server(server_name):
                    current_server = server_name
                    # Update server dropdown using server_frame reference
                    self.server_frame.server_dropdown.configure(
                        values=self.data_manager.accounts_data["servers"],
                        state="normal"
                    )
                    self.server_frame.server_var.set(server_name)
                else:
                    return
            else:
                return
        
        # Get account name
        name_dialog = InputDialog(
            self.parent,
            "Enter Account Name",
            "Enter account name..."
        )
        account_name = name_dialog.show()
        if not account_name:
            return
        
        # Get account ID
        id_dialog = InputDialog(
            self.parent,
            "Enter Account ID",
            "Enter account ID..."
        )
        account_id = id_dialog.show()
        if not account_id:
            return
        
        # Get account password
        pass_dialog = InputDialog(
            self.parent,
            "Enter Account Password",
            "Enter account password...",
            show=""
        )
        account_password = pass_dialog.show()
        if not account_password:
            return
        
        # Create account data with initialized usage
        account_data = {
            "name": account_name,
            "id": account_id,
            "password": account_password,
            "usage": {
                "id_copies": 0,
                "password_copies": 0,
                "total_copies": 0
            }
        }
        
        # Add account widget
        self.add_account_widget(account_data)
        
        # Save to data manager
        self.data_manager.accounts_data[current_server].append(account_data)
        self.data_manager.save_accounts()
    
    def add_account_widget(self, account_data):
        """Add a new account widget to the frame."""
        def on_options():
            """Handle account options for this account."""
            from src.ui.dialogs import OptionsDialog  # Import here to avoid circular imports
            
            def handle_rename():
                # Get new name using input dialog
                new_name = InputDialog(
                    self.parent,
                    "Rename Account",
                    "Enter new name...",
                    initial_value=account_data["name"]
                ).show()
                
                if new_name:
                    # Update account data
                    account_data["name"] = new_name
                    # Update UI
                    account.account_button.configure(text=new_name)
                    # Save changes
                    self.data_manager.save_accounts()
            
            def handle_move():
                # Get target position
                new_pos = InputDialog(
                    self.parent,
                    "Move Account to Place (e.g. 2)",
                    "Enter target position (1-based)..."
                ).show()
                
                if new_pos and new_pos.isdigit():
                    current_server = self.data_manager.current_server
                    accounts = self.data_manager.accounts_data[current_server]
                    new_pos = int(new_pos) - 1  # Convert to 0-based index
                    
                    if 0 <= new_pos < len(accounts):
                        # Find current position
                        current_pos = next(
                            i for i, acc in enumerate(accounts)
                            if acc["id"] == account_data["id"]
                        )
                        
                        # Swap accounts
                        accounts[current_pos], accounts[new_pos] = accounts[new_pos], accounts[current_pos]
                        
                        # Save changes
                        self.data_manager.save_accounts()
                        
                        # Refresh UI
                        self.refresh_accounts(current_server)
            
            def handle_delete():
                # Remove from data manager
                current_server = self.data_manager.current_server
                self.data_manager.accounts_data[current_server] = [
                    acc for acc in self.data_manager.accounts_data[current_server] 
                    if acc["id"] != account_data["id"]
                ]
                # Save changes
                self.data_manager.save_accounts()
                # Remove from UI
                account.destroy()
                # Remove from accounts dict
                self.accounts.pop(account_data["id"])
            
            # Show options dialog with new move option
            OptionsDialog(
                self.parent,
                account_data["name"],
                handle_rename,
                handle_delete,
                handle_move  # Added move handler
            )
        
        # Create account widget
        account = AccountWidget(
            self.scrollable_frame,
            account_data,
            on_options,
            self.data_manager
        )
        self.accounts[account_data["id"]] = account
    
    def refresh_accounts(self, server):
        """Refresh the accounts display for the given server."""
        # Clear current accounts
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.accounts.clear()
        
        # Only load accounts if a valid server is selected
        if server and server != "No servers" and server in self.data_manager.accounts_data:
            # Load accounts for current server
            for account in self.data_manager.accounts_data[server]:
                self.add_account_widget(account)
    
    def show_loading(self):
        """Show loading dialog and fetch ranks."""
        from src.services.op_gg_service import OpGGService
        
        # Count total accounts
        total_accounts = sum(
            len(accounts) for server, accounts in self.data_manager.accounts_data.items()
            if server != "servers"
        )
        
        # Create loading dialog with total accounts
        loading_dialog = LoadingDialog(self.parent, total_accounts)
        
        def fetch_ranks():
            # Create OpGG service and update ranks
            opgg_service = OpGGService(self.data_manager)
            opgg_service.update_all_ranks(loading_dialog)
            
            # Close loading dialog and refresh UI
            self.parent.after(0, lambda: [
                loading_dialog.dialog.destroy(),
                self.refresh_accounts(self.data_manager.current_server)
            ])
        
        # Start fetching in a separate thread
        threading.Thread(target=fetch_ranks, daemon=True).start()
    
    def show_order_dialog(self):
        """Show dialog for ordering accounts."""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Order By")
        dialog.geometry(DIMENSIONS["ORDER_DIALOG_SIZE"])
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() - dialog.winfo_width()) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Create order options
        label = ctk.CTkLabel(
            dialog,
            text="Select Order",
            font=FONTS["DIALOG"]
        )
        label.pack(pady=PADDING["DIALOG_TOP"])
        
        def order_by_most_played():
            current_server = self.data_manager.current_server
            accounts = self.data_manager.accounts_data[current_server]
            # Sort by total_copies in descending order
            accounts.sort(key=lambda x: x["usage"]["total_copies"], reverse=True)
            self.data_manager.save_accounts()
            self.refresh_accounts(current_server)
            dialog.destroy()
        
        def order_by_soloq():
            # Load rank mapping
            try:
                with open(self.data_manager.root_dir / "data" / "rank_mapping.json", 'r') as f:
                    rank_mapping = json.load(f)
            except Exception:
                return
            
            current_server = self.data_manager.current_server
            accounts = self.data_manager.accounts_data[current_server]
            
            def get_rank_value(account):
                rank = account.get("ranks", {}).get("solo", {}).get("rank", "Unranked").lower()
                return rank_mapping.get(rank, {}).get("value", 0)
            
            # Sort by rank value in descending order
            accounts.sort(key=get_rank_value, reverse=True)
            self.data_manager.save_accounts()
            self.refresh_accounts(current_server)
            dialog.destroy()
        
        def order_by_flex():
            # Load rank mapping
            try:
                with open(self.data_manager.root_dir / "data" / "rank_mapping.json", 'r') as f:
                    rank_mapping = json.load(f)
            except Exception:
                return
            
            current_server = self.data_manager.current_server
            accounts = self.data_manager.accounts_data[current_server]
            
            def get_rank_value(account):
                rank = account.get("ranks", {}).get("flex", {}).get("rank", "Unranked").lower()
                return rank_mapping.get(rank, {}).get("value", 0)
            
            # Sort by rank value in descending order
            accounts.sort(key=get_rank_value, reverse=True)
            self.data_manager.save_accounts()
            self.refresh_accounts(current_server)
            dialog.destroy()
        
        # Create order buttons with distinct styling
        most_played_btn = ctk.CTkButton(
            dialog,
            text="Most Played",
            command=order_by_most_played,
            **DARK_BUTTON_STYLE
        )
        most_played_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["SMALL"])
        
        soloq_btn = ctk.CTkButton(
            dialog,
            text="SoloQ Rank",
            command=order_by_soloq,
            **DARK_BUTTON_STYLE
        )
        soloq_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["SMALL"])
        
        flex_btn = ctk.CTkButton(
            dialog,
            text="Flex Rank",
            command=order_by_flex,
            **DARK_BUTTON_STYLE
        )
        flex_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["SMALL"])
        
        # Add cancel button with consistent styling
        cancel_btn = ctk.CTkButton(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            **CANCEL_BUTTON_STYLE
        )
        cancel_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["DIALOG_BOTTOM"])
        
        dialog.bind("<Escape>", lambda e: dialog.destroy()) 