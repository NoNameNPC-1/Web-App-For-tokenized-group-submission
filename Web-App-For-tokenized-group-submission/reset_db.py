import sqlite3
import bcrypt
import os

DB_PATH = 'data.db'

# Borrar archivo existente
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print('🗑️ Archivo data.db eliminado.')

# Crear base de datos y tablas
with open('schema_sqlite.sql', 'r') as f:
    schema = f.read()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.executescript(schema)
conn.commit()

# Crear admin
username = 'admin'
password = '123456'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

cursor.execute(
    "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
    (username, hashed.decode('utf-8'))
)
conn.commit()
conn.close()

print(f"✅ Base de datos inicializada.")
print(f"Usuario: {username}")
print(f"Contraseña: {password}")