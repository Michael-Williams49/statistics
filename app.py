import sqlite3
from flask import Flask, request, send_from_directory, abort
import os
import datetime
import uuid

app = Flask(__name__)
app.config['LOG_DB'] = 'logs.db'
app.config['RESOURCE_DB'] = 'resources.db'

def init_dbs():
    with sqlite3.connect(app.config['LOG_DB']) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id TEXT PRIMARY KEY,  
                resource_id TEXT,
                timestamp TEXT,
                ip_address TEXT,
                user_agent TEXT,
                referrer TEXT,
                FOREIGN KEY(resource_id) REFERENCES resources(id) 
            )
        ''')

    with sqlite3.connect(app.config['RESOURCE_DB']) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id TEXT PRIMARY KEY, 
                description TEXT,
                path TEXT
            )
        ''')

init_dbs()

@app.route('/<string:resource_id>')  
def track_and_serve(resource_id):
    log_id = str(uuid.uuid4())  
    timestamp = datetime.datetime.now().isoformat()
    ip_address = request.headers.get('X-Real-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent', '')
    referrer = request.headers.get('Referer', '')

    with sqlite3.connect(app.config['LOG_DB']) as conn:
        conn.execute('INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)', 
                     (log_id, resource_id, timestamp, ip_address, user_agent, referrer))

    with sqlite3.connect(app.config['RESOURCE_DB']) as conn:
        cursor = conn.execute('SELECT path FROM resources WHERE id = ?', (resource_id,))
        row = cursor.fetchone()

    if not row:
        abort(404)

    resource_path = row[0]
    if not os.path.exists(resource_path):
        abort(404)

    return send_from_directory(os.path.dirname(resource_path), os.path.basename(resource_path))

if __name__ == '__main__':
    app.run(debug=True)
