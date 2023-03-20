import pymysql
import getpass
import os
import hashlib
import random
import time

from flask import Flask, session

#PUSSY DON'T STEAL MY CODE GIMME CREDIT "MED MORTADHA"

app = Flask(__name__)
app.secret_key = os.urandom(24)

db = pymysql.connect(host="localhost", user="root", password="", db="woh")

cursor = db.cursor()
sql = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), dangers INT DEFAULT 0, password VARCHAR(255))"
cursor.execute(sql)

def register():
    email = input("Enter your email: ")
    password = getpass.getpass("Enter a password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "INSERT INTO users (email, dangers, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (email, 0, hashed_password))
    db.commit()
    print("Registration successful!")

def login():
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(sql, (email, hashed_password))
    result = cursor.fetchone()
    if result:
        session['user_email'] = email
        user_email = session.get('user_email')
        print("Login successful!")
        f = 0
        while True:
            with open("dangers.txt", "r") as f:
                dng  = f.read()
                new_f = int(''.join(filter(str.isdigit, dng)))
            if new_f != f:
                f = new_f
                dangers = f
                update_database(user_email, dangers)
                time.sleep(10)
    else:
        print("Invalid email or password.")


def update_database(user_email, dangers):
    sql = "UPDATE users SET dangers = %s WHERE email = %s"
    cursor.execute(sql, (dangers, user_email))
    db.commit()
    print("Database updated successfully.")

def main():
    with app.test_request_context():
        while True:
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                register()
            elif choice == "2":
                login()

            elif choice == "3":
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
