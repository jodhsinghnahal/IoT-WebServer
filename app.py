import serial
import time
import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
database = 'sensordata.db'

def run(command, value):
    db = sqlite3.connect(database)
    line = db.cursor()
    all = line.execute(command, value).fetchall()
    db.commit()
    db.close()
    return all

@app.route("/")
def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(3)
    ser.reset_input_buffer()
    print("SERIAL OK")

    while True:
        time.sleep(0.01)
        if ser.in_waiting > 0:
            line = int(ser.readline().decode('utf-8').rstrip())
            all=run("INSERT INTO data VALUES (?)", (line,))
            render_template("index.html", data=all)
            print(line)
