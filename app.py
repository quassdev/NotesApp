import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QTextEdit, QTimeEdit, QMessageBox
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QIcon
from plyer import notification

class NoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes App")
        self.setGeometry(100, 100, 800, 600)  # Main window size
        self.setStyleSheet("background-color: black; color: gold;")

        # Set an icon for the application (provide the correct path to your icon file)
        self.setWindowIcon(QIcon("path/to/your/icon.png"))  # Change this to your icon's path

        # Create layout
        self.layout = QVBoxLayout()

        # Title input
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Title")
        self.title_input.setStyleSheet("border-radius: 5px; padding: 10px; font-size: 20px;")
        self.title_input.setFixedHeight(60)

        # Content input
        self.content_input = QTextEdit(self)
        self.content_input.setPlaceholderText("Content")
        self.content_input.setStyleSheet("border-radius: 5px; padding: 10px; font-size: 16px;")
        self.content_input.setFixedHeight(200)

        # Time input for reminder
        self.reminder_time_input = QTimeEdit(self)
        self.reminder_time_input.setDisplayFormat("HH:mm")
        self.reminder_time_input.setStyleSheet("border-radius: 5px; padding: 10px; font-size: 20px;")
        self.reminder_time_input.setFixedHeight(60)

        # Add note button
        self.add_note_button = QPushButton("Add Note", self)
        self.add_note_button.setStyleSheet("background-color: #FF9800; color: white; border-radius: 5px; padding: 15px; font-size: 18px;")
        self.add_note_button.clicked.connect(self.add_note)

        # Notes list
        self.notes_list = QListWidget(self)
        self.notes_list.setStyleSheet("background-color: #333; color: white; font-size: 16px;")

        # Add widgets to layout
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.content_input)
        self.layout.addWidget(self.reminder_time_input)  # Add reminder time input
        self.layout.addWidget(self.add_note_button)
        self.layout.addWidget(self.notes_list)

        # Set layout to the main window
        self.setLayout(self.layout)

        # Initialize a timer for notifications
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(1000)  # Check every second

        # Store notes with their reminder times
        self.notes_with_reminders = {}

    def add_note(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        reminder_time = self.reminder_time_input.time().toString("HH:mm")

        if title and content:
            note = f"{title}: {content} (Reminder: {reminder_time})"
            self.notes_list.addItem(note)

            # Store the note with its reminder time
            self.notes_with_reminders[note] = reminder_time

            # Clear the inputs
            self.title_input.clear()
            self.content_input.clear()
            self.reminder_time_input.clear()  # Clear the time input

        else:
            QMessageBox.warning(self, "Warning", "Title and content cannot be empty.")

    def check_notifications(self):
        current_time = QTime.currentTime().toString("HH:mm")
        for note, reminder_time in list(self.notes_with_reminders.items()):
            if reminder_time == current_time:
                self.show_notification(note)
                # Remove the note from reminders after showing the notification
                del self.notes_with_reminders[note]

    def show_notification(self, note):
        title, content = note.split(": ", 1)
        notification.notify(
            title=title,
            message=f"It's time for your note: {content.split(' (Reminder: ')[0]}!",
            timeout=10,
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())
