from flask import render_template, redirect, url_for, flash
from app_alchemy import create_app
from models import db, Usuario
from forms import NombreForm

app = create_app()

@app.route("/", methods=["GET", "POST"])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        nuevo_usuario = Usuario(nombre=form.nombre.data)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario agregado con éxito", "success")
        return redirect(url_for("formulario"))
    return render_template("formulario.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
