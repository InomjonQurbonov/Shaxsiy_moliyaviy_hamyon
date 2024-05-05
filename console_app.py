import datetime
from database import Database

db = Database()


# hisobni tekshirish
def check_balance(username):
    balance, _, _ = db.show_balance(username)
    return f"Hozirgi balansingiz: {balance} so'm"


# pul sarflash
def spend_money(username, amount):
    user_balance, _, _ = db.show_balance(username)
    if amount > user_balance:
        return "Yetarli mablag' yo'q"
    else:
        db.add_record(username, 'expense', amount)
        db.add_user_works(username, 'expense', amount)
        return f"{amount} so'm harajat qilingan. Yangi balans: {user_balance - amount} so'm"


# daromadni kiritish
def add_income(username, income):
    db.add_record(username, 'income', income)
    user_balance, _, _ = db.show_balance(username)
    db.add_user_works(username, 'income', income)
    return f"{income} so'm daromad kiritildi. Yangi balans: {user_balance + income} so'm"


# dasturni to'xtattis
def stop():
    return "Barcha harakatlaringiz to'xtatildi"


# harajat va daromadni sqlash txt faylga
def save_transaction(username, date, type, amount, description):
    with open("transactions.txt", "a") as file:
        file.write(f"Foydalanuvchi {username} \n")
        file.write(f"Sana: {date}\n")
        file.write(f"Turkum: {type}\n")
        file.write(f"Miqdori: {amount}\n")
        file.write(f"Tavsif: {description}\n\n")


# saqlangan txt faylni o'qish
def read_saved_transactions():
    try:
        with open("transactions.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Hali hech qanday ma'lumot saqlanmagan."


# Ilova buyruqlar
def commands(user, money):
    text = f"Salom xurmatli {user} \n"
    text += f"Hozirgi balnsingiz {money} - so'mni tashkil etadi \n"
    text += "Siz pastdagi istalgan buyruqdan foydalanishingiz mumkin \n"
    text += '\t Balance - Hozirgi balnsingizni tekshirish \n'
    text += '\t Spend - Harajat qilish \n'
    text += '\t Income - Siz keltirgan daromadni kiritish \n'
    text += '\t Update_Income - Siz keltirgan daromadni kiritish \n'
    text += '\t Update_Expense - Siz keltirgan daromadni kiritish \n'
    text += '\t Search - Barcha harajatlar orassidan qqidirish \n'
    text += '\t Stop - Barcha harakatlaringizni to`xtatish \n'
    return text


# harajatlarni yangilash
def update_income(username, new_income):
    db.edit_record(username, new_income)


# daromadlarni yangilash
def update_expense(username, new_expense):
    db.edit_record(username, new_expense)


# dasturni boshlash
print('<<<Shaxsiy moliyaviy hamyon>>>')

username = input("Ismingizni kiriting: ")
balance = float(input("Balansingizni kiriting: "))
user_id = db.get_users(username)

existing_user = db.show_balance(username)
if existing_user:
    confirmation = input(
        "Bu nomda foydalanuvchi allaqachon mavjud. Uni o'zgartirishni xohlaysizmi? (ha / yo'q): ").lower()
    if confirmation == "ha":
        db.edit_record(username, 'balance', balance)
    else:
        print("Oldincha mavjud bo'lgan foydalanuvchi saqlangan.")
else:
    db.create_users_and_balance(username, balance)

print(commands(username, balance))

while True:
    command = input("Buyruqni kiriting: ").strip().lower()
    if command == "balance":
        print(check_balance(username))
    elif command == "spend":
        amount = float(input("Bugungi harajatingizni kiriting: "))
        reason = input("Harajat sababini kiriting: ")
        print(spend_money(username, amount))
        save_transaction(username, datetime.datetime.now().strftime("%Y-%m-%d"), "Iste'mol", amount, reason)
    elif command == "income":
        income = float(input("Daromad miqdorini kiriting: "))
        reason = input("Daromad sababini kiriting: ")
        print(add_income(username, income))
        save_transaction(username, datetime.datetime.now().strftime("%Y-%m-%d"), "Daromad", income, reason)
    elif command == "update_income":
        new_income = float(input("Yangi daromad miqdorini kiriting: "))
        update_income(username, new_income)
        print("Daromad miqdori muvaffaqiyatli yangilandi.")
    elif command == "update_expense":
        new_expense = float(input("Yangi xarajat miqdorini kiriting: "))
        update_expense(username, new_expense)
        print("Xarajat miqdori muvaffaqiyatli yangilandi.")
    elif command == "search":
        search_type = input("Qidirish turini tanlang (category / date / amount / username): ").strip().lower()
        if search_type not in ["category", "date", "amount", "username"]:
            print("Noto'g'ri qidiruv turini kiritdingiz. Qaytadan urinib ko'ring.")
            continue
        category = None
        date = None
        amount = None
        if search_type == "category":
            category = input("Kategoriyani kiriting (income / expense): ").strip().lower()
        elif search_type == "date":
            date = input("Sana ni kiriting (YYYY-MM-DD): ").strip()
        elif search_type == "amount":
            amount = input("Miqdorni kiriting: ").strip()
        print(db.search_records(username, category, date, amount))
    elif command == "stop":
        print(stop())
        break
    else:
        print("Noto'g'ri buyruq! Iltimos, qaytadan urinib ko'ring.")

print(read_saved_transactions())
