from flask import Flask, render_template, request, redirect
from biblioteca import Biblioteca, Libro, Usuario, Prestamo

app = Flask(__name__) #Creamos instancia de la aplicación Flask
biblioteca = Biblioteca() #Creamos instancia de la clase biblioteca

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/libros", methods=['GET', 'POST'])
def manejar_libros():
    if request.method == 'POST':
        data = request.form.to_dict()
        
    
    return render_template("libros.html")

if __name__ == '__main__':
    app.run(debug=True)