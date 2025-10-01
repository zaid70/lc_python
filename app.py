from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests
import uuid
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ladies_collections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration (optional - for contact form)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-app-password'     # Replace with your app password

# Twilio WhatsApp configuration
app.config['TWILIO_ACCOUNT_SID'] = ''
app.config['TWILIO_AUTH_TOKEN'] = '61b4637797a78d20ad31d98119e1b3bf'
app.config['TWILIO_PHONE_NUMBER'] = 'whatsapp:+14155238886'  # Twilio's default WhatsApp sandbox number
app.config['TWILIO_WEBHOOK_URL'] = 'https://timberwolf-mastiff-9776.twil.io/demo-reply'  # Your Twilio Function URL

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Models
class JewelryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    whatsapp_upload_id = db.Column(db.String(100))  # To track WhatsApp message ID

@app.route('/whatsapp-webhook', methods=['POST'])
def handle_whatsapp():
    """Handle incoming WhatsApp messages"""
    # Create TwiML response
    resp = MessagingResponse()
    
    # Get message data
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    num_media = int(request.form.get('NumMedia', 0))
    from_number = request.form.get('From')
    message_sid = request.form.get('MessageSid')
    
    # Debug print
    print(f"Received message: {message}")
    print(f"Media URL: {media_url}")
    print(f"Number of media: {num_media}")
    print(f"Form data: {request.form}")
    
    # Only allow specific WhatsApp numbers (admins)
    allowed_numbers = ['whatsapp:+917892750820']  # Your WhatsApp number
    if from_number not in allowed_numbers:
        resp.message('❌ Unauthorized number')
        return str(resp)
        
    try:
        # Parse message format: 
        # Category | Name | Price | Description
        if '|' in message:
            parts = message.split('|')
            category = parts[0].strip()
            name = parts[1].strip()
            price = float(parts[2].strip())
            description = parts[3].strip() if len(parts) > 3 else ''
            
            # Handle image URL
            final_image_url = None
            if num_media > 0 and media_url:
                try:
                    # Download image using Twilio credentials
                    response = requests.get(
                        media_url,
                        auth=(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
                    )
                    
                    if response.status_code == 200:
                        # Generate unique filename
                        file_extension = '.jpg'  # Default to jpg for WhatsApp images
                        filename = f"{uuid.uuid4()}{file_extension}"
                        file_path = os.path.join('static', 'uploads', filename)
                        
                        # Save the file
                        with open(os.path.join(app.root_path, file_path), 'wb') as f:
                            f.write(response.content)
                        
                        # Set the URL to the local path
                        final_image_url = '/' + file_path.replace('\\', '/')
                        print(f"Image saved locally: {final_image_url}")
                    else:
                        print(f"Failed to download image: {response.status_code}")
                except Exception as e:
                    print(f"Error handling image: {str(e)}")
            
            # Create new jewelry item
            item = JewelryItem(
                category=category,
                name=name,
                price=price,
                description=description,
                image_url=final_image_url,
                whatsapp_upload_id=message_sid
            )
            
            db.session.add(item)
            db.session.commit()
            
            # Send confirmation via TwiML
            confirm_message = f'✅ Added new {category}: {name}\nPrice: ₹{price:,.2f}'
            if final_image_url:
                confirm_message += '\nImage: ✓ Successfully uploaded'
            else:
                confirm_message += '\nImage: ❌ No image received'
            resp.message(confirm_message)
            return str(resp)
        else:
            raise ValueError("Message format incorrect")
            
    except Exception as e:
        # Send error message via TwiML
        resp.message(f'❌ Error: {str(e)}\n\nCorrect format:\nCategory | Name | Price | Description\n\nExample:\nNecklaces | Gold Temple Necklace | 2499 | Beautiful traditional necklace')
        return str(resp)

# Authentication helper functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"DEBUG: Checking session for protected route. Session contents: {dict(session)}")
        if 'user_id' not in session or not session.get('logged_in'):
            print("DEBUG: No user_id or logged_in flag in session, redirecting to login")
            flash('🔒 Please log in to access the admin panel.', 'error')
            return redirect(url_for('login'))
        print(f"DEBUG: User authenticated, user_id: {session.get('user_id')}")
        return f(*args, **kwargs)
    return decorated_function

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    admin = User.query.filter_by(username='sabiha').first()
    if not admin:
        admin = User(
            username='sabiha',
            email='info@lcshop.in'
        )
        admin.set_password('admin123')  # Default password - should be changed
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: username='sabiha', password='admin123'")

# Database Models
class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.subject}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/collections')
def collections():
    """Collections page"""
    return render_template('collections.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if name and email and message and subject:
            try:
                # Save to database
                submission = ContactSubmission(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message
                )
                db.session.add(submission)
                db.session.commit()
                
                # Also try to send email notification (optional)
                try:
                    msg = Message(
                        subject=f"New Contact Form: {subject}",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=['info@lcshop.in']  # Replace with your email
                    )
                    msg.body = f"""
New contact form submission from Ladies Collections website:

Name: {name}
Email: {email}
Phone: {phone or 'Not provided'}
Subject: {subject}

Message:
{message}

Submitted at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

You can view all submissions in the admin panel: http://localhost:5000/admin
                    """
                    mail.send(msg)
                except Exception as email_error:
                    # Email failed but database save succeeded
                    print(f"Email notification failed: {email_error}")
                
                flash('Thank you! Your message has been received successfully. We will get back to you soon.', 'success')
                
            except Exception as e:
                db.session.rollback()
                flash('Sorry, there was an error submitting your message. Please try again or call us directly.', 'error')
                print(f"Database error: {e}")
                
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('contact.html')

@app.route('/store')
def store():
    """Store page"""
    return render_template('store.html')

@app.route('/collections/<category>')
def collections_category(category):
    """Display items for a specific category"""
    categories = {
        'necklaces': 'Necklaces',
        'earrings': 'Earrings',
        'bangles': 'Bangles'
    }
    
    if category not in categories:
        return render_template('404.html'), 404
        
    # Get items for this category
    items = JewelryItem.query.filter_by(category=categories[category])\
        .order_by(JewelryItem.created_at.desc()).all()
        
    return render_template(f'collections/{category}.html', 
                         items=items, 
                         category=categories[category])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['logged_in'] = True
            print(f"DEBUG: User logged in successfully. Session: {dict(session)}")
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/debug-session')
def debug_session():
    """Debug route to check session contents"""
    return f"Session contents: {dict(session)}"

@app.route('/test-auth')
@login_required
def test_auth():
    """Test route to verify authentication is working"""
    return "Authentication is working! You are logged in."

@app.route('/admin')
@login_required
def admin():
    """Admin panel for viewing contact submissions"""
    submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
    total_submissions = len(submissions)
    unread_count = ContactSubmission.query.filter_by(is_read=False).count()
    current_user = User.query.get(session['user_id'])
    return render_template('admin.html', 
                         submissions=submissions, 
                         total_submissions=total_submissions,
                         unread_count=unread_count,
                         current_user=current_user)

@app.route('/admin/submission/<int:submission_id>')
@login_required
def view_submission(submission_id):
    """View individual submission and mark as read"""
    submission = ContactSubmission.query.get_or_404(submission_id)
    
    # Mark as read
    if not submission.is_read:
        submission.is_read = True
        db.session.commit()
    
    return render_template('submission_detail.html', submission=submission)

@app.route('/admin/mark_read/<int:submission_id>')
@login_required
def mark_read(submission_id):
    """Mark submission as read"""
    submission = ContactSubmission.query.get_or_404(submission_id)
    submission.is_read = True
    db.session.commit()
    flash('Submission marked as read.', 'success')
    return redirect(url_for('admin'))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        create_admin_user()
        print("Database tables created successfully!")
    
    print("Starting Ladies Collections Flask Application...")
    print("Admin login available at: http://localhost:5000/login")
    print("Default credentials: username='sabiha', password='admin123'")
    app.run(debug=True)
