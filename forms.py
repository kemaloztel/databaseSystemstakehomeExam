from flask_wtf import FlaskForm
from wtforms import StringField

class UpdateForm(FlaskForm):
    
    food_group_id = StringField('food_group_id: ')
    short_desc = StringField('short_desc: ')
    long_desc = StringField('long_desc: ')
    manufac_name = StringField('manufac_name: ')
    sci_name = StringField('sci_name: ')