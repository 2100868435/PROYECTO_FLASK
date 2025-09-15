# app.py
from flask import Flask, render_template, request, redirect, session
from conexion.conexion import get_db_connection, create_tables
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # cámbiala en producción

# Asegurar que la BD y tablas existen
create_tables()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/productos')
    return redirect('/login')

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
                        (nombre, email, password))
            conn.commit()
            conn.close()
            return render_template('resultado.html', titulo="Registro exitoso",
                                   mensaje="Usuario registrado correctamente.",
                                   volver_url="/login")
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('resultado.html', titulo="Error",
                                   mensaje="El email ya está en uso.",
                                   volver_url="/register")
    return render_template('registro.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            return redirect('/productos')
        else:
            return render_template('resultado.html', titulo="Error de login",
                                   mensaje="Credenciales inválidas.",
                                   volver_url="/login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Listar productos
@app.route('/productos')
def mostrar_productos():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

# Crear producto
@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO productos (nombre, descripcion, precio, cantidad) VALUES (?, ?, ?, ?)",
                    (nombre, descripcion, precio, cantidad))
        conn.commit()
        conn.close()
        return redirect('/productos')
    return render_template('crear_producto.html')

# Editar producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        cur.execute("UPDATE productos SET nombre=?, descripcion=?, precio=?, cantidad=? WHERE id=?",
                    (nombre, descripcion, precio, cantidad, id))
        conn.commit()
        conn.close()
        return redirect('/productos')
    producto = conn.execute("SELECT * FROM productos WHERE id=?", (id,)).fetchone()
    conn.close()
    if producto is None:
        return render_template('resultado.html', titulo="No encontrado",
                               mensaje="Producto no encontrado.", volver_url="/productos")
    return render_template('editar_producto.html', producto=producto)

# Eliminar producto
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')

# Ver usuarios (solo ejemplo)
@app.route('/usuarios')
def usuarios():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    usuarios = conn.execute("SELECT id, nombre, email FROM usuarios").fetchall()
    conn.close()
    return render_template('usuarios_formulario.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
