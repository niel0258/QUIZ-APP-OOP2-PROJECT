import json
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QWidget,
)


# ---------- Data classes ----------
class Question:
    def __init__(self, question="", right_answer=None):
        self.question = question
        self.type = "base"
        self.right_answer = right_answer

    def to_dict(self):
        return {
            "question": self.question,
            "type": self.type,
            "right_answer": self.right_answer,
        }


class MultipleChoice(Question):
    def __init__(self, question="", choices=None, right_answer=None):
        super().__init__(question, right_answer)
        self.type = "multiple_choice"
        self.choices = choices or []

    def to_dict(self):
        d = super().to_dict()
        d["choices"] = self.choices
        return d


class TrueFalse(Question):
    def __init__(self, question="", right_answer=True):
        super().__init__(question, right_answer)
        self.type = "true_false"


# ---------- GUI ----------
class QuizCreation(QWidget):
    NUM_CHOICES = 4

    def __init__(self):
        super().__init__()
        self.title = "Quiz Creation"
        self.questions = []
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.title)
        layout = QGridLayout(self)

        # Question type
        layout.addWidget(QLabel("Type:"), 0, 0)
        self.type_box = QComboBox()
        self.type_box.addItems(["Multiple Choice", "True/False"])
        self.type_box.currentIndexChanged.connect(self.on_type_changed)
        layout.addWidget(self.type_box, 0, 1)

        # Question text
        layout.addWidget(QLabel("Question:"), 1, 0)
        self.question_edit = QLineEdit()
        layout.addWidget(self.question_edit, 1, 1)

        # Choice fields
        self.choice_labels = []
        self.choice_edits = []
        for i in range(self.NUM_CHOICES):
            label = QLabel(f"Choice {chr(65 + i)}:")
            edit = QLineEdit()
            layout.addWidget(label, 2 + i, 0)
            layout.addWidget(edit, 2 + i, 1)
            self.choice_labels.append(label)
            self.choice_edits.append(edit)

        # Right answer
        layout.addWidget(QLabel("Right answer:"), 6, 0)
        self.answer_box = QComboBox()
        layout.addWidget(self.answer_box, 6, 1)

        # Buttons
        add_btn = QPushButton("Add Question")
        add_btn.clicked.connect(self.add_question)
        layout.addWidget(add_btn, 7, 0, 1, 2)

        # List of added questions
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget, 8, 0, 1, 2)

        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_question)
        layout.addWidget(delete_btn, 9, 0)

        save_btn = QPushButton("Save Quiz...")
        save_btn.clicked.connect(self.save_quiz)
        layout.addWidget(save_btn, 9, 1)

        self.on_type_changed()
        self.show()

    def on_type_changed(self):
        is_mc = self.type_box.currentText() == "Multiple Choice"
        for label, edit in zip(self.choice_labels, self.choice_edits):
            label.setVisible(is_mc)
            edit.setVisible(is_mc)

        self.answer_box.clear()
        if is_mc:
            self.answer_box.addItems([chr(65 + i) for i in range(self.NUM_CHOICES)])
        else:
            self.answer_box.addItems(["True", "False"])

    def add_question(self):
        text = self.question_edit.text().strip()
        if not text:
            QMessageBox.warning(self, "Missing info", "Enter a question.")
            return

        if self.type_box.currentText() == "Multiple Choice":
            choices = [e.text().strip() for e in self.choice_edits]
            if not all(choices):
                QMessageBox.warning(self, "Missing info", "Fill in all choices.")
                return
            q = MultipleChoice(text, choices, self.answer_box.currentIndex())
        else:
            q = TrueFalse(text, self.answer_box.currentText() == "True")

        self.questions.append(q)
        self.list_widget.addItem(f"[{q.type}] {q.question}")
        self.clear_inputs()

    def clear_inputs(self):
        self.question_edit.clear()
        for e in self.choice_edits:
            e.clear()

    def delete_question(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)
            del self.questions[row]

    def save_quiz(self):
        if not self.questions:
            QMessageBox.warning(self, "Nothing to save", "Add a question first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Quiz", "quiz.json", "JSON Files (*.json)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump([q.to_dict() for q in self.questions], f, indent=2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = QuizCreation()
    sys.exit(app.exec())
