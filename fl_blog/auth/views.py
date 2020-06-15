from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from fl_blog.auth import auth
from fl_blog.auth.forms import LoginForm
from flask_login import login_required, logout_user
from fl_blog.db_model import User

# To protect a route so that it can only be accessed by authenticated users, use login_required decorator.
# if this route is accessed by a user who is not authenticated, it will intercepted and the request
# and send the user to the login page instead. The order of the decorator matters.
@auth.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # login_user() function is invoked to record the user as logged in for the user session.
            # The login_user() function takes the user to log in and an optional “remember me” Boolean,
            # which was also submitted with the form. A value of False for this argument causes the user
            # session to expire when the browser window is closed, so the user will have to log in again
            # next time. A value of True causes a long-term cookie to be set in the user’s browser, which
            # Flask-Login uses to restore the user session. The optional REMEMBER_COOKIE_DURATION configuration
            # option can be used to change the default one-year duration for the remember cookie
            login_user(user, form.remember_me.data)

            # If the login form was presented to the user to prevent unauthorized access to a protected URL
            # the user wanted to visit, then Flask-Login will have saved that original URL in the next query
            # string argument, which can be accessed from the request.args dictionary. If the next query string
            # argument is not available, a redirect to the home page is issued instead. The URL in next is
            # validated to make sure it is a relative URL, to prevent a malicious user from using this argument
            # to redirect unsuspecting users to another site.
            next = request.args.get('next')
            print(type(next))
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    print("form invalidated")
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))