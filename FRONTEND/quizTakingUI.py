import sys
import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QRadioButton, QFrame, QButtonGroup, QScrollArea, QMessageBox
)

class QuizApp(QMainWindow):
    def __init__(self, csv_filepath):
        super().__init__()
        self.setWindowTitle("Quiz Taking")
        self.resize(1280, 720)

        #Load questions
        self.questions = self.load_questions(csv_filepath)
        self.totalQuestions = len(self.questions)
        self.currentQuestion = 0

        #Selected answer dictionary
        self.user_answers = {}

        self.option_frames = []
        self.nav_buttons = []

        if self.totalQuestions == 0:
            QMessageBox.critical(self, "Error", "No valid questions found in the CSV file.")
            sys.exit(1)

        self.UI()
        self.display_question(self.currentQuestion)

    def load_questions(self, filepath):
            questions = []
            type_mapping = {
                "MCQ": "Multiple Choice",
                "T&F": "True or False",
            }
            try:
                with open(filepath, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        raw_type = row['Question Type'].strip()
                        
                        q_type = type_mapping.get(raw_type.upper(), raw_type)

                        options = [
                            row['Option 1'].strip(),
                            row['Option 2'].strip(),
                            row['Option 3'].strip(),
                            row['Option 4'].strip()
                        ]
                        options = [opt for opt in options if opt]

                        questions.append({
                            "type": q_type,
                            "question": row['Question'].strip(),
                            "options": options,
                            "correct": row['Correct Option'].strip()
                        })
            except Exception as e:
                print(f"Error loading CSV file: {e}")
            return questions

    def UI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #f4f6f8;")

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        quiz_card = QFrame()
        quiz_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)
        self.card_layout = QVBoxLayout(quiz_card)
        self.card_layout.setContentsMargins(24, 20, 24, 24)

        card_top = QHBoxLayout()
        self.q_count_label = QLabel(f"Question 1 of {self.totalQuestions}")
        self.q_count_label.setStyleSheet("color: #64748b; font-size: 13px; font-weight: bold; border: none;")
        card_top.addWidget(self.q_count_label)
        card_top.addStretch()
        self.card_layout.addLayout(card_top)

        subheader = QHBoxLayout()
        self.q_type_label = QLabel("Multiple Choice")
        self.q_type_label.setStyleSheet("color: #334155; font-size: 13px; font-weight: bold; border: none;")
        subheader.addWidget(self.q_type_label)
        subheader.addStretch()
        self.card_layout.addLayout(subheader)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #f1f5f9; border: none; min-height: 1px; max-height: 1px;")
        self.card_layout.addWidget(divider)

        self.q_title = QLabel("Question")
        self.q_title.setWordWrap(True)
        self.q_title.setStyleSheet("color: #0f172a; font-size: 20px; font-weight: bold; border: none; margin-top: 10px;")
        self.card_layout.addWidget(self.q_title)

        q_sub = QLabel("Select one answer.")
        q_sub.setStyleSheet("color: #64748b; font-size: 13px; border: none; margin-bottom: 10px;")
        self.card_layout.addWidget(q_sub)

        self.options_container = QWidget()
        self.options_container.setStyleSheet("border: none; background: transparent;")
        self.options_layout = QVBoxLayout(self.options_container)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.setSpacing(10)
        
        self.button_group = QButtonGroup(self)
        self.button_group.idToggled.connect(self.on_option_selected)

        self.card_layout.addWidget(self.options_container)
        self.card_layout.addStretch()

        left_layout.addWidget(quiz_card)

        action_bar = QHBoxLayout()
        
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #f1f5f9; }
            QPushButton:disabled { background-color: #e2e8f0; color: #94a3b8; }
        """)
        self.btn_prev.clicked.connect(self.prev_question)

        self.btn_next = QPushButton("Next")
        self.btn_next.setStyleSheet("""
            QPushButton {
                background-color: #6b1d24;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #52151b; }
            QPushButton:disabled { background-color: #d19ba0; }
        """)
        self.btn_next.clicked.connect(self.handle_next_or_submit)

        action_bar.addWidget(self.btn_prev)
        action_bar.addStretch()
        action_bar.addWidget(self.btn_next)

        left_layout.addLayout(action_bar)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)
        top_layout = QVBoxLayout(sidebar)
        top_layout.setContentsMargins(16, 16, 16, 16)
        top_layout.setSpacing(12)

        nav_header = QHBoxLayout()
        nav_title = QLabel("Quiz navigation")
        nav_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #0f172a; border: none;")
        
        self.answered_count = QLabel("0 answered")
        self.answered_count.setStyleSheet("font-size: 12px; font-weight: bold; color: #ca8a04; border: none;")
        
        nav_header.addWidget(nav_title)
        nav_header.addStretch()
        nav_header.addWidget(self.answered_count)
        top_layout.addLayout(nav_header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(6)

        for idx in range(self.totalQuestions):
            item_btn = QPushButton(f"   ○   Question {idx + 1}")
            item_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            item_btn.clicked.connect(lambda _, q_idx=idx: self.goto_question(q_idx))
            list_layout.addWidget(item_btn)
            self.nav_buttons.append(item_btn)

        list_layout.addStretch()
        scroll_area.setWidget(list_widget)
        top_layout.addWidget(scroll_area)

        
        right_layout.addWidget(sidebar)

        main_layout.addWidget(left_container, 8)
        main_layout.addWidget(right_container, 2)

    def display_question(self, index):
        q_data = self.questions[index]

        self.q_count_label.setText(f"Question {index + 1} of {self.totalQuestions}")
        self.q_type_label.setText(q_data["type"])
        self.q_title.setText(q_data["question"])

        for frame in self.option_frames:
            self.options_layout.removeWidget(frame)
            frame.deleteLater()
        self.option_frames.clear()

        for btn in self.button_group.buttons():
            self.button_group.removeButton(btn)

        for i, text in enumerate(q_data["options"]):
            opt_frame = QFrame()
            opt_layout = QHBoxLayout(opt_frame)
            opt_layout.setContentsMargins(12, 12, 12, 12)

            radio = QRadioButton(text)
            self.button_group.addButton(radio, i)

            is_selected = (self.user_answers.get(index) == i)
            radio.setChecked(is_selected)
            self.set_frame_style(opt_frame, is_selected=is_selected)

            opt_layout.addWidget(radio)
            self.options_layout.addWidget(opt_frame)
            self.option_frames.append(opt_frame)

        self.btn_prev.setEnabled(index > 0)
        
        if index == self.totalQuestions - 1:
            self.btn_next.setText("Submit quiz")
        else:
            self.btn_next.setText("Next")
        self.btn_next.setEnabled(True)

        self.update_sidebar()

    def update_sidebar(self):
        answered = len(self.user_answers)
        self.answered_count.setText(f"{answered} answered")

        for idx, btn in enumerate(self.nav_buttons):
            is_current = (idx == self.currentQuestion)
            is_answered = idx in self.user_answers

            if is_current:
                btn.setText(f"   ●   Question {idx + 1}")
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left; padding: 8px 12px;
                        background-color: #fcf2f3; color: #6b1d24;
                        border: 1px solid #f2c2c5; border-radius: 6px;
                        font-weight: bold; font-size: 13px;
                    }
                """)
            elif is_answered:
                btn.setText(f"   ✓   Question {idx + 1}")
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left; padding: 8px 12px;
                        background-color: #fef9c3; color: #ca8a04;
                        border: 1px solid #facc15; border-radius: 6px;
                        font-weight: 500; font-size: 13px;
                    }
                """)
            else:
                btn.setText(f"   ○   Question {idx + 1}")
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left; padding: 8px 12px;
                        background-color: #ffffff; color: #64748b;
                        border: 1px solid #f1f5f9; border-radius: 6px;
                        font-size: 13px;
                    }
                    QPushButton:hover { background-color: #f8fafc; border-color: #cbd5e1; }
                """)

    def set_frame_style(self, frame, is_selected):
        if is_selected:
            frame.setStyleSheet("""
                QFrame {
                    background-color: #fcf2f3;
                    border: 2px solid #6b1d24;
                    border-radius: 8px;
                }
                QRadioButton {
                    color: #52151b;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                }
                QRadioButton::indicator:checked {
                    background-color: #6b1d24;
                    border: 2px solid #6b1d24;
                    border-radius: 7px;
                    width: 10px;
                    height: 10px;
                }
            """)
        else:
            frame.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                }
                QFrame:hover {
                    border-color: #cbd5e1;
                    background-color: #f8fafc;
                }
                QRadioButton {
                    color: #334155;
                    font-size: 14px;
                    border: none;
                }
            """)

    def on_option_selected(self, option_id, checked):
        if checked:
            #Store choice
            self.user_answers[self.currentQuestion] = option_id
            for idx, frame in enumerate(self.option_frames):
                self.set_frame_style(frame, is_selected=(idx == option_id))
            self.update_sidebar()

    def handle_next_or_submit(self):
        if self.currentQuestion == self.totalQuestions - 1:
            self.submit_quiz()
        else:
            self.next_question()

    def next_question(self):
        if self.currentQuestion < self.totalQuestions - 1:
            self.currentQuestion += 1
            self.display_question(self.currentQuestion)

    def prev_question(self):
        if self.currentQuestion > 0:
            self.currentQuestion -= 1
            self.display_question(self.currentQuestion)

    def goto_question(self, index):
        self.currentQuestion = index
        self.display_question(self.currentQuestion)

    def submit_quiz(self):
        unanswered = self.totalQuestions - len(self.user_answers)
        
        message = "Are you sure you want to submit your quiz?"
        if unanswered > 0:
            message = f"You have {unanswered} unanswered question(s).\n\nAre you sure you want to submit?"

        reply = QMessageBox.question(
            self, 
            "Confirm Submission", 
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        results = {
            "total_questions": self.totalQuestions,
            "answered_count": len(self.user_answers),
            "user_answers": {}
        }

        for i, q in enumerate(self.questions):
            selected_idx = self.user_answers.get(i)
            
            if selected_idx is not None:
                selected_option = q["options"][selected_idx]
                is_correct = (selected_option.lower() == q["correct"].lower())
            else:
                selected_option = None
                is_correct = False

            results["user_answers"][i] = {
                "question": q["question"],
                "selected_index": selected_idx,
                "selected_option": selected_option,
                "correct_option": q["correct"],
                "is_correct": is_correct
            }

        print("Quiz Submitted!")

        return results


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp("questions.csv")
    window.show()
    sys.exit(app.exec())