"""Import flask app object"""
from app import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
    """sign up"""
    return User().signup()

@app.route('/user/signout')
def signout():
    """sign out"""
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    """login"""
    return User().login()
