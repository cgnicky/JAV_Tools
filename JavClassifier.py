import bs4
import shutil
from PyQt5.QtCore import *
import os
import re
import time

from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage


PAUSE_TIME_SECOND = 1


class JavClassifier(QThread):
    result = pyqtSignal(str)

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def getActorName(self, titleName):
        driver = ChromiumPage()

        driver.get("http://www.javlibrary.com/en/vl_searchbyid.php?keyword={}".format(titleName))
        
        cf_bypasser = CloudflareBypasser(driver)
        cf_bypasser.bypass()
        
        soup = bs4.BeautifulSoup(driver.html, "html.parser")
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
                links = soup.find_all("a", {"title": lambda x: x and x.startswith(titleName.upper())})
                link = ""
                for i in links:
                    link = i.attrs['href']
                driver.get("http://www.javlibrary.com/en/{}".format(link[2:len(link)]))
                
                cf_bypasser = CloudflareBypasser(driver)
                cf_bypasser.bypass()
                
                soup2 = bs4.BeautifulSoup(driver.html, "html.parser")
                actorName = soup2.find("span", class_="star").text
                return actorName
        else:
            print("Failed to identify! Move to others...")
            self.result.emit("Failed to identify! Move to others...")
            return "Others"

    def check_existed_file(self, file):
        if os.path.isfile(file):
            return True
        else:
            return False

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
        pattern = r'^([A-Z]+-\d+).*'
        match = re.match(pattern, filename)
        if match:
            return match.group(1)
        else:
            return filename

    def moveFiles(self, path, file, title):
        print("Moving video files...")
        self.result.emit("Moving video files...")
        actor_name = self.getActorName(title)
        if "LUXU" in file:
            title = "LUXU-Series"
            dest = "{}\{}".format(path, title)
        elif "GANA" in file:
            title = "GANA-Series"
            dest = "{}\{}".format(path, title)
        else:
            dest = "{}\{}".format(path, actor_name)
        src = "{}\{}".format(path, file)
        self.checkAndCreateDirectory(dest)
        if self.check_existed_file("{}\{}\{}".format(path, actor_name, file)) is False:
            self.moveFile(src, dest)
        else:
            dest = "{}\{}".format(path, "Existed")
            self.checkAndCreateDirectory(dest)
            self.moveFile(src, dest)
            
    def avoid_rate_limit(self):
        print(f"Pause for {PAUSE_TIME_SECOND}s to prevent rate limiter")
        self.result.emit(f"Pause for {PAUSE_TIME_SECOND}s to prevent rate limiter")
        time.sleep(PAUSE_TIME_SECOND)

    def run(self):
        curPath = self.path
        source = os.listdir(curPath)
        for file in source:            
            print(f"Processing: [{file}] ...")
            self.result.emit(f"Processing: [{file}] ...")
            if len(file.split(".")) <= 2:
                try:
                    title, ext = file.split(".")
                    title = self.filenameFix(title)
                    if file.endswith(".mp4") or file.endswith(".avi"):
                        self.avoid_rate_limit()
                        
                        self.moveFiles(curPath, file, title)
                    else:
                        print("Extension not supported!")
                        self.result.emit("Extension not supported!")
                except ValueError:
                    print("Not a media file, skipped!")
                    self.result.emit("Not a media file, skipped!")
            else:
                print("Invalid extension format!")
                self.result.emit("Invalid extension format!")
        self.result.emit("Process all completed !")
