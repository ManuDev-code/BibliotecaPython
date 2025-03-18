from flask import Flask, json, jsonify, render_template, request, redirect, url_for
from biblioteca import Biblioteca, Libro, Usuario, Prestamo, Bibliotecario
from datetime import datetime

app = Flask(__name__) #Creamos instancia de la aplicación Flask
biblioteca = Biblioteca() #Creamos instancia de la clase biblioteca
bibliotecario = Bibliotecario(1, "Sandro")

def cargar_datos():
    mensajes = []  # Lista para almacenar los mensajes de carga
    try:
        with open('datos.json', 'r') as f:
            contenido = f.read().strip()
            if not contenido:
                datos = {}
            else:
                datos = json.loads(contenido)

            for libro_data in datos.get('libros', []):
                disponible = libro_data.pop('disponible', True)
                libro = Libro(**libro_data)
                libro.disponible = disponible
                mensajes.append(f"Libro cargado: {libro.titulo}, codigo {libro.codigo}")
                
            for usuario_data in datos.get('usuarios', []):
                usuario_data.pop('Libros prestados', None)  # Eliminar libros
                usuario = Usuario(**usuario_data)
                biblioteca.usuarios.append(usuario)
                mensajes.append(f"Usuario cargado: {usuario.nombre}, ID: {usuario.id_usuario}")
                
            for prestamo_data in datos.get('prestamos', []):
                libro_data = prestamo_data['libro']
                usuario_data = prestamo_data['usuario']
                libro = next((libro for libro in biblioteca.libros if str(libro.codigo) == str(libro_data['codigo'])), None)
                usuario = next((usuario for usuario in biblioteca.usuarios if str(usuario.id_usuario) == str(usuario_data['id_usuario'])), None)
                
                if libro and usuario:
                    prestamo = Prestamo(
                        id_prestamo=prestamo_data['id_prestamo'],
                        libro=libro,
                        usuario=usuario,
                        fecha_prestamo=datetime.strptime(prestamo_data['fecha_prestamo'], '%Y-%m-%d'),
                        fecha_devolucion=datetime.strptime(prestamo_data['fecha_devolucion'], '%Y-%m-%d')
                    )
                    biblioteca.prestamos.append(prestamo)
                    
                    mensajes.append(f"Préstamo cargado: Libro {libro.titulo}, Usuario: {usuario.nombre}")

    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    
    return mensajes  # Regresamos la lista de mensajes

@app.route('/')
def index():
    mensajes = cargar_datos()  # Llamamos a cargar_datos para obtener los mensajes
    return render_template("index.html", mensajes=mensajes)  # Pasamos los mensajes al contexto de la plantilla

    # return render_template("index.html")


#Ruta para libros
@app.route("/libros", methods=['GET', 'POST'])
def manejar_libros():
    # Cargar los datos al inicio para asegurarte de que los libros estén disponibles
    mensajes = cargar_datos()

    if request.method == 'POST':
        # Cuando el usuario agrega un nuevo libro
        data = request.form.to_dict()
        nuevo_libro = Libro(
            codigo=data['codigo'],
            titulo=str(data['titulo']),
            autor=data['autor'],
            editorial=data['editorial'],
            año_publicacion=data['año_publicacion']
        )
        bibliotecario.añadir_libro(biblioteca, nuevo_libro)
        guardar_datos()  # Guardar los nuevos datos en el archivo
        return redirect(url_for('manejar_libros'))  # Redirigir para recargar la página con los libros actualizados
    
    elif request.method == 'GET':
        # Aquí asegúrate de que los libros estén disponibles
        return render_template("libros.html", libros=biblioteca.libros, mensajes=mensajes)

 
#ruta para usuarios  
@app.route("/usuarios", methods=['GET', 'POST'])
def manejar_usuarios():
    if request.method == 'POST':
        data = request.form.to_dict()
        nuevo_usuario = Usuario (
            id_usuario = str(data['id_usuario']),
            nombre = data['nombre'],
            email = data['email']
        )
        biblioteca.registrar_usuario(nuevo_usuario)
        guardar_datos()
        return redirect(url_for('manejar_usuarios'))
    elif request.method == 'GET':
        return render_template('usuarios.html', usuarios=biblioteca.usuarios)
    
#ruta para prestamos
@app.route("/prestamos", methods=['GET', 'POST'])
def gestionar_prestamos():
    if request.method == 'POST':
        data = request.form.to_dict()
        id_usuario = str(data['id_usuario'])
        codigo = str(data['codigo'])
        usuario = next((u for u in biblioteca.usuarios if str(u.id_usuario) == id_usuario), None)
        libro = next((l for l in biblioteca.libros if str(l.codigo) == codigo), None)
        if not usuario or not libro:
            return jsonify({'mensaje': 'Usuario o libro no encontrado'}), 404
        
        
        if 'fecha_prestamo' in data:
            if not libro.disponible:
                return jsonify({'mensaje': f'El libro "{libro.titulo}" ya está prestado'}), 404
            
            fecha_prestamo = datetime.strptime(data['fecha_prestamo'], '%Y-%m-%d')
            fecha_devolucion = datetime.strptime(data['fecha_devolucion'], '%Y-%m-%d')
            usuario.prestar_libros(libro)
            nuevo_prestamo = Prestamo (
                id_prestamo=len(biblioteca.prestamos) +1,
                libro=libro,
                usuario=usuario,
                fecha_prestamo=fecha_prestamo,
                fecha_devolucion=fecha_devolucion
            )
            biblioteca.prestamos.append(nuevo_prestamo)
            resultado = f"Libro {libro.titulo} prestado a {usuario.nombre}"
        else:
            #Verificar si el libro realmente está prestado
            prestamo = next((p for p in biblioteca.prestamos if str (p.libro.codigo) == codigo and str(p.usuario.id_usuario) == id_usuario), None)
            if not prestamo:
                return jsonify({'mensaje': f'El libro "{libro.titulo}" no está prestado al usuario {usuario.nombre}'}), 400
            
            usuario.devolver_libro(libro)
            biblioteca.prestamos.remove(prestamo)
            resultado = f"Libro {libro.titulo} devuelto por {usuario.nombre}"
        guardar_datos()
        return jsonify({'mensaje': resultado})
    
    
    
    
    elif request.method == 'GET':
        return render_template('prestamos.html', usuarios=biblioteca.usuarios, libros=biblioteca.libros, prestamos=biblioteca.prestamos)


def guardar_datos():
    try:
        with open('datos.json', 'w') as f:
            datos = {
                'libros': [libro.to_dict() for libro in biblioteca.libros],  # Usamos el método to_dict para serializar los libros
                'usuarios': [usuario.to_dict() for usuario in biblioteca.usuarios],  # Usamos el método to_dict para serializar los usuarios
                'prestamos': [prestamo.to_dict() for prestamo in biblioteca.prestamos]  # Usamos el método to_dict para serializar los préstamos
            }

            json.dump(datos, f, indent=4, default=str)  # Aseguramos que las fechas y cualquier objeto no serializable se conviertan en cadenas

    except Exception as e:
        print(f'Error al guardar los datos: {e}')
    
    
if __name__ == '__main__':
    cargar_datos()
    app.run(debug=True)