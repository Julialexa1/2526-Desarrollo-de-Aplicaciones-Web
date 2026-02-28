from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField("Nombre del producto", validators=[
        DataRequired(), Length(min=3, max=50)
    ])
    tipo = StringField("Tipo", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired(), NumberRange(min=1)])
    precio = FloatField("Precio ($)", validators=[DataRequired(), NumberRange(min=0.1)])
    enviar = SubmitField("Guardar producto")