from flask import Flask, session, request, redirect, url_for, render_template_string
from functools import wraps

app = Flask(__name__)
app.secret_key = 'test-secret-key'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"DEBUG: Checking session. Session contents: {dict(session)}")
        if 'user_id' not in session:
            print("DEBUG: No user_id in session, redirecting to login")
            return "Please login first! <a href='/test-login'>Login</a>"
        print(f"DEBUG: User authenticated, user_id: {session.get('user_id')}")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return 'Home page. <a href="/admin">Admin</a> | <a href="/test-login">Login</a> | <a href="/logout">Logout</a>'

@app.route('/test-login')
def test_login():
    session['user_id'] = 1
    return 'Logged in! <a href="/admin">Go to Admin</a>'

@app.route('/logout')
def logout():
    session.clear()
    return 'Logged out! <a href="/">Home</a>'

@app.route('/admin')
@login_required
def admin():
    return 'Admin panel - you are authenticated!'

@app.route('/debug-session')
def debug_session():
    return f"Session contents: {dict(session)}"

if __name__ == '__main__':
    app.run(debug=True, port=5001)