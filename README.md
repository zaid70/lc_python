# Ladies Collections - Flask Web Application

A modern Flask web application for Ladies Collections jewelry store, featuring dynamic content management, contact forms, and responsive design.

## Features

✅ **Dynamic Website**: Python-powered backend with Flask
✅ **Template Inheritance**: Consistent design across all pages
✅ **Contact Form**: Working contact form with email functionality
✅ **Responsive Design**: Mobile-friendly layout
✅ **SEO Optimized**: Better search engine optimization
✅ **Easy Content Management**: Update content through Python code
✅ **Flash Messages**: User feedback for form submissions

## Installation & Setup

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 2. Installation Steps

1. **Navigate to the Flask app directory:**
   ```bash
   cd flask-app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. **Update app.py** with your email settings (for contact form):
   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password'
   ```

2. **Change the secret key** (for production):
   ```python
   app.secret_key = 'your-unique-secret-key-here'
   ```

### 4. Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## File Structure

```
flask-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template with common elements
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   └── contact.html      # Contact page with form
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Stylesheet
│   ├── js/
│   │   └── main.js      # JavaScript
│   └── images/          # Images and favicon
└── README.md           # This file
```

## Available Routes

- `/` - Home page
- `/about` - About Ladies Collections and Sabiha Rahman
- `/contact` - Contact form and store information
- `/collections` - Jewelry collections (to be implemented)
- `/collections/<category>` - Specific collection categories

## Adding New Pages

1. **Create a new route in app.py:**
   ```python
   @app.route('/new-page')
   def new_page():
       return render_template('new-page.html')
   ```

2. **Create the template file** in `templates/new-page.html`:
   ```html
   {% extends "base.html" %}
   {% block title %}New Page - Ladies Collections{% endblock %}
   {% block content %}
   <h1>Your content here</h1>
   {% endblock %}
   ```

## Email Configuration (Optional)

To enable contact form email functionality:

1. **For Gmail:**
   - Enable 2-factor authentication
   - Generate an App Password
   - Use the App Password in `app.config['MAIL_PASSWORD']`

2. **Update the recipient email:**
   ```python
   recipients=['info@lcshop.in']  # Change to your email
   ```

## Deployment

### For Production:
1. Set `app.run(debug=False)`
2. Use a proper WSGI server like Gunicorn
3. Set environment variables for sensitive data
4. Configure a reverse proxy (nginx)

### Quick Production Setup:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Customization

### Adding Products:
You can extend the application by:
1. Adding a database (SQLite/PostgreSQL)
2. Creating product models
3. Adding admin functionality
4. Implementing e-commerce features

### Styling:
- Modify `static/css/style.css` for design changes
- Update templates for layout modifications
- Add new CSS files and link them in base.html

## Support

For questions about the Flask application:
1. Check Flask documentation: https://flask.palletsprojects.com/
2. Review the code comments in app.py
3. Test each feature in development mode

## Original Static Site

The original HTML/CSS/JS files are preserved in the parent directory for reference.

---

**Ladies Collections (LC Shop)**  
Founded in 2007 by Sabiha Rahman  
Premium Jewelry Store in Koramangala, Bangalore