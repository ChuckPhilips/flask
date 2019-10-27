from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os

mysql = MySQL()
app = Flask(__name__)

if os.path.isfile('/run/secrets/db_pass'):
  f = open(os.environ['MYSQL_PASSWORD'], "r")
  dbpass = f.read().replace('\n','')
  f.close()

if os.path.isfile('/run/secrets/db_user'):
  f = open(os.environ['MYSQL_USER'], "r")
  dbuser = f.read().replace('\n','')
  f.close()

if os.path.isfile('/run/secrets/db_name'):
  f = open(os.environ['MYSQL_DATABASE'], "r")
  dbname = f.read().replace('\n','')
  f.close()

if "MYSQL_USER" in os.environ:
  dbuser = os.environ['MYSQL_USER']

if "MYSQL_PASSWORD" in os.environ:
  dbpass = os.environ['MYSQL_PASSWORD']

if "MYSQL_DATABASE" in os.environ:
  dbname = os.environ['MYSQL_DATABASE']

# MySQL configurations
#app.config['MYSQL_DATABASE_USER'] = dbuser
#app.config['MYSQL_DATABASE_PASSWORD'] = dbpass
#app.config['MYSQL_DATABASE_DB'] = dbname
#app.config['MYSQL_DATABASE_HOST'] = 'flask-mysql-service'
app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DATABASE']
app.config['MYSQL_DATABASE_HOST'] = 'flask-mysql-service'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    else:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
