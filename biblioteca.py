class Libro:
    def __init__(self, codigo, titulo, autor, editorial, año_publicacion):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.año_publicacion = año_publicacion
        self.disponible = True
        
    def mostrar_info(self):
        return f"{self.titulo} por {self.autor}, codigo: {self.codigo}"
    
    def actualizar_disponibilidad(self, disponible):
        self.disponible = disponible
        estado = "disponible" if disponible	else "no disponible"
        print(f"El libro {self.titulo} ahora está {estado}")
        
        
    def to_dict(self):
        """Devuelve un diccionario con los atributos del libro."""
        return {
            'codigo': self.codigo,
            'titulo': self.titulo,
            'autor': self.autor,
            'editorial': self.editorial,
            'año_publicacion': self.año_publicacion,
            'disponible': self.disponible
        }
class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.libro_prestados = []
        
    def prestar_libros(self, libro):
        if libro.disponible:
            self.libro_prestados. append(libro)
            libro.actualizar_disponibilidad(False)
            print(f"Libro {libro.titulo} prestado a {self.nombre}.")
        else:
            print("Este libro no se encuentra disponible para prestar.")
            
    def devolver_libro(self, libro):
        if libro in self.libro_prestados:
            self.libro_prestados.remove(libro)
            libro.actualizar_disponibilidad(True)
            print(f"Libro {libro.titulo} devuelto por {self.nombre}.")
    
    def to_dict(self):
        """Devuelve un diccionario con los atributos del usuario, incluyendo 'email'."""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email  # Ahora se incluye el campo 'email'
        }
class Bibliotecario:
    def __init__(self, id_bibliotecario, nombre):
        self.id_bibliotecario = id_bibliotecario
        self.nombre = nombre
        
    def añadir_libro(self, biblioteca, libro):
        biblioteca.libros.append(libro)
        print(f"Libro {libro.titulo} añadido al sistema.")
        
    def eleminar_libro(self, biblioteca, libro):
        if libro in biblioteca.libros:
            biblioteca.libros.remove(libro)
            print(f"Libro {libro.titulo} eliminado del sistema.")
            
class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []
        self.bibliotecarios = []
        self.prestamos = []
            
    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)
        print(f"Usuario {usuario.nombre} registrado en el sistema")
    
    def eliminar_usuario(self,usuario):
        if usuario in self.usuarios:
            self.usuarios.remove(usuario)
            print(f"Usuario {usuario.nombre} eliminado del sistema.")
            
    def listar_libros(self):
        for libro in self.libros:
            print(libro.mostrar_info())
            
    def listar_usuarios(self):
        for usuario in self.usuarios:
            print(f"{usuario.nombre}, Email: {usuario.email}")
            
class Prestamo:
    def __init__(self, id_prestamo, libro, usuario, fecha_prestamo, fecha_devolucion):
        self.id_prestamo = id_prestamo
        self.libro = libro
        self.usuario= usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        
    def finalizar_prestamo(self):
        print(f"""Prestamo del libro {self.libro.titulo} finalizado.
              Debe ser devuelto por {self.usuario.nombre} antes de {self.fecha_devolucion}.""")
        
    def to_dict(self):
        """Devuelve un diccionario con los atributos del préstamo."""
        return {
            'id_prestamo': self.id_prestamo,
            'libro': self.libro.to_dict(),  # Usamos el método to_dict del libro para serializarlo
            'usuario': self.usuario.to_dict(),  # Usamos el método to_dict del usuario para serializarlo
            'fecha_prestamo': self.fecha_prestamo.strftime('%Y-%m-%d'),  # Convertimos las fechas a cadenas
            'fecha_devolucion': self.fecha_devolucion.strftime('%Y-%m-%d')
        }
