from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.initUI()
       

    def initUI(self):
        uic.loadUi('editor.ui', self)
        self.show()
        self.setWindowTitle("Text Editor")
        self.setWindowIcon(QIcon("Icons/file-word-solid.svg"))

        self.setStyleSheet("QMainWindow {background-color: white; border-radius: 30px;}")

        #FONT SIZES
        self.action12px.triggered.connect(lambda: self.change_size(12))
        self.action18px.triggered.connect(lambda: self.change_size(18))
        self.action24px.triggered.connect(lambda: self.change_size(24))
        
        #BUTTON PUSH
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew_File.triggered.connect(self.new_file)
        self.actionNew_Window.triggered.connect(self.new_window)
        self.actionFont.triggered.connect(self.change_font)
        self.actionWord_Wrap.triggered.connect(self.toggle_word_wrap)
        self.actionClose.triggered.connect(exit)

    #New Window
    def new_window(self):
        MyGUI()
    
    #New File
    def new_file(self, event):
        text = self.textEdit.toPlainText()
        if not text.strip():
            self.initUI()
        else:
            text = self.textEdit.toPlainText()
            if text.strip():
                dialogue = QMessageBox()
                dialogue.setText("Do you want to save your work?")
                dialogue.addButton(QPushButton("Yes"), QMessageBox.YesRole)
                dialogue.addButton(QPushButton("No"), QMessageBox.NoRole)
                dialogue.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

                answer = dialogue.exec_()

                if answer == 0 :
                    self.save_file()
                    self.initUI()
                elif answer == 1:
                    self.initUI()
            else:
                self.initUI()

    #Change font size
    def change_size(self, size):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            char_format = cursor.charFormat()
            char_format.setFontPointSize(size)
            cursor.setCharFormat(char_format)
        else:
            char_format = self.textEdit.currentCharFormat()
            char_format.setFontPointSize(size)
            self.textEdit.setCurrentCharFormat(char_format)

    #Open file from directory
    def open_file(self):
        options = QFileDialog.Options() 
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;Python Files (*.py)", options=options)
        if filename != "":
            with open(filename, "r") as f:
                self.textEdit.setPlainText(f.read())
    
    #Save file into directory
    def save_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if filename != "":
            with open(filename, "w") as f:
                f.write(self.textEdit.toPlainText())

    #Close application
    def closeEvent(self, event):
        text = self.textEdit.toPlainText()
        if text.strip():
            dialogue = QMessageBox()
            dialogue.setText("Do you want to save your work?")
            dialogue.addButton(QPushButton("Yes"), QMessageBox.YesRole)
            dialogue.addButton(QPushButton("No"), QMessageBox.NoRole)
            dialogue.addButton(QPushButton("Cancel"), QMessageBox.RejectRole)

            answer = dialogue.exec_()

            if answer == 0 :
                self.save_file()
                event.accept()
            elif answer == 1:
                event.accept()
            else:
                event.ignore()
        exit

    #Change Font
    def change_font(self):
        font, ok = QFontDialog.getFont(self.textEdit.currentFont(), self)
        if ok:
            self.textEdit.setCurrentFont(font)
    
    def toggle_word_wrap(self):
        if self.actionWord_Wrap.isChecked():
            self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()

if __name__ == "__main__":
    main()