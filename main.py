import sqlite3

from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys

from qtconsole.qtconsoleapp import QtCore


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui", self)
        self.calendarWidget.selectionChanged.connect(self.change_calendar_date)
        self.change_calendar_date()
        self.saveButton.clicked.connect(self.save_changes)
        self.addNewButton.clicked.connect(self.add_new_item)

    def change_calendar_date(self):
        # print("Calendar date was changed.")
        date_selected = self.calendarWidget.selectedDate().toPyDate()
        print(f"Date selected: {date_selected}")
        self.update_task_list(date_selected)

    def update_task_list(self, date):
        self.tasksListWidget.clear()
        db = sqlite3.connect('data.db')
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE Date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        print(results)
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)

    def save_changes(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def add_new_item(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        new_task = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?, ?, ?)"
        row = (new_task, 'NO', date)

        cursor.execute(query, row)
        db.commit()
        self.update_task_list(date)
        self.taskLineEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
