import serial
import time
import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
database = 'sensordata.db'

def run(command, value):
    db = sqlite3.connect(database)
    line = db.cursor()
    line.execute(command, value).fetchall()
    db.commit()
    db.close()
    db2 = sqlite3.connect(database)
    f = db2.cursor()
    all = f.execute("SELECT * FROM data").fetchall()
    db2.close()
    return all

@app.route("/")
def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(1)
    ser.reset_input_buffer()
    print("SERIAL OK")

    while True:
        time.sleep(0.01)
        if ser.in_waiting > 0:
            line = int(ser.readline().decode('utf-8').rstrip())
            all=run("INSERT INTO data VALUES (?)", (line,))
            print(all)
            return render_template("index.html", data=all)
