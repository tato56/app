from flask import Flask, render_template, request
from datetime import date
import requests
import sqlite3
import random
import json

app = Flask(__name__)

def send_message_with_inline_keyboard(chat_id):
    url = f"https://api.telegram.org/bot6172402507:AAGn6IemgyYmqNF-aX-09vXXvwrX0XXaLxA/sendMessage"  # Замените <YOUR_BOT_TOKEN> на токен вашего бота

    inline_keyboard = [
    [
        {"text": "7:00", "callback_data": "button8"}
    ],
    [
        {"text": "8:00", "callback_data": "button9"}
    ],
    [
        {"text": "9:00", "callback_data": "button10"}
    ]
]

    keyboard = {
        "inline_keyboard": inline_keyboard
    }

    data = {
        "chat_id": chat_id,
        "text": 'Вы успешно купили курс',
        "reply_markup": json.dumps(keyboard)
    }

    response = requests.post(url, data=data)

def get_user_info(user_id):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        user_info = cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        con.commit()
        return user_info

def update_user_info(user_id, user_name1, user_name2, user_name3, user_sex, user_years, user_phone, user_address):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute('UPDATE users SET user_name1 = ?, user_name2 = ?, user_name3 = ?, user_years = ?, user_sex = ?, user_phone = ?, user_address = ? WHERE user_id=?', (user_name1, user_name2, user_name3, user_years, user_sex, user_phone, user_address, user_id,))
        con.commit()

def get1(name):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {name}")
        main = cur.fetchall()
    return main

def get2(id_, name):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {name} WHERE id = ?", (id_,))
        main = cur.fetchall()
    return main


def get_course_(id_, id_1, name):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {name}_course WHERE id_ = ? AND id = ?", (id_1, id_,))
        main = cur.fetchall()
    return main

def get_course(id_, name):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {name} WHERE id_ = ? ", (id_,))
        main = cur.fetchall()
    return main   

def get_id_(id_):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT id_ FROM main WHERE id = ?", (id_,))
        main = cur.fetchall()
    return main   

def get3(name):
    main = get1(name)
    items = []
    for row in main:
        item = Item(row[0], row[4], row[3])
        items.append(item)
    return items

def create(user_id, products_id):
    id_ = random.randint(4567, 7567)
    current_date = date.today()
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO "shop_history" (user_id, id, products_id, buy_date) VALUES (?, ?, ?, ?)', (user_id, id_, products_id, current_date,))
        main = cur.fetchall()
    return main   

def course_items(but_id, page):
    if page == 'main':
        id_ = get_id_(but_id)
        main = get_course(id_[0][0], 'main_course')
        items = []
        for row in main:
            item = Item(row[3], row[1], row[5])
            items.append(item)
    else:
        id_ = get_id_(but_id)
        main = get_course(id_[0][0], 'shop_course')
        items = []
        for row in main:
            item = Item(row[3], row[1], row[5])
            items.append(item)
    return items
        

@app.route('/profile_menu', methods=['GET'])
def profile_menu():
    user_id = request.args.get('id')
    user_info = get_user_info(user_id)
    user_name1 = user_info[2]
    user_name2 = user_info[3]
    user_name3 = user_info[4]
    user_sex = user_info[5]
    user_years = user_info[6]
    user_phone = user_info[7]
    user_address = user_info[8]
    if not user_info:
        return render_template('error.html')
    elif user_name1 == None:
        return render_template('profile_menu.html', name1='Имя', name2='Фамилия', name3='*Отчество', sex='Гендер', years='Возраст', phone='Номер', address='Адрес')
    else:
        return render_template('profile_menu.html', name1=user_name1, name2=user_name2, name3=user_name3, sex=user_sex, years=user_years, phone=user_phone, address=user_address)

@app.route('/profile_menu', methods=['POST'])
def profile_menu_post():
    user_id = request.args.get('id')
    user_name1 = request.form['user_name1']
    user_name2 = request.form['user_name2']
    user_name3 = request.form['user_name3']
    user_sex = request.form['user_sex']
    user_years = request.form['user_years']
    user_phone = request.form['user_phone']
    user_address = request.form['user_address']
    update_user_info(user_id, user_name1, user_name2, user_name3, user_sex, user_years, user_phone, user_address)
    return render_template('profile_menu.html', success=True)

@app.route('/ma')
def ma():
    page = request.args.get('page')
    page_id = request.args.get('page_id')
    button_id = request.args.get('id')
    course = get2(int(page_id) + 1, page)
    id_ = int(button_id) + 1
    get = get_course_(id_, course[0][4], page)
    return render_template('shop_menu/buy.html', url_logo=get[0][5], tag1=get[0][3], tag2=get[0][2], tag3=get[0][4], tag4=get[0][7])

@app.route('/ma', methods=['POST'])
def ma_post():
    get_data = request.get_json()
    get_datam = json.dumps(get_data)
    get_datam1 = json.loads(get_datam) 
    user_id = get_datam1["userid"]
    tovar_id = get_datam1["tovarid"]
    create(user_id, tovar_id)
    send_message_with_inline_keyboard(user_id)
    return render_template('shop_menu/buy.html', success=True)

class Item:
    def __init__(self, name, id_, image):
        self.name = name
        self.id_ = id_
        self.image = image

@app.route('/main_menu')
def main_menu():
    name = 'main'
    items = get3(name)
    return render_template('shop_menu.html', tag1=name, items=items)

@app.route('/shop_menu')
def shop_menu():
    name = 'shop'
    items = get3(name)
    return render_template('shop_menu.html', tag1=name, items=items)

@app.route('/shop_page')
def index2():
    page = request.args.get('page')
    if page == 'main':
        button_id = request.args.get('id')
        course = get2(int(button_id) + 1, 'main')
        items = course_items(int(button_id) + 1, 'main')
    else:
        button_id = request.args.get('id')
        course = get2(int(button_id) + 1, 'shop')
        items = course_items(int(button_id) + 1, 'shop')
    return render_template('shop_menu/example.html', items=items, tag1=course[0][0], tag2=course[0][2], url_logo=course[0][3])

@app.route('/error')
def er403():
    no = ''
    return render_template('shop_menu/error.html', url_logo='https://i.ibb.co/qdrhXmh/problem.gif', tag1='Ведется работа', tag2='Ведется работа перезайдите по позже', tag3=no, tag4=no)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', favicon='https://i.ibb.co/qdrhXmh/problem.gif', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)