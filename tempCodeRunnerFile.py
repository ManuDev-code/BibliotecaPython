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