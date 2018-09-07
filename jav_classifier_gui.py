import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import *
from gui_style import Ui_MainWindow
import cfscrape
import bs4
import os
import shutil


class mainThread(QThread):
    result = pyqtSignal(str)

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def getActorName(self, titleName):
        scraper = cfscrape.create_scraper()

        response = scraper.get("http://www.javlibrary.com/en/vl_searchbyid.php?keyword={}".format(titleName))
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        if self.validateSearchResult(soup) is True:
            if not soup.find("div", class_="videos"):
                if soup.find("span", class_="star"):
                    actorName = soup.find("span", class_="star").text
                    return actorName
                else:
                    print("Empty actor name! Move to others...")
                    self.result.emit("Empty actor name! Move to others...")
                    return "Others"
            else:
                link = \
                soup.find("div", class_="video").find("a", {"title": lambda x: x and x.startswith(titleName)}).attrs[
                    'href']
                nextPage = scraper.get("http://www.javlibrary.com/en/{}".format(link[2:len(link)]))
                soup2 = bs4.BeautifulSoup(nextPage.content, "html.parser")
                actorName = soup2.find("span", class_="star").text
                return actorName
        else:
            print("Failed to identify! Move to others...")
            self.result.emit("Failed to identify! Move to others...")
            return "Others"

    def checkAndCreateDirectory(self, filePath):
        print("Checking Directory exists or not...")
        self.result.emit("Checking Directory exists or not...")
        if os.path.exists(filePath) is True:
            print("Directory existed !")
            self.result.emit("Directory existed !")
        else:
            print("Create a new directory...")
            self.result.emit("Create a new directory...")
            try:
                os.mkdir(filePath)
            except OSError:
                print("Creation of the directory %s failed" % filePath)
                self.result.emit("Creation of the directory %s failed" % filePath)
            else:
                print("Successfully created the directory %s " % filePath)
                self.result.emit("Successfully created the directory %s " % filePath)

    def moveFile(self, file, dest):
        print("Moving {} to {}...".format(file, dest))
        self.result.emit("Moving {} to {}...".format(file, dest))
        shutil.move(file, dest)

    def validateSearchResult(self, content):
        if content.find("div", id="badalert"):
            print("Invalid format of search keyword!")
            self.result.emit("Invalid format of search keyword!")
            return False
        elif content.find("em"):
            print("No result found!")
            self.result.emit("No result found!")
            return False
        else:
            return True

    def filenameFix(self, filename):
        if filename.endswith("C"):
            return filename[:len(filename) - 2]
        else:
            return filename

    def moveMp4(self, path, file, title):
        print("Moving MP4 files...")
        self.result.emit("Moving MP4 files...")
        if "LUXU" in file:
            dest = "{}/{}".format(path, "LUXU-Series")
        elif "GANA" in file:
            dest = "{}/{}".format(path, "GANA-Series")
        else:
            dest = "{}/{}".format(path, self.getActorName(title))
        src = "{}/{}".format(path, file)
        self.checkAndCreateDirectory(dest)
        self.moveFile(src, dest)

    def moveAvi(self, path, file, title):
        print("Moving AVI files...")
        self.result.emit("Moving AVI files...")
        dest = "{}/{}".format(path, self.getActorName(title))
        src = "{}/{}".format(path, file)
        self.checkAndCreateDirectory(dest)
        self.moveFile(src, dest)

    def run(self):
        curPath = self.path
        source = os.listdir(curPath)
        for file in source:
            print(file)
            self.result.emit(file)
            if len(file.split(".")) <= 2:
                try:
                    title, ext = file.split(".")
                    title = self.filenameFix(title)
                    if file.endswith(".mp4"):
                        self.moveMp4(curPath, file, title)
                    elif file.endswith(".avi"):
                        self.moveAvi(curPath, file, title)
                    else:
                        print("Extension not supported!")
                        self.result.emit("Extension not supported!")
                except ValueError:
                    print("Not a media file, skipped...")
                    self.result.emit("Not a media file, skipped...")
            else:
                print("Invalid extension format!")
                self.result.emit("Invalid extension format!")
        print("Process Successfully !!")
        self.result.emit("Process Successfully !!")


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.show()

        self.ui.srcEdit.setText("/DATA/Downloads/Media")
        self.ui.execBtn.clicked.connect(self.mainProcess)
        self.ui.clearBtn.clicked.connect(self.clearOutput)
        self.ui.browseBtn.clicked.connect(self.selectFolder)

    def mainProcess(self):
        path = self.ui.srcEdit.text()
        self.workerThread = mainThread(path)
        self.workerThread.result.connect(self.msgLogging)
        self.workerThread.start()

    def selectFolder(self):
        self.ui.srcEdit.setText(QFileDialog.getExistingDirectory(None, 'Select a Folder', '/DATA/', QFileDialog.ShowDirsOnly))

    def msgLogging(self, content):
        self.ui.msgBox.append(content)

    def clearOutput(self):
        self.ui.msgBox.clear()


app = QApplication([])
w = AppWindow()
w.show()
sys.exit(app.exec_())
