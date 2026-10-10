import sys
import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QRadioButton, QFrame, QButtonGroup, QScrollArea, QMessageBox
)

import styles as st

class QuizApp(QMainWindow):
    def __init__(self, csv_filepath):
        super().__init__()
        self.setWindowTitle("Quiz Taking")
        self.resize(1280, 720)

        self.quiz_title = "Quiz"
        self.subject_name = "Subject"

        self.questions = self.load_questions(csv_filepath)
        self.totalQuestions = len(self.questions)
        self.currentQuestion = 0

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
                for i, row in enumerate(reader):
                    if i == 0:
                        if 'Quiz Title' in row and row['Quiz Title'].strip():
                            self.quiz_title = row['Quiz Title'].strip()
                        if 'Subject Name' in row and row['Subject Name'].strip():
                            self.subject_name = row['Subject Name'].strip()

                    raw_type = row.get('Question Type', '').strip()
                    q_type = type_mapping.get(raw_type.upper(), raw_type)

                    options = [
                        row.get('Option 1', '').strip(),
                        row.get('Option 2', '').strip(),
                        row.get('Option 3', '').strip(),
                        row.get('Option 4', '').strip()
                    ]
                    options = [opt for opt in options if opt]

                    questions.append({
                        "type": q_type,
                        "question": row.get('Question', '').strip(),
                        "options": options,
                        "correct": row.get('Correct Option', '').strip()
                    })
        except Exception as e:
            print(f"Error loading CSV file: {e}")
        return questions

    def UI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet(st.MAIN_WINDOW)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        quiz_card = QFrame()
        quiz_card.setStyleSheet(st.CARD_FRAME)
        
        card_outer_layout = QVBoxLayout(quiz_card)
        card_outer_layout.setContentsMargins(0, 0, 0, 0)
        card_outer_layout.setSpacing(0)

        ribbon_frame = QFrame()
        ribbon_frame.setStyleSheet(st.RIBBON_CONTAINER)
        
        ribbon_layout = QHBoxLayout(ribbon_frame)
        ribbon_layout.setContentsMargins(24, 16, 24, 16)

        ribbon_left = QVBoxLayout()
        ribbon_left.setSpacing(4)

        self.ribbon_title = QLabel(self.quiz_title)
        self.ribbon_title.setStyleSheet(st.LABEL_RIBBON_TITLE)

        self.ribbon_subtitle = QLabel(self.subject_name)
        self.ribbon_subtitle.setStyleSheet(st.LABEL_RIBBON_SUBTITLE)

        ribbon_left.addWidget(self.ribbon_title)
        ribbon_left.addWidget(self.ribbon_subtitle)

        ribbon_right = QVBoxLayout()
        ribbon_right.setSpacing(4)
        ribbon_right.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.q_count_label = QLabel(f"Question 1 of {self.totalQuestions}")
        self.q_count_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold; border: none;")
        self.q_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.q_type_label = QLabel("Multiple Choice")
        self.q_type_label.setStyleSheet("color: #f2c2c5; font-size: 13px; font-weight: bold; border: none;")
        self.q_type_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        ribbon_right.addWidget(self.q_count_label)
        ribbon_right.addWidget(self.q_type_label)

        ribbon_layout.addLayout(ribbon_left)
        ribbon_layout.addStretch()
        ribbon_layout.addLayout(ribbon_right)

        card_outer_layout.addWidget(ribbon_frame)

        self.card_layout = QVBoxLayout()
        self.card_layout.setContentsMargins(24, 20, 24, 24)
        self.card_layout.setSpacing(10)

        self.q_title = QLabel("Question")
        self.q_title.setWordWrap(True)
        self.q_title.setStyleSheet(st.LABEL_TITLE)
        self.card_layout.addWidget(self.q_title)

        q_sub = QLabel("Select one answer.")
        q_sub.setStyleSheet(st.LABEL_MUTED + " margin-bottom: 10px;")
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

        card_outer_layout.addLayout(self.card_layout)
        left_layout.addWidget(quiz_card)

        action_bar = QHBoxLayout()
        
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.setStyleSheet(st.BTN_SECONDARY)
        self.btn_prev.clicked.connect(self.prev_question)

        self.btn_next = QPushButton("Next")
        self.btn_next.setStyleSheet(st.BTN_PRIMARY)
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
        sidebar.setStyleSheet(st.CARD_FRAME)
        top_layout = QVBoxLayout(sidebar)
        top_layout.setContentsMargins(16, 16, 16, 16)
        top_layout.setSpacing(12)

        nav_header = QHBoxLayout()
        nav_title = QLabel("Quiz navigation")
        nav_title.setStyleSheet(st.LABEL_SIDEBAR_HEADER)
        
        self.answered_count = QLabel("0 answered")
        self.answered_count.setStyleSheet(st.LABEL_COUNTER_ACTIVE)
        
        nav_header.addWidget(nav_title)
        nav_header.addStretch()
        nav_header.addWidget(self.answered_count)
        top_layout.addLayout(nav_header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(st.SIDEBAR_SCROLL_AREA)

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
            opt_frame.setStyleSheet(st.option_frame(is_selected))

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
                btn.setStyleSheet(st.nav_button("current"))
            elif is_answered:
                btn.setText(f"   ✓   Question {idx + 1}")
                btn.setStyleSheet(st.nav_button("answered"))
            else:
                btn.setText(f"   ○   Question {idx + 1}")
                btn.setStyleSheet(st.nav_button("default"))

    def on_option_selected(self, option_id, checked):
        if checked:
            self.user_answers[self.currentQuestion] = option_id
            for idx, frame in enumerate(self.option_frames):
                frame.setStyleSheet(st.option_frame(idx == option_id))
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
    window = QuizApp("questionsFormat.csv")
    window.show()
    sys.exit(app.exec())