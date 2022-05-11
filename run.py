from flask import Flask,render_template ,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import  DataRequired
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)


   # Create a Form Class
app.config['SECRET_KEY'] = "secretkeypass"
class SignForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def hello_world():
    return render_template('base.html')



#Create SignUp Page
@app.route('/signup',methods=['GET','POST'])
def signup():
    name = None
    form = SignForm()

    #Validation
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("User Added Successfully!")
    return render_template('signup.html',
        name=name,
        form=form)
