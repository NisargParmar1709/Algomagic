from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import UserSession

main = Blueprint('main', __name__)

from .models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/user_profile')
@login_required
def user_profile():
    
    user = {}
    
    user["first_name"] = current_user.first_name
    user["email"] = current_user.email
    return render_template('user_profile.html', user=user)

@main.route('/active_users')
@login_required
def active_users():

    active_sessions = UserSession.query.filter_by(active=True).all()
    active_users = [session.user for session in active_sessions]

    active_users = set(active_users)

    return render_template('active_users.html', active_users=active_users)