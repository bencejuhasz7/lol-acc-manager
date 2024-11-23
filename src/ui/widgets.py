import customtkinter as ctk
import pyperclip
import json
from src.utils.constants import (
    COLORS, DIMENSIONS, PADDING, FONTS,
    REGULAR_BUTTON_STYLE, ICON_BUTTON_STYLE,
    DARK_BUTTON_STYLE, COPY_BUTTON_STYLE,
    CANCEL_BUTTON_STYLE
)

class AccountWidget:
    """Widget for displaying account information."""
    
    def __init__(self, parent, account_data, on_options, data_manager):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS["FRAME_BG"])
        self.frame.pack(fill="x", pady=PADDING["TINY"], padx=PADDING["TINY"])
        
        self.account_data = account_data
        self.data_manager = data_manager
        self.credentials_frame = None
        
        self._setup_header(on_options)
        self._create_credentials_frame()
    
    def _setup_header(self, on_options):
        header_frame = ctk.CTkFrame(self.frame, fg_color=COLORS["TRANSPARENT"])
        header_frame.pack(fill="x", pady=PADDING["TINY"], padx=PADDING["TINY"])
        
        # Account button with frame background color
        account_button_style = {
            "height": DIMENSIONS["ACCOUNT_BUTTON_HEIGHT"],
            "anchor": "w",
            "fg_color": COLORS["BUTTON_DARK"],
            "hover_color": COLORS["BUTTON_DARK_HOVER"]
        }
        
        self.account_button = ctk.CTkButton(
            header_frame,
            text=self.account_data["name"],
            command=self._toggle_credentials,
            **account_button_style
        )
        self.account_button.pack(side="left", fill="x", expand=True, padx=PADDING["TINY"])
        
        # Info button
        info_button = ctk.CTkButton(
            header_frame,
            text="ℹ",  # Info symbol
            command=self._show_info,
            **ICON_BUTTON_STYLE
        )
        info_button.pack(side="right", padx=PADDING["TINY"])
        
        # Options button
        options_button = ctk.CTkButton(
            header_frame,
            text="⚙",
            command=on_options,
            **ICON_BUTTON_STYLE
        )
        options_button.pack(side="right", padx=(0, PADDING["TINY"]))
    
    def _create_credentials_frame(self):
        self.credentials_frame = ctk.CTkFrame(self.frame)
        
        # ID Field
        id_frame = ctk.CTkFrame(self.credentials_frame)
        id_frame.pack(fill="x", pady=PADDING["TINY"], padx=PADDING["TINY"])
        
        # ID Label
        id_label = ctk.CTkLabel(
            id_frame,
            text="ID:",
            width=DIMENSIONS["LABEL_WIDTH"],
            font=FONTS["NORMAL"]
        )
        id_label.pack(side="left", padx=PADDING["LABEL_X"])
        
        # ID Entry
        id_entry = ctk.CTkEntry(id_frame)
        id_entry.insert(0, self.account_data["id"])
        id_entry.configure(state="readonly")
        id_entry.pack(side="left", fill="x", expand=True, padx=PADDING["TINY"])
        
        # ID Copy Button
        ctk.CTkButton(
            id_frame,
            text="Copy",
            command=lambda: self._copy_with_tracking("id", self.account_data["id"]),
            **COPY_BUTTON_STYLE
        ).pack(side="right", padx=PADDING["TINY"])
        
        # Password Field
        pass_frame = ctk.CTkFrame(self.credentials_frame)
        pass_frame.pack(fill="x", pady=PADDING["TINY"], padx=PADDING["TINY"])
        
        # Password Label
        pass_label = ctk.CTkLabel(
            pass_frame,
            text="PW:",
            width=DIMENSIONS["LABEL_WIDTH"],
            font=FONTS["NORMAL"]
        )
        pass_label.pack(side="left", padx=PADDING["LABEL_X"])
        
        # Password Entry
        self.pass_entry = ctk.CTkEntry(pass_frame, show="•")
        self.pass_entry.insert(0, self.account_data["password"])
        self.pass_entry.configure(state="readonly")
        self.pass_entry.pack(side="left", fill="x", expand=True, padx=PADDING["TINY"])
        
        # Show/Hide Button
        self.show_pass_btn = ctk.CTkButton(
            pass_frame,
            text="Show",
            command=self._toggle_password,
            **COPY_BUTTON_STYLE
        )
        self.show_pass_btn.pack(side="left", padx=(PADDING["TINY"], PADDING["TINY"]))
        
        # Password Copy Button
        ctk.CTkButton(
            pass_frame,
            text="Copy",
            command=lambda: self._copy_with_tracking("password", self.account_data["password"]),
            **COPY_BUTTON_STYLE
        ).pack(side="right", padx=PADDING["TINY"])
    
    def _toggle_credentials(self):
        if self.credentials_frame.winfo_viewable():
            self.credentials_frame.pack_forget()
        else:
            self.credentials_frame.pack(fill="x", pady=PADDING["TINY"], padx=PADDING["TINY"])
    
    def _toggle_password(self):
        current_show = self.pass_entry.cget("show")
        if current_show == "•":
            self.pass_entry.configure(show="")
            self.show_pass_btn.configure(text="Hide")
        else:
            self.pass_entry.configure(show="•")
            self.show_pass_btn.configure(text="Show")
    
    def destroy(self):
        self.frame.destroy()
    
    def _copy_with_tracking(self, field_type, text):
        """Copy text and track usage."""
        pyperclip.copy(text)
        
        # Update usage counters
        current_server = self.data_manager.current_server
        for account in self.data_manager.accounts_data[current_server]:
            if account["id"] == self.account_data["id"]:
                if "usage" not in account:
                    account["usage"] = {
                        "id_copies": 0,
                        "password_copies": 0,
                        "total_copies": 0
                    }
                if field_type == "id":
                    account["usage"]["id_copies"] += 1
                elif field_type == "password":
                    account["usage"]["password_copies"] += 1
                account["usage"]["total_copies"] += 1
                self.data_manager.save_accounts()
                break
    
    def _show_info(self):
        """Show account usage and rank information."""
        usage = self.account_data.get("usage", {
            "id_copies": 0,
            "password_copies": 0,
            "total_copies": 0
        })
        
        # Default to "No data" instead of "Unranked"
        ranks = self.account_data.get("ranks", {
            "solo": {"rank": "No data", "lp": ""},
            "flex": {"rank": "No data", "lp": ""}
        })
        
        # Load rank mapping
        rank_mapping = {}
        try:
            with open(self.data_manager.root_dir / "data" / "rank_mapping.json", 'r') as f:
                rank_mapping = json.load(f)
        except Exception:
            pass
        
        # Get mapped rank names if available
        solo_rank = ranks["solo"]["rank"]
        flex_rank = ranks["flex"]["rank"]
        
        if solo_rank != "No data" and solo_rank != "Unranked":
            solo_rank = rank_mapping.get(solo_rank.lower(), {}).get("clean_name", solo_rank)
        if flex_rank != "No data" and flex_rank != "Unranked":
            flex_rank = rank_mapping.get(flex_rank.lower(), {}).get("clean_name", flex_rank)
        
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Account Info")
        dialog.geometry(DIMENSIONS["INFO_DIALOG_SIZE"])
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.frame.winfo_rootx() + (self.frame.winfo_width() - dialog.winfo_width()) // 2
        y = self.frame.winfo_rooty() + (self.frame.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Usage statistics in a frame with lighter background
        usage_frame = ctk.CTkFrame(dialog, fg_color=COLORS["BUTTON_PRIMARY"])
        usage_frame.pack(pady=(PADDING["DEFAULT"], PADDING["SMALL"]), padx=PADDING["DEFAULT"], fill="x")
        
        # Usage info (divided by 2)
        usage_label = ctk.CTkLabel(
            usage_frame,
            text=f"Usage: {usage['total_copies'] // 2}",  # Integer division by 2
            font=FONTS["DIALOG"]
        )
        usage_label.pack(pady=2)
        
        # Soloq rank info
        soloq_frame = ctk.CTkFrame(dialog, fg_color=COLORS["BUTTON_PRIMARY"])
        soloq_frame.pack(pady=PADDING["SMALL"], padx=PADDING["DEFAULT"], fill="x")
        soloq_label = ctk.CTkLabel(
            soloq_frame,
            text=f"Solo: {solo_rank} {ranks['solo']['lp']}",
            font=FONTS["DIALOG"]
        )
        soloq_label.pack(pady=2)
        
        # Flex rank info
        flex_frame = ctk.CTkFrame(dialog, fg_color=COLORS["BUTTON_PRIMARY"])
        flex_frame.pack(pady=PADDING["SMALL"], padx=PADDING["DEFAULT"], fill="x")
        flex_label = ctk.CTkLabel(
            flex_frame,
            text=f"Flex: {flex_rank} {ranks['flex']['lp']}",
            font=FONTS["DIALOG"]
        )
        flex_label.pack(pady=2)
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            **CANCEL_BUTTON_STYLE
        )
        close_btn.pack(pady=PADDING["SMALL"])
        
        dialog.bind("<Escape>", lambda e: dialog.destroy())