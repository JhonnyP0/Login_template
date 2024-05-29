from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    'user': os.getenv('user'),
    'password': os.getenv('pass'),  
    'host': os.getenv('host'),
    'port':os.getenv('port'),
    'database': os.getenv('db')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def welc():
    return render_template('welc.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login')



@app.route('/login_protocol', methods=['POST','GET'])
def login_protocol():
    if request.method=='POST':
        username=request.form['username']
        try:
            conn=get_db_connection()
            cur=conn.cursor()
            
            cur.execute("SELECT username, password FROM user_data WHERE username LIKE %s",["%"+username+"%"])
            data= cur.fetchone()

            if data:
                return render_template('access_granted.html')
            else:
                render_template('login.html',error="Something went wrong")
            cur.close()
        except Exception as e:
            error_message=str(e)
            return render_template('login.html', error=error_message)



@app.route('/signup_protocol', methods=['POST'])
def signup_protocol():
    try:
        name = request.form['name']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO user_data (username, password) VALUES (%s, %s)', (name, password))
    
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('signup'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300)
