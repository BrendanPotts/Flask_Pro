from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'DeckBuilder'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def showLogin():
    return render_template('login.html')

@app.route('/signup')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    cursor.callproc('sp_createUser', (_name, _email, _password))

    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})


@app.route('/admin')
def adminPage():
    return render_template('adminPage.html')

@app.route('/user')
def userPage():
    return render_template('userPage.html')

@app.route('/build')
def builDeck():
    return render_template('sub_page/buildDeck.html')
@app.route('/delete')
def delDeck():
    return render_template('sub_page/delDeck.html')


if __name__ == '__main__':
    app.run()
