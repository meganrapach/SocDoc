from flask import render_template, flash, redirect, url_for, request, jsonify, session

from app import app
from app.forms import LoginForm, CreateAccountForm, ContactUsForm

from app.email import send_email

from app.catalog import Catalog

import requests

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Megan'}
    posts = [
        {
            'author': {'username': 'Matt'},
            'body': 'Beautiful day in Toms River!'
        },
        {
            'author': {'username': 'Kendall'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'Post'])
def login():
    form = LoginForm()

    if 'logged_in' not in session or session['logged_in'] == False:
        if form.validate_on_submit():
            user = form.username.data
            password = form.password.data
        
            #flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
            URL = "https://ofe3yhbyec.execute-api.us-east-1.amazonaws.com/beta/socdoc-login?username=%s&password=%s" % (user, password)
            print(URL)
            r = requests.get(url = URL)
            print("\n")
            print(r.json())

            if r.json() == "verified":
                session['logged_in'] = True
                print(session.get('logged_in'))
                flash('Login successful! Welcome %s' % (user))
                #session['logged_in'] = False
                #print(session.get('logged_in'))
                return redirect(url_for('index'))

        return render_template('login.html', title = 'Sign In', form = form)

    if 'logged_in' in session and session['logged_in'] == True:
        flash('You are already logged in')
        return render_template('login.html', title = 'Sign In', form = form)
        
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout', methods=['GET', 'Post'])
def logout():
    if 'logged_in' in session and session['logged_in'] == True:
        session['logged_in'] = False
        print('logged out')
        flash("You have been logged out")
        return redirect(url_for('index'))
    flash('You are not logged in!')
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    catalog = Catalog()
    return render_template('catalog.html', title='Product Catalog', catalog=catalog)

@app.route('/products')
def products():
    catalog = Catalog()
    return render_template('products.html', title='Product List', catalog=catalog)

@app.route('/itemDetail')
def itemDetail():
    catalog = Catalog()

    if request.method == 'GET':
        item = request.args.get('item', '')
        print(type(item))
        print(item)
    else:
        item = "Placeholder"

    for index in range(len(catalog.items)):
        for key in catalog.items[index]:
            if catalog.items[index][key] == item:
                item = catalog.items[index]
                print(item)
    
    #item = request.args.get('item')
    #itemj = jsonify(item)
    #print(type(item))
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(itemj)
    return render_template('itemDetail.html', title='Product Detail', item=item, catalog=catalog)

@app.route('/about')
def about():
    return render_template('about.html', title='About SocDoc')

@app.route('/returnPolicy')
def returnPolicy():
    return render_template('returnPolicy.html', title='Return Policy')

@app.route('/termsOfService')
def termsOfService():
    return render_template('termsOfService.html', title='Terms of Service')

@app.route('/privacyPolicy')
def privacyPolicy():
    return render_template('privacyPolicy.html', title='Privacy Policy')

@app.route('/trackOrder')
def trackOrder():
    return render_template('trackOrder.html', title='Track Order')

@app.route('/cart')
def cart():
    return render_template('cart.html', title='Your Cart')

@app.route('/contact', methods=['GET', 'Post'])
def contact():
    form = ContactUsForm()
    if form.validate_on_submit():
        #flash('Message sent from {}'.format(
        #    form.name.data))
        print(form.message)
        #send_email('SocDoc Support Request',
        #           'contactSocDoc@gmail.com', ['s0937372@monmouth.edu'],
        #           'Name: {}\nReturn email: {}\nMessage Content: {}'.format(form.name.data, form.email.data, form.message.data))
        return redirect(url_for('index'))
    return render_template('contact.html', title='Contact Us', form = form)

@app.route('/createAccount', methods=['GET', 'Post'])
def createAccount():
    #URL = "https://ofe3yhbyec.execute-api.us-east-1.amazonaws.com/beta/testapicall"
    
    accountForm = CreateAccountForm()
    if accountForm.validate_on_submit():
        first = accountForm.firstName.data
        last = accountForm.lastName.data
        zipCode = accountForm.zipCode.data

        user = accountForm.email.data
        password = accountForm.password.data

        if accountForm.check_password(password):
            URL = "https://ofe3yhbyec.execute-api.us-east-1.amazonaws.com/beta/socdoc-create-account?username=%s&password=%s&firstname=%s&lastname=%s&zipcode=%s" % (user, password, first, last, zipCode)
            print(URL)
            r = requests.get(url = URL)
            print("\n")
            print(r.json())
            #print(type(r.json()))
            #flash('New Account requested for user {}'.format(accountForm.firstName.data))
            return redirect(url_for('createAccount_success', first = first, last = last, user = user))
    
    return render_template('createAccount.html', title='Create Account', form = accountForm)

@app.route('/createAccount_success', methods=['GET', 'Post'])
def createAccount_success():

    if request.method == 'GET':
        first = request.args.get('first', '')
        last = request.args.get('last', '')
        user = request.args.get('user', '')
        print(type(user))
        print(user)
    else:
        user = "Placeholder"
    
    return render_template('createAccount_success.html', title='Account Created!', first = first, last = last, user = user)

@app.route('/createAccount_fail')
def createAccount_fail():
    return render_template('createAccount_fail.html', title='Unable to Create Account')
