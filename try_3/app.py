from flask import Flask, render_template, request, redirect, url_for, flash
from wtforms import Form, StringField, validators
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# SQLite database setup
DATABASE = 'waitlist.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.cursor().execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name TEXT NOT NULL, 
                             email TEXT UNIQUE NOT NULL)''')
        db.commit()
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

class RegistrationForm(Form):
    name = StringField('Full Name', [validators.Required()])
    email = StringField('Email Address', [validators.Required(), validators.Email()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        db = get_db()
        try:
            db.cursor().execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            db.commit()
            flash('Thank you for joining the waitlist!', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError: #Handles if the email is already in the database.
            flash('This email is already on the waitlist.', 'error')
        except Exception as e:  # Catch any other potential database errors.
            print(f"Database error: {e}")
            flash('An error occurred. Please try again later.', 'error')

    return render_template('index.html', form=form)



# --- Templates (index.html) ---
# Save this as templates/index.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>My Awesome Startup</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">  </head>
<body>
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h1>Join the Waitlist</h1>
            <p>We're building something amazing! Be among the first to know when we launch.</p>
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}


            <form method="POST" action="/">
                {{ form.hidden_csrf() }}
                <div class="form-group">
                    {{ form.name.label }}
                    {{ form.name(class="form-control") }}
                </div>
                <div class="form-group">
                    {{ form.email.label }}
                    {{ form.email(class="form-control") }}
                </div>
                <button type="submit" class="btn btn-primary">Join Now</button>
            </form>
            <p class="mt-3">Learn more about our startup <a href="#about">below</a>.</p>

            <section id="about" class="mt-5">
            <h2>About Us</h2>
                <p> We're revolutionizing the way people [describe your startup's area]. </p> 
                <p>[Add more details about your startup – its mission, what it does, etc.]</p>
            </section>

        </div>
    </div>
</div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True) 