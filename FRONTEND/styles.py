# styles.py

# --- Existing Styles ---
class Colors:
    PRIMARY = "#6b1d24"
    PRIMARY_HOVER = "#52151b"
    PRIMARY_LIGHT = "#fcf2f3"
    PRIMARY_BORDER = "#f2c2c5"
    PRIMARY_DISABLED = "#d19ba0"

    ACCENT = "#ca8a04"
    ACCENT_BG = "#fef9c3"
    ACCENT_BORDER = "#facc15"

    BG_MAIN = "#f4f6f8"
    CARD_BG = "#ffffff"
    HOVER_BG = "#f8fafc"

    TEXT_DARK = "#0f172a"
    TEXT_MUTED = "#64748b"
    TEXT_MEDIUM = "#334155"

    BORDER_LIGHT = "#e2e8f0"
    BORDER_DIVIDER = "#f1f5f9"
    BORDER_INPUT = "#cbd5e1"

MAIN_WINDOW = f"background-color: {Colors.BG_MAIN};"

CARD_FRAME = f"""
    QFrame {{
        background-color: {Colors.CARD_BG};
        border: 1px solid {Colors.BORDER_LIGHT};
        border-radius: 8px;
    }}
"""

DIVIDER = f"""
    background-color: {Colors.BORDER_DIVIDER};
    border: none;
    min-height: 1px;
    max-height: 1px;
"""

LABEL_TITLE = f"""
    color: {Colors.TEXT_DARK};
    font-size: 20px;
    font-weight: bold;
    border: none;
    margin-top: 10px;
"""

LABEL_SUBHEADER = f"""
    color: {Colors.TEXT_MEDIUM};
    font-size: 13px;
    font-weight: bold;
    border: none;
"""

LABEL_MUTED = f"""
    color: {Colors.TEXT_MUTED};
    font-size: 13px;
    border: none;
"""

LABEL_SIDEBAR_HEADER = f"""
    font-size: 15px;
    font-weight: bold;
    color: {Colors.TEXT_DARK};
    border: none;
"""

LABEL_COUNTER_ACTIVE = f"""
    font-size: 12px;
    font-weight: bold;
    color: {Colors.ACCENT};
    border: none;
"""

SIDEBAR_SCROLL_AREA = """
    QScrollArea {
        border: none;
        background-color: transparent;
    }
"""

BTN_PRIMARY = f"""
    QPushButton {{
        background-color: {Colors.PRIMARY};
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {Colors.PRIMARY_HOVER};
    }}
    QPushButton:disabled {{
        background-color: {Colors.PRIMARY_DISABLED};
    }}
"""

BTN_SECONDARY = f"""
    QPushButton {{
        background-color: {Colors.CARD_BG};
        color: {Colors.TEXT_MEDIUM};
        border: 1px solid {Colors.BORDER_INPUT};
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {Colors.BORDER_DIVIDER};
    }}
    QPushButton:disabled {{
        background-color: {Colors.BORDER_LIGHT};
        color: #94a3b8;
    }}
"""

# --- Ribbon Styles ---

RIBBON_CONTAINER = f"""
    QFrame {{
        background-color: {Colors.PRIMARY};
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        border: none;
    }}
"""

LABEL_RIBBON_TITLE = """
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    border: none;
"""

LABEL_RIBBON_SUBTITLE = """
    color: #f2c2c5;
    font-size: 13px;
    border: none;
"""

# --- Dynamic Helper Functions ---

def option_frame(is_selected: bool) -> str:
    if is_selected:
        return f"""
            QFrame {{
                background-color: {Colors.PRIMARY_LIGHT};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 8px;
            }}
            QRadioButton {{
                color: {Colors.PRIMARY_HOVER};
                font-size: 14px;
                font-weight: bold;
                border: none;
            }}
            QRadioButton::indicator:checked {{
                background-color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 7px;
                width: 10px;
                height: 10px;
            }}
        """
    return f"""
        QFrame {{
            background-color: {Colors.CARD_BG};
            border: 1px solid {Colors.BORDER_LIGHT};
            border-radius: 8px;
        }}
        QFrame:hover {{
            border-color: {Colors.BORDER_INPUT};
            background-color: {Colors.HOVER_BG};
        }}
        QRadioButton {{
            color: {Colors.TEXT_MEDIUM};
            font-size: 14px;
            border: none;
        }}
    """

def nav_button(state: str) -> str:
    base_padding = "text-align: left; padding: 8px 12px; border-radius: 6px; font-size: 13px;"
    
    if state == "current":
        return f"""
            QPushButton {{
                {base_padding}
                background-color: {Colors.PRIMARY_LIGHT};
                color: {Colors.PRIMARY};
                border: 1px solid {Colors.PRIMARY_BORDER};
                font-weight: bold;
            }}
        """
    elif state == "answered":
        return f"""
            QPushButton {{
                {base_padding}
                background-color: {Colors.ACCENT_BG};
                color: {Colors.ACCENT};
                border: 1px solid {Colors.ACCENT_BORDER};
                font-weight: 500;
            }}
        """
    else:
        return f"""
            QPushButton {{
                {base_padding}
                background-color: {Colors.CARD_BG};
                color: {Colors.TEXT_MUTED};
                border: 1px solid {Colors.BORDER_DIVIDER};
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER_BG};
                border-color: {Colors.BORDER_INPUT};
            }}
        """