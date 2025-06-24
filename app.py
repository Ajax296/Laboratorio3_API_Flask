# Importaciones necesarias para el funcionamiento de la API
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 

# Creacion de la aplicacion Flask y configuracion de la base de datos
app = Flask(__name__)
# Configuracion de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/tareasdb'
# Configuracion para evitar mensajes de modificacion de SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializacion de SQLAlchemy
db = SQLAlchemy(app)

# Definicion del modelo de datos para las tareas
class Tarea(db.Model):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    hecha = db.Column(db.Boolean, default=False)

# Creacion de la base de datos y las tablas, se usa app.app_context() para crear el contexto de la aplicacion
#Se modifico el antiguo codigo dado que usando @app.before_first_request no funcionaba correctamente
with app.app_context():
    db.create_all()

# Ruta principal de la API, muestra un mensaje de bienvenida
@app.route('/')
def index():
    return "API de Tareas"

# Ruta para consultar todas las tareas registradas en la base de datos
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    # Consulta todas las tareas y las devuelve en formato JSON
    tareas = Tarea.query.all()
    return jsonify([
        {'id': t.id, 'nombre': t.nombre, 'hecha': t.hecha} for t in tareas
    ])

# Ruta para crear una nueva tarea, recibe datos en formato JSON
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    # Asigna a `datos` el contenido JSON de la solicitud
    datos = request.json
    # Asigna a 'nueva' una nueva instancia de Tarea con el nombre proporcionado
    nueva = Tarea(nombre=datos['nombre'])
    # Adiciona la nueva tarea a la sesión de la base de datos y la guarda
    db.session.add(nueva)
    # Realiza el commit para guardar los cambios en la base de datos
    db.session.commit()
    # Devuelve un mensaje de éxito con el código de estado 201 (Creado)
    return jsonify({'mensaje': 'Tarea creada'}), 201

# Ruta para obtener una tarea por su ID, devuelve un error si no se encuentra
@app.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea(id):
    # Busca la tarea por su ID en la base de datos
    tarea = Tarea.query.get(id)
    # Si la tarea existe, devuelve sus detalles; si no, devuelve un error 404
    if tarea:
        return jsonify({'id': tarea.id, 'nombre': tarea.nombre, 'hecha': tarea.
    hecha})
    return jsonify({'error': 'No encontrada'}), 404

# Ruta para obtener tareas completadas, a partir de la columna 'hecha'
@app.route('/tareas/completadas', methods=['GET'])
def obtener_tareas_completadas():
    # Filtra las tareas por aquellas que están marcadas como hechas
    tareas = Tarea.query.filter_by(hecha=True).all()
    # Devuelve las tareas completadas en formato JSON
    return jsonify([
        {'id': t.id, 'nombre': t.nombre, 'hecha': t.hecha} for t in tareas
    ])

# Ruta para obtener tareas pendientes, a partir de la columna 'hecha'
@app.route('/tareas/pendientes', methods=['GET'])
def obtener_tareas_pendientes():
    # Filtra las tareas por aquellas que no están marcadas como pendientes
    tareas = Tarea.query.filter_by(hecha=False).all()
    # Devuelve las tareas pendientes en formato JSON
    return jsonify([
        {'id': t.id, 'nombre': t.nombre, 'hecha': t.hecha} for t in tareas
    ])

# Ruta para buscar tareas por una palabra clave en el nombre
@app.route('/tareas/buscar/<string:palabra>', methods=['GET'])
def obtener_tareas_por_palabra(palabra):
    # Filtra las tareas que contienen la palabra clave en su nombre, usando ilike para una búsqueda insensible a mayúsculas
    tareas = Tarea.query.filter(Tarea.nombre.ilike(f'%{palabra}%')).all()
    # Devuelve las tareas que coinciden con la búsqueda en formato JSON
    return jsonify([
        {'id': t.id, 'nombre': t.nombre, 'hecha': t.hecha} for t in tareas
    ])

# Ruta para actualizar una tarea existente, recibe datos en formato JSON
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    # Busca la tarea por su ID en la base de datos
    tarea = Tarea.query.get(id)
    # Si la tarea existe, actualiza sus campos con los datos proporcionados
    if tarea:
        # Asigna a `datos` el contenido JSON de la solicitud
        datos = request.json
        # Actualiza los campos de la tarea con los datos recibidos, si están presentes
        tarea.nombre = datos.get('nombre', tarea.nombre)
        tarea.hecha = datos.get('hecha', tarea.hecha)
        # Realiza el commit para guardar los cambios en la base de datos
        db.session.commit()
        # Devuelve un mensaje de éxito
        return jsonify({'mensaje': 'Tarea actualizada'})
    return jsonify({'error': 'No encontrada'}), 404

# Ruta para eliminar una tarea por su ID
@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    # Busca la tarea por su ID en la base de datos
    tarea = Tarea.query.get(id)
    # Si la tarea existe, la elimina de la base de datos
    if tarea:
        # Elimina la tarea de la sesión de la base de datos
        db.session.delete(tarea)
        # Realiza el commit para guardar los cambios en la base de datos
        db.session.commit()
        # Devuelve un mensaje de éxito
        return jsonify({'mensaje': 'Tarea eliminada'})
    return jsonify({'error': 'No encontrada'}), 404

# Punto de entrada para ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)