import requests
import pymysql
import datetime
from pattern import p_app, p_movie, p_song


class App:
    def __init__(self, db, bucket):
        self.database = db
        self.bucket = bucket
        self.read = {}

    def run(self):
        while 1:
            k = self.get_data(self.get_json())
            self.update_database(k)

    def get_json(self):
        return requests.get(self.bucket + "files_list.data").content.splitlines()

    def get_data(self, arr):
        args = []
        for i in arr:
            k = requests.get(self.bucket + str(i)[2:-1:1]).json()
            for j in k:
                args.append(j)
        return args

    def update_database(self, args):

        cursor = 0  # get cursor from db
        for arg in args:
            if arg["type"] == "app":
                p = p_app
                """cursor.execute(p.format(arg["data"]["name"],
                                        arg["data"]["genre"],
                                        arg["data"]["rating"],
                                        arg["data"]["version"],
                                        arg["data"]["size_bytes"],
                                        arg["data"]["is_awesome"]))
                print(cursor.fetchall())"""
            elif arg["type"] == "movie":
                p = p_movie

                original_title_normalized = ""
                for i in arg["data"]["original_title"]:
                    if i.isalpha() or i.isdigit() or i.isspace():
                        original_title_normalized += i.lower()
                original_title_normalized = original_title_normalized.replace(" ", "_")
                print(original_title_normalized)

                """cursor.execute(p.format(arg["data"]["original_title"],
                                        arg["data"]["original_language"],
                                        arg["data"]["budget"],
                                        arg["data"]["is_adult"],
                                        arg["data"]["release_date"],
                                        original_title_normalized))
                print(cursor.fetchall())"""
            elif arg["type"] == "song":
                p = p_song
                now = datetime.datetime.now()
                """cursor.execute(p.format(arg["data"]["artist_name"],
                                        arg["data"]["title"],
                                        arg["data"]["year"],
                                        arg["data"]["release"],
                                        now))
                print(cursor.fetchall())"""

    @staticmethod
    def main():
        app = App("", "https://data-engineering-interns.macpaw.io/")
        app.run()


if __name__ == "__main__":
    App.main()
