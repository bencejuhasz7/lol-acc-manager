import customtkinter as ctk
import threading
import time
from src.utils.constants import (
    DIMENSIONS, COLORS, PADDING, FONTS,
    CANCEL_BUTTON_STYLE, REGULAR_BUTTON_STYLE,
    DELETE_BUTTON_STYLE, DARK_BUTTON_STYLE
)

class InputDialog:
    """Dialog for getting user input with validation."""
    
    def __init__(self, parent, title, placeholder, show=None, initial_value=None):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        if title == "Add Server":
            self.dialog.geometry(DIMENSIONS["ADD_SERVER_DIALOG_SIZE"])
        else:
            self.dialog.geometry(DIMENSIONS["INPUT_DIALOG_SIZE"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.result = {"value": None}
        self._setup_ui(title, placeholder, show, initial_value)
        self._center_dialog(parent)
    
    def _setup_ui(self, title, placeholder, show, initial_value):
        label = ctk.CTkLabel(
            self.dialog,
            text=title,
            font=FONTS["DIALOG"]
        )
        label.pack(pady=PADDING["DIALOG_TOP"])
        
        self.entry = ctk.CTkEntry(
            self.dialog,
            placeholder_text=placeholder,
            show=show
        )
        if initial_value:
            self.entry.insert(0, initial_value)
        self.entry.pack(pady=PADDING["SMALL"], padx=PADDING["DEFAULT"], fill="x")
        self.entry.focus()
        
        # Create buttons vertically aligned
        continue_btn = ctk.CTkButton(
            self.dialog,
            text="Continue",
            command=self._on_continue,
            **REGULAR_BUTTON_STYLE
        )
        continue_btn.pack(pady=(PADDING["DEFAULT"], PADDING["SMALL"]))
        
        cancel_btn = ctk.CTkButton(
            self.dialog,
            text="Cancel",
            command=self._on_cancel,
            **CANCEL_BUTTON_STYLE
        )
        cancel_btn.pack(pady=(0, PADDING["DEFAULT"]))
        
        self.dialog.bind("<Return>", lambda e: self._on_continue())
        self.dialog.bind("<Escape>", lambda e: self._on_cancel())
    
    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
    
    def _on_continue(self):
        """Handle continue button click."""
        self.result["value"] = self.entry.get()
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle cancel button click."""
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result."""
        self.dialog.wait_window()
        return self.result["value"]

class OptionsDialog:
    """Dialog for showing account options."""
    
    def __init__(self, parent, account_name, on_rename, on_delete, on_move):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Account Options")
        self.dialog.geometry(DIMENSIONS["OPTIONS_DIALOG_SIZE"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._setup_ui(account_name, on_rename, on_delete, on_move)
        self._center_dialog(parent)
        
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
    
    def _setup_ui(self, account_name, on_rename, on_delete, on_move):
        name_label = ctk.CTkLabel(
            self.dialog,
            text=f"Account name: {account_name}",
            font=FONTS["DIALOG"]
        )
        name_label.pack(pady=PADDING["DIALOG_TOP"])
        
        rename_btn = ctk.CTkButton(
            self.dialog,
            text="Rename Account",
            command=lambda: [self.dialog.destroy(), on_rename()],
            **DARK_BUTTON_STYLE
        )
        rename_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["SMALL"])
        
        move_btn = ctk.CTkButton(
            self.dialog,
            text="Move Account",
            command=lambda: [self.dialog.destroy(), on_move()],
            **DARK_BUTTON_STYLE
        )
        move_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["SMALL"])
        
        delete_btn = ctk.CTkButton(
            self.dialog,
            text="Delete Account",
            command=lambda: [self.dialog.destroy(), on_delete()],
            **DELETE_BUTTON_STYLE
        )
        delete_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["SMALL"])
        
        cancel_btn = ctk.CTkButton(
            self.dialog,
            text="Cancel",
            command=self.dialog.destroy,
            **CANCEL_BUTTON_STYLE
        )
        cancel_btn.pack(fill="x", padx=PADDING["DEFAULT"], pady=PADDING["DIALOG_BOTTOM"])

    def _center_dialog(self, parent):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")

class LoadingDialog:
    """Dialog for showing loading progress."""
    
    def __init__(self, parent, total_accounts):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Loading")
        self.dialog.geometry(DIMENSIONS["LOADING_DIALOG_SIZE"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.current_account = 0
        self.total_accounts = total_accounts
        
        self._setup_ui()
        self._center_dialog(parent)
    
    def _setup_ui(self):
        # Status label
        self.status_label = ctk.CTkLabel(
            self.dialog,
            text=f"Querying account... [0/{self.total_accounts}]",
            font=FONTS["DIALOG"]
        )
        self.status_label.pack(pady=PADDING["DEFAULT"])
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.dialog)
        self.progress_bar.pack(pady=PADDING["DEFAULT"], padx=PADDING["DEFAULT"], fill="x")
        self.progress_bar.set(0)  # Start at 0
    
    def update_progress(self, account_name):
        """Update progress bar and status text."""
        self.current_account += 1
        progress = self.current_account / self.total_accounts
        self.progress_bar.set(progress)
        self.status_label.configure(
            text=f"Querying account {account_name}... [{self.current_account}/{self.total_accounts}]"
        )
    
    def _center_dialog(self, parent):
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
    
    def _close_after_delay(self, duration):
        time.sleep(duration)
        self.dialog.destroy() 