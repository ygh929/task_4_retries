from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waitlist.db'  # Or your preferred database URI
db = SQLAlchemy(app)

class WaitlistEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']

        if not full_name or not email:
            flash('Please enter both your full name and email address.', 'error')
            return redirect(url_for('index'))

        if db.session.query(WaitlistEntry).filter_by(email=email).first():
            flash('You are already on the waitlist!', 'info')
            return redirect(url_for('index'))


        try:  # Improved error handling
            new_entry = WaitlistEntry(full_name=full_name, email=email)
            db.session.add(new_entry)
            db.session.commit()
            flash('Thank you for joining the waitlist!', 'success')
            return redirect(url_for('index'))
        except Exception as e:  # Catching potential errors (e.g., database issues)
            db.session.rollback()  # Roll back the session in case of error
            flash(f"An error occurred: {e}", 'error') # More specific flash message
            return redirect(url_for('index'))



    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)