from flask import render_template, request, Blueprint, flash, redirect, url_for, session

from utils.utility import register_user, has_less_than_two_words, does_not_contain_at, login_user

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')

        if has_less_than_two_words(fullname):
            flash("Full name required, specify at least two names", category='error')
        elif len(username) < 4 or does_not_contain_at(username):
            flash("Username too short or is malformed", category='error')
        elif len(password) < 6:
            flash("Password must be at least six characters", category='error')
        else:
            data = await register_user(fullname=fullname, username=username, password=password)
            if data['success']:
                flash("Successfully registered", category='success')
                session['username'] = username
                session['fullname'] = fullname
                session['signup'] = True
                return redirect(url_for('auth.login'))
            else:
                flash(f"Error: {data['details']}", category='error')

    return render_template('register.html', loggedin=session.get('loggedin', False))


@auth.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if len(username) < 4 or does_not_contain_at(username):
            flash("Username too short or is malformed", category='error')
        elif len(password) < 6:
            flash("Password must be at least six characters", category='error')
        else:
            data = await login_user(username=username, password=password)
            print(data)
            if data['data']['loggedin']:
                session.update({
                    'fullname': data['data']['fullname'],
                    'username': data['data']['username'],
                    'token': data['data']['token'],
                    'signup': data['data']['signup'],
                    'loggedin': data['data']['loggedin'],
                    'created_at': data['data']['created_at'],
                    'token_expires': data['data']['token_expires']
                })
                flash("Successfully logged in", category='success')
                return redirect(url_for('views.home'))
            else:
                flash(f"Error: {data['details']}", category='error')

    return render_template('login.html', loggedin=session.get('loggedin', False))


@auth.route("/logout")
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.", category='info')
    return redirect(url_for('auth.login'))
