from flask import Flask,render_template ,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField,BooleanField,ValidationError
from wtforms.validators import  DataRequired,EqualTo,Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import UserMixin
from wtforms.widgets import TextArea


app = Flask(__name__)

#Add Database #SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fkjcprkpdmtgke:3da620cc3546cef8066ff0bd1335445ece84cb858b5344919318c4bd121df546@ec2-107-22-238-112.compute-1.amazonaws.com:5432/d6ab7t3gmljed8'
# 'mysql+pymysql://root:password123@localhost/our_users'

#Secret Key
app.config['SECRET_KEY'] = "secretkeypass"

#Initialize The DataBase
db = SQLAlchemy(app)
migrate = Migrate(app, db)



#Pitch Model
class Pitches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    content = db.Column(db.Text)
    author = db.Column(db.String())
    

#Pitch Form
class PitchForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    submit = StringField("Submit")


#Post Page
@app.route('/add-pitch', methods=['GET','POST'])
def add_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        pitch = Pitches(title=form.title.data, content=form.content.data,
        author=form.author.data
        )
        #Clear form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        
        #Add Pitch DataBase
        db.session.add(pitch)
        db.session.commit()

        flash("Pitch Added Successfully!")

    return render_template("add_pitch.html",
    form=form)










class Users(db.Model,UserMixin):
    #Defined tablename
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Passwords
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not areadable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


      #Create String
    def __repr__(self):
        return '<Name %r>' % self.name



@app.route('/dlete/<int:id>')
def delete(id):
    user_to_delete =Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)


    except:
        flash("Delete Failed!!")
        return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)

  


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2',message='Password should match')])
    password_hash2 =PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField("Submit")




# Create a Form Class
class SignForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data)
            user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash = ''
        flash("User Added Successfully!")
    our_users =Users.query.order_by(Users.date_added)

    return render_template("add_user.html",
    form=form,
    name=name,
    our_users=our_users)




#Create SignUp Page
@app.route('/signup',methods=['GET','POST'])
def signup():
    name = None
    form = SignForm()

    #Validation
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('signup.html',
        name=name,
        form=form)
