#aplicaicon en flask
from flask import Flask, render_template,redirect, url_for,flash, request
from flask_wtf import flaskform
from wtforms import stringfield, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(_name_)

# clave secreta para formulario
app.config['SECRET_KEY']='mi_clave_secreta_123'
# app.config['WTF_CSRF_SECRET_KEY']='mi_clave_csrf_123'



@app.route('/')
def index():
   # return "Hola, Mundo!!!!!!!"
   return render_template('index.html', title='inicio')

@app.route('/producto/nuevo', methods=['GET', 'POST']) 
def nuevo_producto():

    class ProductoForm(FlaskForm):
        nombre = Stringfield('nombre del producto', validators=[DataRequired(), Length(min=2, maz=50)])  
        submit = SubmitmitField('Agregar Producto') 

        form = ProductoForm()
        if form.validate_on_submit():
            nombre_producto = form.nombre.data
            flash(f'producto "{nombre_producto}" agregar con exito', 'success')
            return redirect(url_for('index'))
        
        return render_template('form.html', title='Nuevo Producto', form=form)

@app.route('/usuario/<nombre!')
def usuario(nombre):
    retur f"Hola, {nombre!}"

@app.route('/about)
def about():
   # return "Esta es una aplicacion de ejemplo en flask."
   return render_template('about.html',title='Acerca de')

@app.route('/contacto')
def contacto():
    return "contacto con nosotros en"