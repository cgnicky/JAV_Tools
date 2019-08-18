from PyQt5.QtCore import *
import os
from configparser import ConfigParser
import psycopg2
import datetime


class JavDatabaseUpdater(QThread):
    result = pyqtSignal(str)
    progressResult = pyqtSignal(int)
    pBarMaxValue = pyqtSignal(int)

    # config_path = '/home/nicky/PycharmProjects/pythonPractice/database.ini'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(ROOT_DIR, "database.ini")
    db_type = 'postgresql'

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def config(self, filename, section):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def establish_to_db(self):
        # read connection parameters
        params = self.config(self.config_path, self.db_type)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        self.result.emit('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        return conn

    def update_to_db(self, cur, row_list):
        count = 0
        for row in row_list:
            actor = row[0]
            label = row[1]
            timestamp = row[2]
            path = row[3]
            if "\'" not in path:
                # insert_query = f"INSERT INTO javlist_3 VALUES ('{actor}', '{label}', '{timestamp}', '{path}')"
                insert_query = f"INSERT INTO javlist_3 VALUES ('{actor}', '{label}', '{timestamp}', '{path}') ON CONFLICT (label) DO NOTHING"
                cur.execute(insert_query)

            count += 1
            self.progressResult.emit(count)

    def get_media_list(self, dir_list):
        result_list = list()
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        folder_list = ['253KAKU', '261ARA', '300MIUM', 'GANA-Series', 'LUXU-Series', 'S-Cute', 'SIRO']

        # Get the list of all files in directory tree at given path
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(dir_list):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]

        # Print the files
        for elem in listOfFiles:
            parts = str(elem).split("/")
            media_name = parts[len(parts) - 1].split(".")[0]
            actor_name = parts[len(parts) - 2]
            if actor_name != "Downloading":
                result_list.append([actor_name, media_name, ts, elem])
            # if parts[4] == "JAV Stars":
            #     actor_name = parts[5]
            #     media_name = parts[6]
            #     #           print(actor_name + " : " + media_name)
            #     result_list.append([actor_name, media_name, ts, elem])
            # elif parts[4] in folder_list:
            #     actor_name = "Unknown"
            #     media_name = parts[5]
            #     result_list.append([actor_name, media_name, ts, elem])
            # else:
            #     print("Skipped...")
        return result_list

    def run(self):
        data_list = self.get_media_list(self.path)
        conn = None
        try:
            conn = self.establish_to_db()
            # create a cursor
            cur = conn.cursor()
            # Sending signal result to front-end
            self.result.emit("Working on {}".format(self.path))
            self.pBarMaxValue.emit(len(data_list))

            self.update_to_db(cur, data_list)

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                self.result.emit('Database connection closed.')