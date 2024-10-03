from flask import Flask, render_template, request, flash
from wtforms import Form, StringField, validators, EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Startup information
startup_name = "InnovateXYZ"  # Replace with your startup's name
startup_description = "Revolutionizing the widget industry with cutting-edge technology." # Replace with your startup's description
startup_tagline = "Building a better widget, one innovation at a time."  # Optional tagline

# Waitlist form
class WaitlistForm(Form):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(), validators.Email()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WaitlistForm(request.form)
    if request.method == 'POST' and form.validate():
        full_name = form.full_name.data
        email = form.email.data

        # TODO:  Handle data persistence (e.g., save to database or file)
        #  Here's a simple example of saving to a text file:
        with open("waitlist.txt", "a") as f:  
            f.write(f"{full_name},{email}\n")


        flash('Thanks for joining the waitlist!', 'success')  # Success message
        return render_template('index.html', form=form, startup_name=startup_name, startup_description=startup_description, startup_tagline=startup_tagline)

    return render_template('index.html', form=form, startup_name=startup_name, startup_description=startup_description, startup_tagline=startup_tagline)



if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production