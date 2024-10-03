from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waitlist.db'  # Use SQLite; change if needed
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

with app.app_context():  # Create the database
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if not name or not email:
            flash('Please fill in both name and email fields.', 'error') 
            return redirect(url_for('index'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('You are already on the waitlist!', 'info')
            return redirect(url_for('index'))


        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for joining the waitlist!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)