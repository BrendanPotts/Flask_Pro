from flask import Flask, session, redirect, url_for, escape, request, render_template, json
from hashlib import md5
import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="deckbuilder")
cursor = db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['inputName']
        password_form  = request.form['inputPassword']
        cursor.execute("SELECT COUNT(1) FROM tbl_user WHERE user_name = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cursor.fetchone()[0]:
            cursor.execute("SELECT user_password FROM tbl_user WHERE user_name = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cursor.fetchall():
                if md5(password_form).hexdigest() == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)

@app.route('/login',  methods=['GET', 'POST'])
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

    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

    data = cursor.fetchall()

    if len(data) is 0:
        db.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})

@app.route('/usercreated')
def userCreated():
    return render_template('usercreated.html')

@app.route('/addCard')
def showCardCreate():
    return render_template('sub_page/addCard.html')

@app.route('/addCard', methods=['POST'])
def addCard():
    _cname = request.form['c_name']
    _ctype = request.form['c_type']

    cursor.callproc('sp_createCard', (_cname, _ctype))

    data = cursor.fetchall()

    if len(data) is 0:
        db.commit()
        return json.dumps({'message': 'Card created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})


@app.route('/admin')
def adminPage():
    return render_template('adminPage.html')

@app.route('/addUser')
def showAddUser():
    return render_template('sub_page/addUser.html')

@app.route('/addUser', methods=['POST'])
def addUser():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    _hashed_password = generate_password_hash(_password)
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

    data = cursor.fetchall()

    if len(data) is 0:
        db.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})

@app.route('/user')
def userPage():
    return render_template('userPage.html')

@app.route('/build')
def buildDeck():
    return render_template('sub_page/buildDeck.html')

@app.route('/adminBuild')
def adminBuild():
    return render_template('sub_page/adminBuild.html')

@app.route('/delete')
def delDeck():
    return render_template('sub_page/delDeck.html')


if __name__ == '__main__':
    app.run(debug=True)
