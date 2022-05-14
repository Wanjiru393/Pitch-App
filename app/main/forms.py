from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user


class PitchForm(FlaskForm):

    content = TextAreaField('Content', validators=[DataRequired()])

    category = SelectField('Category', choices=[(
        'General', 'General'), ('Pickuplines', 'Pickuplines'), ('Quotes', 'Quotes')], validators=[DataRequired()])

    submit = SubmitField('Pitch')


class CommentForm(FlaskForm):
    comment = StringField('Comment')
    submit = SubmitField('Comment')
