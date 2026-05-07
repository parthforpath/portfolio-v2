from flask import Flask,render_template, request, jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

# Load variables from .env file
load_dotenv()

app = Flask(__name__)

DATA_FILE = 'form_submissions.json'

sender_email = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

@app.route('/')
def index():
    return render_template('index.html', current_page='home')

@app.route('/about/')
def about():
    return render_template('about.html', current_page='about')

@app.route('/contact/')
def contact():
    return render_template('contact.html', current_page='contact')

@app.route('/work/')
def work():
    return render_template('portfolio.html', current_page='work')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Parse form data
        form_data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "company_name": request.form.get('company-name'),
            "website": request.form.get('website'),
            "interest": request.form.get('options-base'),
            "budget_range": request.form.get('budget-options'),
            "exact_budget": request.form.get('budget'),
            "timeline": request.form.get('timeline'),
            "message": request.form.get('message')
        }

        # Save to JSON file
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = []

        data.append(form_data)

        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        # Send email
        send_email(form_data)

        return "Thank you! Your message has been sent.", 200

    except Exception as e:
        return f"Error: {str(e)}", 500


def send_email(data):
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver_email = "parthchopra111@gmail.com"  # send to yourself

    subject = f"New Inquiry from {data['name']}"

    body = f"""
    New Contact Form Submission:

    Name: {data['name']}
    Email: {data['email']}
    Phone: {data['phone']}
    Company Name: {data['company_name']}
    Website: {data['website']}
    Interested In: {data['interest']}
    Budget Range: {data['budget_range']}
    Exact Budget: {data['exact_budget']}
    Timeline: {data['timeline']}
    Message: {data['message']}
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

