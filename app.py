from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary modification tracking
db = SQLAlchemy(app)  # Initialize SQLAlchemy

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        
        # Create new user in the database
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return f'User {name} added to the database!'
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
