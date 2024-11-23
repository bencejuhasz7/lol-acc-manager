# Colors
COLORS = {
    # Button colors
    "BUTTON_PRIMARY": "#3E4654",  # Lighter blue-gray for regular buttons
    "BUTTON_HOVER": "#4C566A",    # Hover color for regular buttons
    "BUTTON_DARK": "#2B2B2B",     # Dark gray for some buttons
    "BUTTON_DARK_HOVER": "#3B3B3B",  # Hover color for dark buttons
    "BUTTON_DELETE": "#b22222",    # Red color for delete button
    "BUTTON_DELETE_HOVER": "#8b0000",  # Darker red for delete hover
    "CANCEL_BUTTON": "#555555",    # Gray for cancel buttons
    "CANCEL_BUTTON_HOVER": "#666666",  # Lighter gray for cancel hover
    
    # Dropdown colors
    "DROPDOWN_BG": "#3E4654",      # Dropdown background
    "DROPDOWN_BUTTON": "#2E3440",  # Dropdown button color
    "DROPDOWN_HOVER": "#4C566A",   # Dropdown hover color
    
    # Frame colors
    "FRAME_BG": "#2B2B2B",        # Background for frames
    "TRANSPARENT": "transparent"    # Transparent background
}

# Dimensions
DIMENSIONS = {
    # Main window
    "WINDOW_SIZE": "550x600",
    
    # Buttons
    "BUTTON_HEIGHT": 40,
    "BUTTON_WIDTH": 120,
    "ICON_BUTTON_SIZE": 32,
    "COPY_BUTTON_WIDTH": 60,
    "COPY_BUTTON_HEIGHT": 28,
    "ACCOUNT_BUTTON_HEIGHT": 28,
    
    # Dropdowns
    "DROPDOWN_WIDTH": 120,
    "DROPDOWN_HEIGHT": 32,
    
    # Dialogs
    "DIALOG_WIDTH": 300,
    "ADD_SERVER_DIALOG_SIZE": "350x280",
    "INPUT_DIALOG_SIZE": "300x280",
    "OPTIONS_DIALOG_SIZE": "350x300",
    "LOADING_DIALOG_SIZE": "300x150",
    "ORDER_DIALOG_SIZE": "300x350",
    "INFO_DIALOG_SIZE": "300x250",
    
    # Other
    "SCROLLABLE_FRAME_HEIGHT": 300,
    "LABEL_WIDTH": 50
}

# Padding and margins
PADDING = {
    "DEFAULT": 20,
    "SMALL": 10,
    "TINY": 5,
    "BUTTON_X": 10,
    "DIALOG_TOP": (20, 30),
    "DIALOG_BOTTOM": (30, 20),
    "LABEL_X": 5
}

# Font configurations
FONTS = {
    "HEADER": ("Arial", 16, "bold"),
    "NORMAL": ("Arial", 13),
    "DIALOG": ("Arial", 14, "bold")
}

# Button styles
CANCEL_BUTTON_STYLE = {
    "fg_color": COLORS["CANCEL_BUTTON"],
    "hover_color": COLORS["CANCEL_BUTTON_HOVER"]
}

DROPDOWN_STYLE = {
    "fg_color": COLORS["DROPDOWN_BG"],
    "button_color": COLORS["DROPDOWN_BUTTON"],
    "button_hover_color": COLORS["DROPDOWN_HOVER"],
    "dropdown_fg_color": COLORS["DROPDOWN_BG"],
    "dropdown_hover_color": COLORS["DROPDOWN_HOVER"],
    "dropdown_text_color": "white",
    "font": FONTS["NORMAL"],
    "width": DIMENSIONS["DROPDOWN_WIDTH"],
    "height": DIMENSIONS["DROPDOWN_HEIGHT"]
}

REGULAR_BUTTON_STYLE = {
    "fg_color": COLORS["BUTTON_PRIMARY"],
    "hover_color": COLORS["BUTTON_HOVER"]
}

DARK_BUTTON_STYLE = {
    "fg_color": COLORS["BUTTON_DARK"],
    "hover_color": COLORS["BUTTON_DARK_HOVER"]
}

DELETE_BUTTON_STYLE = {
    "fg_color": COLORS["BUTTON_DELETE"],
    "hover_color": COLORS["BUTTON_DELETE_HOVER"]
}

ICON_BUTTON_STYLE = {
    "width": DIMENSIONS["ICON_BUTTON_SIZE"],
    "height": DIMENSIONS["ICON_BUTTON_SIZE"],
    "fg_color": COLORS["BUTTON_PRIMARY"],
    "hover_color": COLORS["BUTTON_HOVER"]
}

COPY_BUTTON_STYLE = {
    "width": DIMENSIONS["COPY_BUTTON_WIDTH"],
    "height": DIMENSIONS["COPY_BUTTON_HEIGHT"],
    "fg_color": COLORS["BUTTON_PRIMARY"],
    "hover_color": COLORS["BUTTON_HOVER"]
} 