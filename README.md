# Web-App-For-tokenized-group-submission
**Español:**
Este proyecto fue desarrollado para la última empresa en la que trabajé, un pequeño hotel que necesitaba un sistema para recopilar datos de sus clientes, almacenarlos localmente y exportarlos en formato Excel. Los datos recogidos se utilizan posteriormente para generar fichas que se suben a un sistema policial. La aplicación permite segmentar los formularios por grupos mediante tokens únicos, con una interfaz pública para los clientes y un panel de administración para gestionar grupos, ver respuestas y realizar exportaciones.

Está construido con Python (backend), SQLite (base de datos) y Vanilla JS (frontend), sin frameworks. Dado que se usa en grupos reducidos (20 a 40 personas, unas 2 veces por semana), SQLite es ideal por su simplicidad y portabilidad.

## 🚀 Funcionalidades

- Sistema de tokens únicos para organizar formularios por grupos
- Formulario público con aviso legal, protección de datos y firma digital
- Panel de administración para gestionar grupos y ver respuestas
- Exportación de datos a Excel
- Desarrollado sin frameworks: Vanilla JS (frontend) + Python (backend)
- Base de datos local con SQLite

---

## 🛠️ Tecnologías Utilizadas

- Python (biblioteca estándar, sin frameworks web)
- SQLite
- HTML/CSS/JavaScript (Vanilla)
- Exportación a Excel con Python

---

## 💻 Cómo Ejecutar el Proyecto en Local

### 1. Clona el repositorio

bash
git clone https://github.com/tuusuario/Nombredelformulario.git
cd Nombredelformulario

### 2. Ejecuta el script de base de datos

bash
python setup_db.py

### 3. Inicia la aplicación

bash
python app.py

### 4. Abre tu navegador en:

http://localhost:5000

**English:**
This project was built for the last company I worked with—a small hotel that needed a system to collect client data, store it locally, and export it to Excel for submission to a police system. The application allows for form segmentation using unique tokens, offering a public interface for guests and an admin panel to manage groups, view responses, and export data.

It's developed using Python (backend), SQLite (database), and Vanilla JS (frontend), without any frameworks. Since it's used in small group settings (20 to 40 people, twice a week), SQLite is the ideal solution due to its simplicity and portability.

## 🚀 Features

- Unique token system to assign and organize form groups
- Public form for guests with data privacy notice and digital signature
- Admin panel for group management and data review
- Export submissions to Excel
- Built with no frameworks: Vanilla JS (frontend) + Python (backend)
- Uses SQLite as a lightweight local database

---

## 🛠️ Technologies Used

- Python (standard library, no web frameworks)
- SQLite
- HTML/CSS/JavaScript (Vanilla)
- Excel export with Python

---

## 💻 How to Run the Project Locally

### 1. Clone the repository

bash
git clone https://github.com/yourusername/nameoftheform.git
cd nameoftheform

### 2. Set up the database

bash
python setup_db.py

### 3. Start the application

bash
python app.py

### 4. Open the app in your browser

http://localhost:5000
