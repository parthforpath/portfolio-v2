from flask import Flask, render_template, request, abort
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

from utils.data_loader import (
    load_projects,
    load_project_by_slug,
    load_blogs,
    load_blog_by_slug,
    load_experiences,
)

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
DATA_FILE = 'form_submissions.json'


@app.route('/')
def index():
    projects = load_projects()
    featured_projects = [project for project in projects if project.get('featured')]
    featured_blogs = load_blogs()[:2]
    return render_template('index.html', current_page='home', featured_projects=featured_projects, featured_blogs=featured_blogs)


@app.route('/about/')
def about():
    return render_template('about.html', current_page='about', experiences=load_experiences())


@app.route('/contact/')
def contact():
    return render_template('contact.html', current_page='contact')


@app.route('/work/')
def work():
    return render_template('portfolio.html', current_page='work', projects=load_projects())


@app.route('/project/<slug>/')
def project_detail(slug):
    project = load_project_by_slug(slug)
    if not project:
        abort(404)
    return render_template('portfolio-single.html', current_page='work', project=project)


@app.route('/blogs/')
def blogs():
    return render_template('blog.html', current_page='blogs', blogs=load_blogs())


@app.route('/blog/<slug>/')
def blog_detail(slug):
    blog = load_blog_by_slug(slug)
    if not blog:
        abort(404)
    return render_template('blog-single.html', current_page='blogs', blog=blog)


@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        form_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'company_name': request.form.get('company-name'),
            'website': request.form.get('website'),
            'interest': request.form.get('options-base'),
            'budget_range': request.form.get('budget-options'),
            'exact_budget': request.form.get('budget'),
            'timeline': request.form.get('timeline'),
            'message': request.form.get('message'),
        }

        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = []

        data.append(form_data)

        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        send_email(form_data)
        return 'Thank you! Your message has been sent.', 200
    except Exception as exc:
        return f'Error: {str(exc)}', 500


def send_email(data):
    sender_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    receiver_email = 'parthchopra111@gmail.com'

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
