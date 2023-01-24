from flask import (
            Flask,
            flash,  # система сообщений
            redirect,
            render_template,
            request,
            session,
            url_for)
import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Qsrdv8z\n\xec]/'
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO patients (created, surname, name, patronymic, test, result) VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.date.today().strftime('%d-%m-%Y'), 'Алексеев', 'Валерий', 'Юрьевич', 'Опросник ЦС А', 56)
            )
connection.commit()
connection.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('main_page.html')
# TODO: добавить возможность прохождения теста из личного кабинета врача или как гость


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')


@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if 'user' in session:
        return redirect(url_for('user'))

    if request.method == 'POST':
        username = request.form.get('login')  # запрос к данным формы
        password = request.form.get('password')

        if username == 'admin' and password == 'pass':
            user = {'login': username, 'password': password}
            session['user'] = user
            flash('Добро пожаловать, '+username)
            return redirect(url_for('user'))
        else:
            message = "Неверный логин или пароль, попробуйте ещё"

    return render_template('login.html', message=message)


@app.route('/user/')
def user():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()
    return render_template('user.html', patients=patients)


@app.route('/test/sensitisation/', methods=['GET', 'POST'])
def sensitisation():
    test = 'Опросник ЦС А'
    if request.method == 'POST':
        session['patient'] = request.form.get('patient')
        session['result'] = request.form.get('result')
        session['date'] = datetime.date.today().strftime('%d-%m-%Y')

        patientname = session['patient'].strip().split()

        with sqlite3.connect("database.db") as con:
            cur = con.cursor()

            if len(patientname) == 3:
                cur.execute("INSERT INTO patients (created, surname, name, patronymic, test, result) VALUES (?, ?, ?, ?, ?, ?)",
                            (session['date'], patientname[0], patientname[1], patientname[2], test, int(session['result']))
                            )
            elif len(patientname) == 2:
                cur.execute("INSERT INTO patients (created, surname, name, test, result) VALUES (?, ?, ?, ?, ?)",
                            (session['date'], patientname[0], patientname[1], test, int(session['result']))
                            )
            con.commit()

        flash('Вы успешно сохранили результат')
        print(session)
        return redirect(url_for('index'))

    return render_template('sensitisation.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

