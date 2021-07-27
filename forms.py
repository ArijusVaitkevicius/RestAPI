from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ItemEditForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    price = IntegerField('Price', [DataRequired()])
    qtty = IntegerField('Quantity', [DataRequired()])
    submit = SubmitField('submit')

class NewItemForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    price = IntegerField('Price', [DataRequired()])
    qtty = IntegerField('Quantity', [DataRequired()])
    submit = SubmitField('submit')
