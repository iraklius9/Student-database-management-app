import sys
import random
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QLineEdit, QMessageBox, QHeaderView, QFormLayout,
                             QGroupBox, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont


class DatabaseWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, students_data):
        super().__init__()
        self.students_data = students_data

    def run(self):
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()

            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS students
                           (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               surname TEXT NOT NULL,
                               name TEXT NOT NULL,
                               subject TEXT NOT NULL,
                               score INTEGER NOT NULL
                           )
                           ''')

            cursor.execute('DELETE FROM students')

            self.progress.emit("მონაცემთა ბაზაში ჩაწერა იწყება...")

            for i, student in enumerate(self.students_data):
                cursor.execute('''
                               INSERT INTO students (surname, name, subject, score)
                               VALUES (?, ?, ?, ?)
                               ''', student)

                if (i + 1) % 100 == 0:
                    self.progress.emit(f"ჩაწერილია {i + 1}/1000 სტუდენტი")

            conn.commit()
            conn.close()
            self.progress.emit("ყველა სტუდენტი წარმატებით ჩაიწერა!")

        except Exception as e:
            self.progress.emit(f"შეცდომა: {str(e)}")


class StudentDatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_data()
        self.init_ui()
        self.init_database()

    def init_data(self):
        self.lnames = [
            'აბაშიძე', 'გიგაური', 'არჩვაძე', 'ახალაია', 'ბაძაღუა', 'ბერიანიძე',
            'ბერიშვილი', 'გვენცაძე', 'დალაქიშვილი', 'ანთიძე', 'გიორგაძე', 'გოგალაძე',
            'გოცირიძე', 'ვარდიძე', 'ზარანდია', 'თადუმაძე', 'ლაბაძე', 'კვარაცხელია',
            'კუსრაძე', 'კვესელავა', 'კაპანაძე', 'კასრაძე', 'კვინიკაძე', 'კოპაძე',
            'კანკია', 'კორძაია', 'მიქავა', 'მელია', 'მონიავა', 'ნიაური', 'ლაცაბიძე',
            'მიქაძე', 'ნემსიწვერიძე', 'მაისურაძე', 'მაცაბერიძე', 'მჟავია', 'მაჩალაძე',
            'ოდიშარია', 'მეტრეველი', 'ნეფარიძე', 'მოდებაძე', 'მარჯანიძე', 'მუმლაძე',
            'ნასრაშვილი', 'ჯანჯღავა', 'მოსია', 'ნოზაძე', 'ნუცუბიძე', 'ონიანი',
            'ოქრუაშვილი', 'პერტია', 'რაზმაძე', 'რევაზაშვილი', 'საგანელიძე', 'ჯახაია',
            'სალუქვაძე', 'სამსონაშვილი', 'სამხარაძე', 'სარალიძე', 'სართანია',
            'სარიშვილი', 'სიმონიშვილი', 'სხილაძე', 'ხურციძე', 'სიხარულიძე',
            'ტაბატაძე', 'ფაცაცია', 'ფილაური', 'ფუხაშვილი', 'ქობალია', 'ყიფშიძე',
            'შაინიძე', 'ფიფია', 'შენგელია', 'შეროზია', 'შველიძე', 'ჩხეიძე', 'ჩადუნელი',
            'ჩიკვაშვილი', 'ცქიტიშვილი', 'ჩოკორაია', 'ცაგურია', 'ცერცვაძე', 'ცუხიშვილი',
            'ძინძიბაძე', 'წერეთელი', 'წიკლაური', 'ჭავჭანიძე', 'ჩირაძე', 'ჭელიძე',
            'ჭანტურია', 'სირაძე', 'შონია', 'ხანჯალაძე', 'ხარაზიშვილი', 'ხელაძე',
            'ხვინგია', 'ხუციშვილი', 'ჯანელიძე', 'ჯოხაძე'
        ]

        self.fnames = [
            'ანა', 'ანუკი', 'ბარბარე', 'გვანცა', 'დიანა', 'ეკა', 'ელენე', 'ვერონიკა',
            'ვიქტორია', 'თათია', 'ლამზირა', 'თეა', 'თეკლე', 'თინიკო', 'თამარი', 'იზაბელა',
            'ია', 'იამზე', 'ლია', 'ლიკა', 'ლანა', 'მარიკა', 'მანანა', 'მაია', 'მაკა',
            'მარიამი', 'ნანა', 'ნანი', 'ნატა', 'ნატო', 'ნინო', 'ნონა', 'ოლიკო', 'ქეთევანი',
            'სალომე', 'სოფიკო', 'ნია', 'ქრისტინე', 'შორენა', 'ხატია', 'ალეკო', 'ალიკა',
            'ამირან', 'ანდრია', 'არჩილი', 'ასლანი', 'ბაჩუკი', 'ბექა', 'გიგა', 'გიორგი',
            'დავითი', 'გიგი', 'გოგა', 'დათა', 'ერეკლე', 'თემური', 'იაკობ', 'ილია', 'ირაკლი',
            'ლადო', 'ლაშა', 'მიხეილ', 'ნიკა', 'ოთარი', 'პაატა', 'რამაზ', 'რამინი', 'რატი',
            'რაული', 'რევაზი', 'რომა', 'რომანი', 'სანდრო', 'საბა', 'სერგი', 'სიმონ',
            'შალვა', 'შოთა', 'ცოტნე', 'ჯაბა'
        ]

        self.subjects = [
            'პროგრამირების საფუძვლები', 'კალკულუსი II', 'შესავალი ფიზიკაში',
            'კომპიუტერული უნარჩვევები', 'ქიმიის შესავალი', 'ბიოლოგიის შესავალი',
            'ალგორითმები I', 'შესავალი ელექტრონიკაში', 'მონაცემთა სტრუქტურები',
            'ალგორითმები II'
        ]

    def init_ui(self):
        self.setWindowTitle('სტუდენტების მონაცემთა ბაზის მართვა')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel('სტუდენტების მონაცემთა ბაზის მართვა')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        main_layout.addWidget(title_label)

        self.create_entry_form()
        main_layout.addWidget(self.entry_group)

        buttons_layout = QHBoxLayout()

        self.write_btn = QPushButton('ჩაწერა')
        self.write_btn.setMinimumHeight(40)
        self.write_btn.clicked.connect(self.write_students)
        buttons_layout.addWidget(self.write_btn)

        self.read_btn = QPushButton('წაკითხვა')
        self.read_btn.setMinimumHeight(40)
        self.read_btn.clicked.connect(self.read_students)
        buttons_layout.addWidget(self.read_btn)

        self.search_btn = QPushButton('ძიება')
        self.search_btn.setMinimumHeight(40)
        self.search_btn.clicked.connect(self.search_students)
        buttons_layout.addWidget(self.search_btn)

        self.delete_selected_btn = QPushButton('არჩეულის წაშლა')
        self.delete_selected_btn.setMinimumHeight(40)
        self.delete_selected_btn.clicked.connect(self.delete_selected_students)
        buttons_layout.addWidget(self.delete_selected_btn)

        self.delete_all_btn = QPushButton('ყველას წაშლა')
        self.delete_all_btn.setMinimumHeight(40)
        self.delete_all_btn.clicked.connect(self.delete_all_students)
        buttons_layout.addWidget(self.delete_all_btn)

        main_layout.addLayout(buttons_layout)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel('ძიება (სახელი/გვარი):'))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('შეიყვანეთ სახელი ან გვარი...')
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        self.status_label = QLabel('მზად არის მუშაობისთვის')
        self.status_label.setStyleSheet("QLabel { color: blue; }")
        main_layout.addWidget(self.status_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'გვარი', 'სახელი', 'საგანი', 'ქულა'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)

        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)

        main_layout.addWidget(self.table)

    def create_entry_form(self):
        """Create the student entry form"""
        self.entry_group = QGroupBox("სტუდენტის ჩანაწერი")
        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("ავტომატური ID")
        form_layout.addRow("ID:", self.id_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("შეიყვანეთ სახელი...")
        form_layout.addRow("სახელი:", self.name_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("შეიყვანეთ გვარი...")
        form_layout.addRow("გვარი:", self.surname_input)

        self.subject_input = QComboBox()
        self.subject_input.addItems(self.subjects)
        self.subject_input.setEditable(True)
        form_layout.addRow("საგანი:", self.subject_input)

        self.score_input = QSpinBox()
        self.score_input.setRange(0, 100)
        self.score_input.setValue(0)
        form_layout.addRow("შეფასება:", self.score_input)

        form_buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton('დამატება')
        self.add_btn.clicked.connect(self.add_student)
        form_buttons_layout.addWidget(self.add_btn)

        self.update_btn = QPushButton('ჩასწორება')
        self.update_btn.clicked.connect(self.update_student)
        self.update_btn.setEnabled(False)
        form_buttons_layout.addWidget(self.update_btn)

        self.clear_btn = QPushButton('გასუფთავება')
        self.clear_btn.clicked.connect(self.clear_form)
        form_buttons_layout.addWidget(self.clear_btn)

        form_layout.addRow(form_buttons_layout)
        self.entry_group.setLayout(form_layout)

    def clear_form(self):
        """Clear all form fields"""
        self.id_input.clear()
        self.name_input.clear()
        self.surname_input.clear()
        self.subject_input.setCurrentIndex(0)
        self.score_input.setValue(0)
        self.update_btn.setEnabled(False)
        self.add_btn.setEnabled(True)

    def add_student(self):
        """Add a single student to the database"""
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        subject = self.subject_input.currentText().strip()
        score = self.score_input.value()

        if not name or not surname or not subject:
            QMessageBox.warning(self, 'გაფრთხილება', 'გთხოვთ შეავსოთ ყველა ველი!')
            return

        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO students (surname, name, subject, score)
                           VALUES (?, ?, ?, ?)
                           ''', (surname, name, subject, score))
            conn.commit()
            conn.close()

            self.clear_form()
            self.read_students()
            self.status_label.setText('ახალი სტუდენტი წარმატებით დაემატა!')

        except Exception as e:
            QMessageBox.critical(self, 'შეცდომა', f'სტუდენტის დამატების შეცდომა: {str(e)}')

    def update_student(self):
        """Update selected student"""
        if not self.id_input.text():
            QMessageBox.warning(self, 'გაფრთხილება', 'გთხოვთ აირჩიოთ სტუდენტი ცხრილიდან!')
            return

        student_id = int(self.id_input.text())
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        subject = self.subject_input.currentText().strip()
        score = self.score_input.value()

        if not name or not surname or not subject:
            QMessageBox.warning(self, 'გაფრთხილება', 'გთხოვთ შეავსოთ ყველა ველი!')
            return

        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute('''
                           UPDATE students
                           SET surname=?,
                               name=?,
                               subject=?,
                               score=?
                           WHERE id = ?
                           ''', (surname, name, subject, score, student_id))
            conn.commit()
            conn.close()

            self.clear_form()
            self.read_students()
            self.status_label.setText('სტუდენტის მონაცემები წარმატებით განახლდა!')

        except Exception as e:
            QMessageBox.critical(self, 'შეცდომა', f'სტუდენტის განახლების შეცდომა: {str(e)}')

    def on_table_selection_changed(self):
        """Handle table selection changes"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            # Fill form with selected student data
            self.id_input.setText(self.table.item(current_row, 0).text())
            self.surname_input.setText(self.table.item(current_row, 1).text())
            self.name_input.setText(self.table.item(current_row, 2).text())

            subject_text = self.table.item(current_row, 3).text()
            subject_index = self.subject_input.findText(subject_text)
            if subject_index >= 0:
                self.subject_input.setCurrentIndex(subject_index)
            else:
                self.subject_input.setCurrentText(subject_text)

            self.score_input.setValue(int(self.table.item(current_row, 4).text()))

            self.update_btn.setEnabled(True)
            self.add_btn.setEnabled(False)

    def init_database(self):
        """Initialize the database"""
        try:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS students
                           (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               surname TEXT NOT NULL,
                               name TEXT NOT NULL,
                               subject TEXT NOT NULL,
                               score INTEGER NOT NULL
                           )
                           ''')
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'შეცდომა', f'მონაცემთა ბაზის ინიციალიზაციის შეცდომა: {str(e)}')

    def generate_students_data(self):
        """Generate 1000 random students data"""
        students_data = []
        for _ in range(1000):
            surname = random.choice(self.lnames)
            name = random.choice(self.fnames)
            subject = random.choice(self.subjects)
            score = random.randint(0, 100)
            students_data.append((surname, name, subject, score))
        return students_data

    def write_students(self):
        """Write 1000 students to database"""
        self.write_btn.setEnabled(False)
        self.status_label.setText('მონაცემების გენერაცია...')

        students_data = self.generate_students_data()

        self.worker = DatabaseWorker(students_data)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.write_finished)
        self.worker.start()

    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)

    def write_finished(self):
        """Called when writing is finished"""
        self.write_btn.setEnabled(True)
        self.read_students()  # Refresh table
        QMessageBox.information(self, 'შესრულებულია', '1000 სტუდენტის მონაცემი წარმატებით ჩაიწერა!')

    def read_students(self):
        """Read all students from database and display in table"""
        try:
            self.status_label.setText('მონაცემების ჩატვირთვა მიმდინარეობს...')
            QApplication.processEvents()  # Update UI immediately

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students ORDER BY id LIMIT 1000')
            students = cursor.fetchall()
            conn.close()

            self.table.setRowCount(len(students))
            for row, student in enumerate(students):
                for col, data in enumerate(student):
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))

                if row % 100 == 0:
                    QApplication.processEvents()

            if len(students) == 1000:
                self.status_label.setText(f'ნაჩვენებია პირველი 1000 სტუდენტი')
            else:
                self.status_label.setText(f'ნაჩვენებია {len(students)} სტუდენტი')

        except Exception as e:
            QMessageBox.critical(self, 'შეცდომა', f'მონაცემების წაკითხვის შეცდომა: {str(e)}')

    def search_students(self):
        """Search students by name or surname"""
        search_text = self.search_input.text().strip()
        if not search_text:
            QMessageBox.information(self, 'ინფორმაცია', 'გთხოვთ შეიყვანოთ საძიებო ტექსტი!')
            return

        try:
            self.status_label.setText('ძიება მიმდინარეობს...')
            QApplication.processEvents()

            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT *
                           FROM students
                           WHERE surname LIKE ?
                              OR name LIKE ?
                           ORDER BY id LIMIT 1000
                           ''', (f'%{search_text}%', f'%{search_text}%'))
            students = cursor.fetchall()
            conn.close()

            self.table.setRowCount(len(students))
            for row, student in enumerate(students):
                for col, data in enumerate(student):
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))

                if row % 100 == 0:
                    QApplication.processEvents()

            if len(students) == 0:
                self.status_label.setText('ძიების შედეგი: სტუდენტი ვერ მოიძებნა')
            else:
                self.status_label.setText(f'ძიების შედეგი: {len(students)} სტუდენტი')

        except Exception as e:
            QMessageBox.critical(self, 'შეცდომა', f'ძიების შეცდომა: {str(e)}')

    def delete_selected_students(self):
        """Delete selected students from database"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, 'გაფრთხილება', 'გთხოვთ აირჩიოთ სტუდენტი(ები) წასაშლელად!')
            return

        reply = QMessageBox.question(
            self, 'დაადასტურეთ',
            f'ნამდვილად გსურთ {len(selected_rows)} სტუდენტის წაშლა?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect('students.db')
                cursor = conn.cursor()
                selected_ids = [int(self.table.item(row.row(), 0).text()) for row in selected_rows]

                cursor.executemany('DELETE FROM students WHERE id = ?', [(id,) for id in selected_ids])
                conn.commit()
                conn.close()

                self.clear_form()
                self.read_students()
                self.status_label.setText(f'{len(selected_rows)} სტუდენტი წარმატებით წაიშალა')
                QMessageBox.information(self, 'შესრულებულია', f'{len(selected_rows)} სტუდენტი წარმატებით წაიშალა!')

            except Exception as e:
                QMessageBox.critical(self, 'შეცდომა', f'არჩეული სტუდენტების წაშლის შეცდომა: {str(e)}')

    def delete_all_students(self):
        """Delete all students from database"""
        reply = QMessageBox.question(
            self, 'დაადასტურეთ',
            'ნამდვილად გსურთ ყველა სტუდენტის მონაცემის წაშლა?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect('students.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM students')
                conn.commit()
                conn.close()

                self.table.setRowCount(0)
                self.clear_form()
                self.status_label.setText('ყველა მონაცემი წაიშალა')
                QMessageBox.information(self, 'შესრულებულია', 'ყველა სტუდენტის მონაცემი წარმატებით წაიშალა!')

            except Exception as e:
                QMessageBox.critical(self, 'შეცდომა', f'მონაცემების წაშლის შეცდომა: {str(e)}')


def main():
    app = QApplication(sys.argv)

    font = QFont()
    font.setPointSize(10)
    app.setFont(font)

    window = StudentDatabaseApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()