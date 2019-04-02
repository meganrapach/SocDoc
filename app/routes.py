from flask import render_template, flash, redirect, url_for, request, jsonify

from app import app
from app.forms import LoginForm, CreateAccountForm, ContactUsForm

from app.email import send_email

from app.catalog import Catalog

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
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/catalog')
def catalog():
    catalog = Catalog()
    return render_template('catalog.html', title='Product Catalog', catalog=catalog)

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
        flash('Message sent from {}'.format(
            form.name.data))
        print(form.message)
        send_email('SocDoc Support Request',
                   'contactSocDoc@gmail.com', ['s0937372@monmouth.edu'],
                   'Name: {}\nReturn email: {}\nMessage Content: {}'.format(form.name.data, form.email.data, form.message.data))
        return redirect(url_for('index'))
    return render_template('contact.html', title='Contact Us', form = form)

@app.route('/createAccount', methods=['GET', 'Post'])
def createAccount():
    accountForm = CreateAccountForm()
    if accountForm.validate_on_submit():
        flash('New Account requested for user {}'.format(
            accountForm.firstName.data))
        return redirect(url_for('index'))
    return render_template('createAccount.html', title='Create Account', form = accountForm)
