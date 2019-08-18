import sys
from PyQt5.QtWidgets import *
from PyQt5GUI import Ui_TabWidget
from JavClassifier import JavClassifier
from JavDatabaseUpdater import JavDatabaseUpdater
from JavQuery import JavQuery


class AppWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.javClassifierTab()
        self.javQueryTab()
        self.javDBUpdaterTab()
        self.show()

    # Jav Classifier

    def javClassifierTab(self):
        self.ui.srcEdit.setText("/DATA/Downloads/Media")
        self.ui.execBtn.clicked.connect(self.javClassifierMain)
        self.ui.clearBtn.clicked.connect(self.clearOutput)
        self.ui.browseBtn.clicked.connect(self.selectFolder)

    def javClassifierMain(self):
        path = self.ui.srcEdit.text()
        self.workerThread = JavClassifier(path)
        self.workerThread.result.connect(self.msgLogging)
        self.workerThread.start()
        self.workerThread.finished.connect(self.done)
        self.ui.execBtn.setEnabled(False)

    def done(self):
        self.ui.execBtn.setEnabled(True)
        QMessageBox.information(self, "Done!", "Process Completed!")

    def selectFolder(self):
        self.ui.srcEdit.setText(
            QFileDialog.getExistingDirectory(None, 'Select a Folder', '/DATA', QFileDialog.ShowDirsOnly))

    def msgLogging(self, content):
        self.ui.msgBox.append(content)

    def clearOutput(self):
        self.ui.msgBox.clear()

    # Jav Query

    def javQueryTab(self):
        self.ui.searchKeywordsTextBox.setText("Enter Your Search Keywords Here!!")
        self.ui.queryBtn.clicked.connect(self.javQueryMain)
        self.ui.queryResultClearBtn.clicked.connect(self.clearQueryResult)
        self.ui.searchKeywordsTextBox.clicked.connect(self.ui.searchKeywordsTextBox.clear)

    def javQueryMain(self):
        search_keywords = self.ui.searchKeywordsTextBox.text()
        self.ui.queryResultTextBox.clear()
        self.workerThread = JavQuery(search_keywords, self.set_search_type())
        self.workerThread.result.connect(self.msgLoggingJavQuery)
        self.workerThread.result2.connect(self.updateRecordsCount)
        self.workerThread.start()
        self.workerThread.finished.connect(self.doneJavQuery)
        self.ui.queryBtn.setEnabled(False)

    def msgLoggingJavQuery(self, content):
        self.ui.queryResultTextBox.append(content)

    def updateRecordsCount(self, record_count):
        self.ui.recordCountNumber.setText(str(record_count))

    def doneJavQuery(self):
        self.ui.queryBtn.setEnabled(True)

    def clearQueryResult(self):
        self.ui.queryResultTextBox.clear()

    def set_search_type(self):
        if self.ui.actorRadioBtn.isChecked():
            return "actor"
        elif self.ui.titleRadioBtn.isChecked():
            return "label"
        else:
            QMessageBox.information(self, "Error!", "No Type Selected!")

    # Jav Database Updater
    def javDBUpdaterTab(self):
        default_str = "Insert Directory Path Here!"
        self.ui.dirTextBox.setText(default_str)
        self.ui.dirBrowseBtn.clicked.connect(lambda: self.selectFolderJavUpdater(self.ui.dirTextBox.text(), default_str))
        self.ui.addDirBtn.clicked.connect(lambda: self.addPathToList(self.ui.dirTextBox.text(), default_str))
        self.ui.clearDirListBtn.clicked.connect(self.clearDirList)
        self.ui.updateBtn.clicked.connect(self.javDBUpdaterMain)
        self.ui.dirTextBox.clicked.connect(self.ui.dirTextBox.clear)
        self.ui.dirList.itemDoubleClicked.connect(self.removeItemOnSelection)

    def javDBUpdaterMain(self):
        dir_list = [str(self.ui.dirList.item(i).text()) for i in range(self.ui.dirList.count())]
        if dir_list:
            for path in dir_list:
                self.ui.updateProgressBar.reset()
                self.workerThread = JavDatabaseUpdater(path)
                self.workerThread.start()
                self.workerThread.result.connect(self.showStatusText)
                self.workerThread.pBarMaxValue.connect(self.setProgressMaximum)
                self.workerThread.progressResult.connect(self.updateProgress)
                self.workerThread.finished.connect(self.doneJavUpdater)
                self.ui.updateBtn.setEnabled(False)
                # self.ui.cancelUpdateBtn.clicked.connect(self.workerThread.terminate())
            self.ui.statusContent.setText("Idle")
        else:
            QMessageBox.information(self, "Error!", "Empty Directory List!")

    def selectFolderJavUpdater(self, textbox_path, default_str):
        if textbox_path == default_str:
            self.ui.dirTextBox.setText(
                QFileDialog.getExistingDirectory(None, 'Select a Folder', '/DATA/', QFileDialog.ShowDirsOnly))
        elif not textbox_path:
            self.ui.dirTextBox.setText(
                QFileDialog.getExistingDirectory(None, 'Select a Folder', '/DATA/', QFileDialog.ShowDirsOnly))
        else:
            self.ui.dirTextBox.setText(
                QFileDialog.getExistingDirectory(None, 'Select a Folder', textbox_path, QFileDialog.ShowDirsOnly))

    def addPathToList(self, dir_path, default_str):
        if dir_path.strip() and dir_path.strip() != default_str:
            self.ui.dirList.addItem(dir_path)
        else:
            QMessageBox.information(self, "Error!", "Invalid Directory!")

    def clearDirList(self):
        self.ui.dirList.clear()

    def showStatusText(self, content):
        self.ui.statusContent.setText(content)

    def doneJavUpdater(self):
        self.ui.updateBtn.setEnabled(True)

    def updateProgress(self, complete):
        self.ui.updateProgressBar.setValue(complete)

    def setProgressMaximum(self, maxValue):
        self.ui.updateProgressBar.setMaximum(maxValue)

    def removeItemOnSelection(self, item):
        self.ui.dirList.takeItem(item.currentRow)


def main():
    app = QApplication(sys.argv)
    ex = AppWindow()
    ex.setCurrentIndex(2)  # Show the first tab at start
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
