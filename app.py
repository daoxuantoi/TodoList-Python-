from flask import Flask, request,redirect,url_for,jsonify,json
import sqlite3
from flask_cors import CORS # thưa thầy câu lệnh để cài đặt thư viện là pip install -U flask-cors ạ
app = Flask(__name__)
#this cors use to prevent some problem about route
CORS(app, support_credentials=True)

#THƯA THẦY ĐÂY LÀ PHẦN ĐỂ TẠO BẢNG DATABASE VÀ INSERT DỮ LIỆU VÀO DATABASE Ạ

def createTableAndInsert ():
    conn = sqlite3.connect('todoList.db')
    cursor = conn.cursor()
    cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='todo' """)
    if cursor.fetchone()[0] == 1:
        return
    conn.execute("""CREATE TABLE IF NOT EXISTS todo
            (id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            status TEXT NOT NULL
            );""")
    conn.execute("INSERT INTO todo (description, status) VALUES ('SS1 Assignment 1', 'Done')")
    conn.execute("INSERT INTO todo (description, status) VALUES ('SS1 Assignment 2', 'Doing')")
    conn.execute("INSERT INTO todo (description, status) VALUES ('SS1 Final', 'Doing')")
    conn.commit()

# CREATE TABLE
createTableAndInsert()

@app.route('/api/list',methods = ['GET'])
def index():
    #connect to db then get again value from db
    conn = sqlite3.connect('todoList.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    objectTempt = []# create array then push the each of record to array
    for item in rows:
        objectTempt.append({"id": item[0],"description": item[1],"status": item[2]})
    return jsonify(objectTempt)
#ADD ROUTE WITH METHOD POST
@app.route('/api/add',methods = ['POST'])
def add():
    dataFromUser = json.loads(request.data)
    #connect to db then insert the value to db
    conn = sqlite3.connect('todoList.db')
    query = "INSERT INTO todo (description, status) VALUES ('{n}', 'Doing')".format(n = dataFromUser['itemDescription'])
    conn.execute(query)
    conn.commit()
    return redirect(url_for("index"))
#UPDATE ROUTE WITH METHOD POST
@app.route('/api/update',methods=['GET'])
def edit():
    idOfToDo = int(request.args.get("id"))
    #connect to db then update the value for database
    conn = sqlite3.connect('todoList.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo WHERE id = {id}".format(id =idOfToDo))
    rows = cur.fetchall()
    idCheckDoingOrNot = rows[0][2]# this use to check whether the job is Done or Doing
    # print(idCheckDoingOrNot=="Doing")
    if(idCheckDoingOrNot == "Doing"):
        query = "UPDATE todo SET 'status' = 'Done' WHERE id = {id}".format(id = int(idOfToDo))
        conn.execute(query)
        conn.commit()
    else:
        query = "UPDATE todo SET 'status' = 'Doing' WHERE id = {id}".format(id = int(idOfToDo))
        conn.execute(query)
        conn.commit()
    return redirect(url_for("index"))
#DELETE ROUTE WITH METHOD POST
@app.route('/api/delete',methods = ['GET'])
def delete():
    idOfToDo = int(request.args.get("id"))
    #connect to database then find the id of record and delete it
    conn = sqlite3.connect('todoList.db')
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM todo WHERE id = {id}".format(id =idOfToDo))
    query = "DELETE FROM todo WHERE id = {id}".format(id = int(idOfToDo))
    conn.execute(query)
    conn.commit()
    return redirect(url_for("index"))
#MAIN TO TEST  
if __name__ == '__main__':
    app.run()