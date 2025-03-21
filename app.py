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

@app.route('/users')
def users():
    # Query all users from the database
    users = User.query.all()
    return render_template('users.html', users=users)  # Render the users.html template

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

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Get the updated data from the form
        user.name = request.form['username']
        user.email = request.form['email']

        # Commit the changes to the database
        db.session.commit()
        return f'User {user.name} has been updated!'

    return render_template('update_user.html', user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Get the user by id
    user = User.query.get_or_404(user_id)

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return f'User {user.name} has been deleted!'


@app.route('/delete_confirm/<int:user_id>', methods=['GET', 'POST'])
def delete_user_confirm(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Delete the user if confirmed
        db.session.delete(user)
        db.session.commit()
        return f'User {user.name} has been deleted!'

    return render_template('delete_confirm.html', user=user)



if __name__ == '__main__':
    app.run(debug=True)
