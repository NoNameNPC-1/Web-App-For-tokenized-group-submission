from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash, send_file
import sqlite3
from db_config import DB_PATH
import secrets
from functools import wraps
from flask_bcrypt import Bcrypt
from flask_session import Session
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'
app.config['SESSION_TYPE'] = 'filesystem'

bcrypt = Bcrypt(app)
Session(app)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_token():
    return secrets.token_hex(8)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
        admin = cursor.fetchone()
        conn.close()
        if admin and bcrypt.check_password_hash(admin['password_hash'], password):
            session['admin_id'] = admin['id']
            return redirect(url_for('list_groups'))
        else:
            flash('Credenciales incorrectas')
    return render_template('login.html')

@app.route('/admin/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('login'))

@app.route('/admin/groups')
@login_required
def list_groups():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, token FROM groups")
    groups = cursor.fetchall()
    conn.close()
    return render_template('groups.html', groups=groups, current_page='groups')

@app.route('/admin/create_group', methods=['POST'])
@login_required
def create_group():
    name = request.form.get('name')
    token = generate_token()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groups (name, token) VALUES (?, ?)", (name, token))
    conn.commit()
    conn.close()
    return redirect(url_for('list_groups'))

@app.route('/admin/delete_group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_groups'))

@app.route('/admin/clients')
@login_required
def list_clients():
    group_id = request.args.get('group_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    if group_id:
        cursor.execute("""
            SELECT clients.*, groups.name AS group_name 
            FROM clients 
            LEFT JOIN groups ON clients.group_id = groups.id 
            WHERE group_id = ?
        """, (group_id,))
    else:
        cursor.execute("""
            SELECT clients.*, groups.name AS group_name 
            FROM clients 
            LEFT JOIN groups ON clients.group_id = groups.id
        """)
    clients = cursor.fetchall()
    cursor.execute("SELECT id, name FROM groups")
    groups = cursor.fetchall()
    conn.close()
    return render_template('clients.html', clients=clients, groups=groups, selected_group=group_id, current_page='clients')

@app.route('/admin/delete_client/<int:client_id>', methods=['POST'])
@login_required
def delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_clients'))

@app.route('/admin/edit_client/<int:client_id>')
@login_required
def edit_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = cursor.fetchone()
    cursor.execute("SELECT id, name FROM groups")
    groups = cursor.fetchall()
    conn.close()
    if not client:
        return "Registro no encontrado", 404
    return render_template('edit_client.html', client=client, groups=groups)

@app.route('/admin/update_client/<int:client_id>', methods=['POST'])
@login_required
def update_client(client_id):
    data = request.form
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE clients SET
        full_name = ?, contact = ?, birth_date = ?, address = ?, zip_code = ?, country = ?,
        passport_number = ?, issuing_country = ?, date_of_issue = ?, date_of_expiration = ?,
        terms_accepted = ?, group_id = ?
        WHERE id = ?
    """
    values = (
        data.get('fullName'), data.get('contact'), data.get('birthDate'), data.get('address'),
        data.get('zipCode'), data.get('country'), data.get('passportNumber'), data.get('issuingCountry'),
        data.get('dateOfIssue'), data.get('dateOfExpiration'),
        True if data.get('terms') == 'on' else False,
        data.get('group_id') or None, client_id
    )
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return redirect(url_for('list_clients'))

@app.route('/admin/export')
@login_required
def export_clients():
    group_id = request.args.get('group_id')
    conn = get_db_connection()
    if group_id:
        query = """
            SELECT clients.id, full_name, contact, birth_date, address, zip_code, country,
                   passport_number, issuing_country, date_of_issue, date_of_expiration,
                   terms_accepted, groups.name AS group_name
            FROM clients 
            LEFT JOIN groups ON clients.group_id = groups.id
            WHERE group_id = ?
        """
        df = pd.read_sql_query(query, conn, params=(group_id,))
    else:
        query = """
            SELECT clients.id, full_name, contact, birth_date, address, zip_code, country,
                   passport_number, issuing_country, date_of_issue, date_of_expiration,
                   terms_accepted, groups.name AS group_name
            FROM clients 
            LEFT JOIN groups ON clients.group_id = groups.id
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clients')
    output.seek(0)
    return send_file(output, download_name='clients.xlsx', as_attachment=True)

@app.route('/formulario')
def formulario():
    token = request.args.get('token')
    if not token:
        return "Token is missing.", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM groups WHERE token = ?", (token,))
    group = cursor.fetchone()
    conn.close()
    if not group:
        return "Invalid token.", 400
    return render_template('form.html', group_id=group['id'], group_name=group['name'])

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.form
        signature = data.get('signature')
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO clients
            (full_name, contact, birth_date, address, zip_code, country, passport_number, 
             issuing_country, date_of_issue, date_of_expiration, terms_accepted, signature, group_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            data.get('fullName'), data.get('contact'), data.get('birthDate'), data.get('address'),
            data.get('zipCode'), data.get('country'), data.get('passportNumber'), data.get('issuingCountry'),
            data.get('dateOfIssue'), data.get('dateOfExpiration'),
            True if data.get('terms') == 'on' else False,
            signature, data.get('groupId')
        )
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Form submitted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error submitting form'}), 500

if __name__ == '__main__':
    app.run(debug=True)
