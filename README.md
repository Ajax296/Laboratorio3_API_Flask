# Laboratorio 3 - API Flask con PostgreSQL

## 🚀 Instrucciones de ejecución

1. **Crear base de datos**
   - Abrir psql en el buscador de windows
   - Ingresar contraseña de PostgreSQL
   - Ejecutar el siguiente comando en psql
   ```bash
   CREATE DATABASE tareasdb;

3. **Clonar el repositorio (abrir GitBash)**:
   ```bash
   git clone https://github.com/Ajax296/Laboratorio3_API_Flask.git
   cd Laboratorio3_API_Flask
   
4. **Configurar el entorno virtual**
   ```bash
   python -m venv venv
   code .

5. **Activar entorno virtual e instalar dependencias**
   - Abrir una nueva terminal en VSCode
   - Ejecutar los siguientes comandos en la terminal
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt

6. **Ejecutar la API (Desde la terminal de VSCode)**
   ```bash
   python app.py

7. **Acceder a la API**
   ```bash
   http://localhost:5000
