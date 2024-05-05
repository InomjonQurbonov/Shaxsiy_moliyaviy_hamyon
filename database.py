import sqlite3
import datetime


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3')
        self.cursor = self.connection.cursor()

    def get_users(self, username):
        self.cursor.execute('SELECT id FROM users WHERE username=?', (username, ))
        return self.cursor.fetchall()

    def create_users_and_balance(self, username, balance):
        self.cursor.execute("INSERT INTO users (username, balance) VALUES (?, ?)", (username, balance))
        self.connection.commit()

    def show_balance(self, username):
        self.cursor.execute("SELECT balance, income, expense FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def add_record(self, username, category, amount):
        if category == 'income':
            self.cursor.execute("UPDATE users SET income = income + ?, balance = balance + ? WHERE username = ?",
                                (amount, amount, username))
        elif category == 'expense':
            self.cursor.execute("UPDATE users SET expense = expense + ?, balance = balance - ? WHERE username = ?",
                                (amount, amount, username))
        self.connection.commit()

    def edit_record(self, username, category, amount):
        if category == 'income':
            self.cursor.execute("UPDATE users SET income = ?, balance = income - expense WHERE username = ?",
                                (amount, username))
        elif category == 'expense':
            self.cursor.execute("UPDATE users SET expense = ?, balance = income - expense WHERE username = ?",
                                (amount, username))
        self.connection.commit()

    def add_user_works(self, username, category, amount):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO records (username, category, amount, date) VALUES (?, ?, ?, ?)",
                            (username, category, amount, current_date))
        self.connection.commit()

    def search_records(self, username, category=None, date=None, amount=None):
        query = "SELECT * FROM records WHERE username = ?"
        params = [username]

        if category:
            query += " AND category = ?"
            params.append(category)
        if date:
            query += " AND date = ?"
            params.append(date)
        if amount:
            query += " AND amount = ?"
            params.append(amount)

        self.cursor.execute(query, params)
        return self.cursor.fetchall()
