# Python file for importing the JSON into postgres database


import psycopg2
import datetime
import json
db_con = "dbname='flask_blog' user='postgres' host='localhost' password='suji2051'"
import time
with open("/home/rahul/Desktop/_rahul/python_file/py_projects/flask_blog/unneces/h.json", "r") as f:
    data = json.load(f)
    for i in data:
        con = psycopg2.connect(db_con)
        cur = con.cursor()
        time = datetime.datetime.now()
        print(i["title"])
        print(i["content"])
        print(int(i["user_id"]))
        cur.execute("INSERT into public.post (title,date_posted,content,user_id) VALUES ('{}', '{}','{}', {});".format(str(i["title"]), time, str(i["content"]), int(i["user_id"])))
        con.commit()