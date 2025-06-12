from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)

# Configure Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

# Database model
class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize DB (only needed once)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message_text = request.form['message']

    # Save to database
    new_message = MessageModel(name=name, email=email, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    # Send email
    msg = Message(f"Message from {name}", sender=email, recipients=['your_email@gmail.com'])
    msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}"
    mail.send(msg)

    flash("Message sent and saved successfully!")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
