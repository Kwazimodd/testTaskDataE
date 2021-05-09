import requests
import pymysql
import datetime
from pattern import p_app, p_movie, p_song


class App:
    def __init__(self, bucket):
        self.bucket = bucket

    def run(self):
        while 1:
            self.get_data(self.get_bucket())

    def get_bucket(self):
        return requests.get(self.bucket + "files_list.data").content.splitlines()

    def get_data(self, arr):
        conn = pymysql.connect(host="www.db4free.net", user="linad2997", password="london1997", database="cual2000")
        cursor = conn.cursor()
        for i in arr:
            name = (str(i))[2:-1:1]
            cursor.execute("""SELECT * FROM ID_used
                            WHERE Id_used='{}';""".format(name))
            a = cursor.fetchall()
            print(a)
            if len(a) > 0:
                return
            else:
                cursor.execute("""INSERT INTO ID_used (Id_used) 
                                  VALUES ("{}");""".format(name))
                conn.commit()
            k = requests.get(self.bucket + name).json()
            for j in k:
                self.update_database(j)

    def update_database(self, arg):
        conn = pymysql.connect(host="www.db4free.net", user="linad2997", password="london1997", database="cual2000")
        cursor = conn.cursor()
        if arg["type"] == "app":
            p = p_app
            is_awesome = arg["data"]["genre"] == "Games"
            cursor.execute(p.format(arg["data"]["name"],
                                    arg["data"]["genre"],
                                    arg["data"]["rating"],
                                    arg["data"]["version"],
                                    arg["data"]["size_bytes"],
                                    int(is_awesome)))
            conn.commit()
            print(cursor.fetchall())
        elif arg["type"] == "movie":
            p = p_movie

            original_title_normalized = ""
            for i in arg["data"]["original_title"]:
                if i.isalpha() or i.isdigit() or i.isspace():
                    original_title_normalized += i.lower()
            original_title_normalized = original_title_normalized.replace(" ", "_")

            print(p.format(arg["data"]["original_title"],
                            arg["data"]["original_language"],
                            arg["data"]["budget"],
                                    int(arg["data"]["is_adult"]),
                                    arg["data"]["release_date"],
                                    original_title_normalized))

            cursor.execute(p.format(arg["data"]["original_title"],
                                    arg["data"]["original_language"],
                                    arg["data"]["budget"],
                                    int(arg["data"]["is_adult"]),
                                    arg["data"]["release_date"],
                                    original_title_normalized))
            conn.commit()
            print(cursor.fetchall())
        elif arg["type"] == "song":
            p = p_song
            now = datetime.datetime.now()
            cursor.execute(p.format(arg["data"]["artist_name"],
                                    arg["data"]["title"],
                                    arg["data"]["year"],
                                    arg["data"]["release"],
                                    now))
            conn.commit()
            print(cursor.fetchall())

    @staticmethod
    def main():
        app = App("https://data-engineering-interns.macpaw.io/")
        app.run()


if __name__ == "__main__":
    App.main()
