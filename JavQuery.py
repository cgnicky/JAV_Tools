from PyQt5.QtCore import *
import os
from configparser import ConfigParser
import psycopg2


class JavQuery(QThread):
    result = pyqtSignal(str)
    result2 = pyqtSignal(int)

    # config_path = '/home/nicky/PycharmProjects/pythonPractice/database.ini'
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(ROOT_DIR, "database.ini")
    db_type = 'postgresql'

    def __init__(self, search_keywords, search_type):
        QThread.__init__(self)
        self.search_keywords = search_keywords
        self.search_type = search_type

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
        # self.result.emit('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        return conn

    def query_by_label(self, cur, keyword):
        # self.result.emit("Executing statement with keywords \"{}\"".format(keyword))
        cur.execute("SELECT actor,label FROM javlist_2 WHERE label like \'%{}%\' ORDER BY label".format(keyword))
        row_count = cur.rowcount
        result = cur.fetchall()
        return row_count, result

    def query_by_actor(self, cur, keyword):
        cur.execute("SELECT actor,label FROM javlist_2 WHERE actor like \'%{}%\' ORDER BY label".format(keyword))
        row_count = cur.rowcount
        result = cur.fetchall()
        return row_count, result

    def run(self):
        # self.result.emit('Initializing Database Connection...')
        search_key = self.search_keywords
        conn = None
        try:
            conn = self.establish_to_db()
            # create a cursor
            cur = conn.cursor()

            if self.search_type == "label":
                # Query from database and show result
                result_count, result_set = self.query_by_label(cur, search_key)
                if result_count != 0:
                    self.result2.emit(result_count)
                    for row in result_set:
                        actor = row[0]
                        label = row[1]
                        self.result.emit("{}, {}".format(actor, label))
                else:
                    self.result.emit("No Records Found!")
            elif self.search_type == "actor":
                # Query from database and show result
                result_count, result_set = self.query_by_actor(cur, search_key)
                if result_count != 0:
                    self.result2.emit(result_count)
                    for row in result_set:
                        actor = row[0]
                        label = row[1]
                        self.result.emit("{}, {}".format(actor, label))
                else:
                    self.result.emit("No Records Found!")

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                # self.result.emit('Database connection closed.')