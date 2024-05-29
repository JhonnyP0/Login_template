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
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO user_data (username, password) VALUES (%s, %s)', (name, password))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/welc')
def singup():
    return render_template('welc.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5300)
