# 🚀 Instalación y ejecución local del sistema de formulario

Este proyecto contiene un sistema web para gestión y registro de clientes dividido en grupos mediante tokens, desarrollado en **Python (Flask)**, **SQLite** y **Vanilla JS**.

---

## ✅ Requisitos previos

Antes de empezar asegúrate de tener instalado:

- Python 3.8+
- Pip
- SQLite3 (en la mayoría de sistemas ya viene instalado)
- Un navegador web

---

## 📄 Pasos de instalación

### 1. Descargar el proyecto

Copia o descarga todos los archivos del proyecto en una carpeta de tu ordenador, por ejemplo:

```
C:\proyectos\formulario_admin_system_sqlite
```

### 2. Crear entorno virtual

Abre una terminal y ve a la carpeta del proyecto:

```bash
cd C:\proyectos\formulario_admin_system_sqlite
```

Crea un entorno virtual:

```bash
python -m venv venv
```

Activa el entorno:

- En Windows:
```bash
venv\Scripts\activate
```

- En Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install flask flask-bcrypt flask-session pandas openpyxl
```

### 4. Crear la base de datos

```bash
sqlite3 data.db < schema_sqlite.sql
```

### 5. Crear el usuario administrador

```bash
python init_db_flask_bcrypt.py
```

Usuario y contraseña por defecto:

```
admin / 123456
```

✅ Podrás cambiar la contraseña luego desde la administración.

### 6. Ejecutar el servidor

```bash
python app.py
```

Accede a:
```
http://localhost:5000/admin/login
```

---

## 🔄 Reiniciar la base de datos (opcional para pruebas)

```bash
del data.db       # En Windows
# o
rm data.db        # En Linux/Mac

sqlite3 data.db < schema_sqlite.sql
python init_db_flask_bcrypt.py
```

---

## ✅ Estructura del proyecto

```
formulario_admin_system_sqlite/
├── app.py
├── db_config.py
├── schema_sqlite.sql
├── init_db_flask_bcrypt.py
├── templates/
├── static/
├── data.db
└── README_LOCAL.md
```