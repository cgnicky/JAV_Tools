import bs4
import shutil
from PyQt5.QtCore import QThread, pyqtSignal
import os
import re
import time

from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage

PAUSE_TIME_SECOND = 1

class JavClassifier(QThread):
    result = pyqtSignal(str)
    driver = None
    
    def __init__(self, path):
        super().__init__()
        self.path = path

    def getActorName(self, titleName):
        self.driver = ChromiumPage()
        self.driver.get(f"http://www.javlibrary.com/en/vl_searchbyid.php?keyword={titleName}")
        
        cf_bypasser = CloudflareBypasser(self.driver)
        cf_bypasser.bypass()
                
        soup = bs4.BeautifulSoup(self.driver.html, "html.parser")
        if self.validateSearchResult(soup):
            return self.extractActorName(soup, titleName)
        else:
            self.result.emit("Invalid search result!")
            return "Others"

    def extractActorName(self, soup, titleName):
        if not soup.find("div", class_="videos"):
            actor_span = soup.find("span", class_="star")
            if actor_span:
                return actor_span.text
            else:
                self.result.emit("Empty actor name! Move to others...")
                return "Others"
        else:
            print("Found multiple videos in the search result page...")
            self.result.emit("Found multiple videos in the search result page...")
            links = soup.find_all("a", {"title": lambda x: x and x.startswith(titleName.upper())})
            
            url = "http://www.javlibrary.com/en" + links[0].get("href").replace(".", "")

            self.driver.get(url)
            vp_soup = bs4.BeautifulSoup(self.driver.html, "html.parser")
            
            actor_span = vp_soup.find("span", class_="star")
            if actor_span:
                print(f"Found actor name: {actor_span.text}")
                self.result.emit(f"Found actor name: {actor_span.text}")
                return actor_span.text
            else:
                print(f"Found actor name: {actor_span.text}")
                self.result.emit("Empty actor name! Move to others...")
                return "Others"

    def check_existed_file(self, file):
        if os.path.isfile(file):
            return True
        else:
            return False

    def checkAndCreateDirectory(self, filePath):
        print("Checking directory exists or not...")
        self.result.emit("Checking directory exists or not...")
        if os.path.exists(filePath) is True:
            print("Directory existed !")
            self.result.emit("Directory existed !")
        else:
            print("Create a new directory...")
            self.result.emit("Create a new directory...")
            try:
                os.mkdir(filePath)
            except OSError:
                print("Directory %s is failed to be created" % filePath)
                self.result.emit("Directory %s is failed to be created" % filePath)
            else:
                print("Successfully created the directory %s " % filePath)
                self.result.emit("Successfully created the directory %s " % filePath)

    def moveFile(self, file, dest):
        print("Moving {} to {}...".format(file, dest))
        self.result.emit("Moving {} to {}...".format(file, dest))
        shutil.move(file, dest)

    def validateSearchResult(self, soup):
        # Implement the validation logic here
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
                    title, _ = file.split(".")
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
