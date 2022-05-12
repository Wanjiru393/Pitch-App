from flask import Flask,render_template ,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import  DataRequired
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "secretkeypass"

#Initialize The DataBase
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    date_added =db.Column(db.DateTime, default=datetime.utcnow)

    #Create String

    def __repr__(self):
        return '<Name %r>' % self.name

    class SignForm(FlaskForm):
        name = StringField("Name", validators=[DataRequired()])
        email = StringField("Email", validators=[DataRequired()])
        submit = SubmitField("Submit")




# Create a Form Class
class SignForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/user/add', methods=['GET','POST'])
def add_user(form):
    form = SignForm()

    return render_template("add_user.html",form=form)







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
