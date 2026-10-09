import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
    QStackedWidget,
    QGraphicsDropShadowEffect,
    QMessageBox,
)
from users import verify_user, create_user

WINDOW_SIZE = (980, 550)  

LOGIN_THEME = ("#8B2630", "#370404", "#fff")  
REGISTER_THEME = LOGIN_THEME
 
 
def _password_field() -> QLineEdit:
    edit = QLineEdit()
    edit.setEchoMode(QLineEdit.EchoMode.Password)
    return edit
 
 
def _page_style(c1: str, c2: str, text: str) -> str:
    return f"""
    QWidget#page {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {c1}, stop:1 {c2}); }}
    QLabel {{ color: {text}; font-family: 'Segoe UI', Arial; background: transparent; }}
    QLabel#header {{ font-size: 22px; padding: 8px 12px; border-bottom: 2px solid rgba(0,0,0,70); }}
    QLabel#pageTitle {{ font-size: 36px; font-weight: bold; }}
    QLabel#hint {{ font-size: 13px; }}
    QLabel#cardTitle {{ font-size: 22px; }}
    QLabel#field {{ font-size: 17px; }}
    QFrame#card {{ background: #ebebeb; border: 3px solid #FFD700; border-radius: 24px; }}
    QFrame#card QLabel {{ border: none; color: #000; }}
    QLineEdit {{ background: white; border: none; border-radius: 15px; padding: 4px 12px;
                min-height: 22px; font-size: 14px; color: #000; }}
    QComboBox {{ background: white; border: none; padding: 6px 10px; font-size: 13px; color: #000; }}
    QPushButton#primary {{ background: #000; color: white; border: none; border-radius: 14px;
                          font-size: 13px; font-weight: bold; min-height: 28px; }}
    QPushButton#primary:hover {{ background: #222; }}
    QPushButton#link {{ background: transparent; border: none; color: white;
                       text-decoration: underline; font-size: 13px; }}
    """
 
 
class LoginUI(QWidget):
    logged_in = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
 
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.pages = QStackedWidget()
        outer.addWidget(self.pages)
 
        # Build UI Screens
        self.pages.addWidget(self._create_register_page())  
        self.pages.addWidget(self._create_login_page())   
        
        
    # ----page builder (header, title, hint, card, button, link)-----

    def _build_page(self, theme, title, hint, rows, btn_text, on_btn, link_text, on_link) -> QWidget:
        page = QWidget()
        page.setObjectName("page")
        page.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        page.setStyleSheet(_page_style(*theme))
 
        v = QVBoxLayout(page)
        v.setContentsMargins(0, 0, 0, 20)
        v.setSpacing(6)
 
        header = QLabel("Quiz")
        header.setObjectName("header")
        v.addWidget(header)
        v.addSpacing(10)
 
        t = QLabel(title)
        t.setObjectName("pageTitle")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(t)
 

        hint_row = QHBoxLayout()
        hint_row.addStretch()
        h = QLabel(hint)
        h.setObjectName("hint")
        h.setFixedWidth(360)
        hint_row.addWidget(h)
        hint_row.addStretch()
        v.addLayout(hint_row)
 
        # Card
        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(360, 290)
        glow = QGraphicsDropShadowEffect(card)
        glow.setBlurRadius(18)
        glow.setOffset(-6, 6)
        glow.setColor(QColor(255, 215, 0, 150))
        card.setGraphicsEffect(glow)
 
        grid = QGridLayout(card)
        grid.setContentsMargins(14, 14, 14, 14)
        grid.setVerticalSpacing(14)
        card_title = QLabel("  ")
        card_title.setObjectName("cardTitle")
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(card_title, 0, 0, 1, 2)
        grid.setRowStretch(1, 1)
        for i, (label, widget) in enumerate(rows, start=2):
            lbl = QLabel(label)
            lbl.setObjectName("field")
            grid.addWidget(lbl, i, 0)
            grid.addWidget(widget, i, 1)
        grid.setRowStretch(len(rows) + 2, 1)
        grid.setColumnStretch(1, 1)
 
        card_row = QHBoxLayout()
        card_row.addStretch()
        card_row.addWidget(card)
        card_row.addStretch()
        v.addLayout(card_row)
        v.addSpacing(6)
 
        # Primary button
        btn = QPushButton(btn_text)
        btn.setObjectName("primary")
        btn.setFixedWidth(230)
        if on_btn:
            btn.clicked.connect(on_btn)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn)
        btn_row.addStretch()
        v.addLayout(btn_row)
 
        # Link
        link = QPushButton(link_text)
        link.setObjectName("link")
        link.setFlat(True)
        link.clicked.connect(on_link)
        v.addWidget(link, alignment=Qt.AlignmentFlag.AlignCenter)
 
        v.addStretch()
        return page
 

    # -----------------------------PAGE 0: Register----------------------
    
    def do_register(self):
        username = self.reg_user.text().strip()
        password = self.reg_pass.text()
        role = self.reg_role.currentText()
 
        if not username or not password:
            QMessageBox.critical(self, "Missing Information", "Username and password are required.")
        elif len(password) < 6:
            QMessageBox.critical(self, "Weak Password", "Password must be at least 6 characters.")
        elif not create_user(username, password, role):
            QMessageBox.critical(self, "Username Taken", "That username already exists.")
        else:
            QMessageBox.information(self, "Account Created", "Account created! You can now log in.")
            self.reg_user.clear()
            self.reg_pass.clear()
            self.login_user.setText(username)        
            self.pages.setCurrentIndex(1)
            
            
    def _create_register_page(self) -> QWidget:
        self.reg_user = QLineEdit()
        self.reg_pass = _password_field()
        self.reg_pass.setPlaceholderText("(min. 6 characters)") 
        self.reg_pass.returnPressed.connect(self.do_register)
        self.reg_role = QComboBox()
        self.reg_role.addItems(["Student", "Teacher"])
 
        return self._build_page(
            REGISTER_THEME,
            "Register",
            "Please Register to Login",
            [("Username", self.reg_user), ("Password", self.reg_pass), ("Role", self.reg_role)],
            "Sign-up", self.do_register,
            "Already have an account? Log in",
            lambda: self.pages.setCurrentIndex(1),   
            
        )
        
 
    # -----------------------------PAGE 1: Login----------------------
    def do_login(self):
        username = self.login_user.text().strip()
        password = self.login_pass.text()
 
        if not username or not password:
            QMessageBox.critical(self, "Missing Information", "Enter your username and password.")
            return
 
        role = verify_user(username, password)      
        if role is None:
            QMessageBox.critical(self, "Login Failed", "Incorrect username or password.")
            self.login_pass.clear()
            return
 
        self.reset()
        self.logged_in.emit(username, role)  
    
    
    def _create_login_page(self) -> QWidget:
        self.login_user = QLineEdit()
        self.login_pass = _password_field()
        self.login_pass.returnPressed.connect(self.do_login)
 
        return self._build_page(
            LOGIN_THEME,
            "Login",
            "Please Log in to continue",
            [("Username", self.login_user), ("Password", self.login_pass)],
            "Log-in",
            self.do_login,                                     
            "Create an account",
            lambda: self.pages.setCurrentIndex(0),   
        )
        

    def reset(self):
        """Clear all fields and go back to the Register page (call this on log out)."""
        for w in (self.reg_user, self.reg_pass, self.login_user, self.login_pass):
            w.clear()
        self.reg_role.setCurrentIndex(0)
        self.pages.setCurrentIndex(0)
        
 
if __name__ == "__main__":
    from users import initialize_storage
    initialize_storage()   
    app = QApplication(sys.argv)
 
    window = LoginUI()
    window.resize(*WINDOW_SIZE)
    window.setWindowTitle("Quiz App")
    window.logged_in.connect(lambda u, r: print("Logged in:", u, r))
    window.show()
 
    sys.exit(app.exec())
