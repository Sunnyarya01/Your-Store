import base64
import os
from sqlalchemy import text
from application import app
from flask import flash, g, redirect, render_template, request, session, url_for

from application.models import Product, User
from application.database import db

@app.route('/', methods=['GET'])
def home():
    if g.user and session['role']=="admin":
        return redirect('/admin_dashboard')
    if g.user:
        return redirect('/customer/'+str(session['id']))
    products = Product.query.all()
    products = sorted(products, key=lambda x: x.id)
    for product in products:
        if product.image:
            product.image=base64.b64encode(product.image).decode('utf-8')
    return render_template('index.html', products=products)

app.secret_key=os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        session.pop('user', None)
        session.pop('role', None)
        session.pop('id', None)
        username = request.form['username']
        password = request.form['password']
        query = text("SELECT * FROM users WHERE username = :username")
        result = db.session.execute(query, {'username': username})
        user = result.fetchone()        
        if user!=None and username == user.username and password == user.password:
            id = int(user.id)
            session['user'] = username
            session['role'] = user.role
            session['id'] = user.id
            if user.role=="admin":
                return redirect('/admin_dashboard')
            return redirect('/customer/'+str(id))
        else:
            flash("Invalid username or password")
            return render_template('login.html')
    else:
        return render_template("login.html")
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    session.pop('id', None)
    return redirect('/')


@app.route('/customer/<int:id>')
def customer(id):
    if g.user:
        user = db.get_or_404(User, id)
        products = Product.query.all()
        products = sorted(products, key=lambda x: x.id)
        for product in products:
            if product.image:
                product.image = base64.b64encode(product.image).decode('utf-8')
        return render_template('customer_dashboard.html', user = user, products=products)
    return redirect('/login')

@app.route('/admin_dashboard', methods=['GET'])
def get_all_user():
    if g.user and session['role']=="admin":
        users_all = User.query.all()
        users_all = sorted(users_all, key=lambda x: x.id)
        products_all = Product.query.all()
        products_all = sorted(products_all, key=lambda x: x.id)
        for product in products_all:
            if product.image:
                product.image = base64.b64encode(product.image).decode('utf-8')
        return render_template('admin_dashboard.html', products_all = products_all, users_all = users_all, id = session['id'])
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        city = request.form['city']
        mobile_no = request.form['mobile_no'] 
        email = request.form['email']
        if email == 'admin@yourstore.com' and password=="Sunny@admin":
            role = 'admin'
        else:
            role = 'customer'
        users = User.query.filter_by(username=username).all()
        if len(users)==1:
            return ('Users already exist')
        else:
            user = User(name=name, username=username,age=age,role=role,city=city,password=password,mobile_no=mobile_no,email=email)
            db.session.add(user)
            db.session.commit()
            users = User.query.filter_by(username=username).all()
            if g.user and session['role']=='admin':
                return redirect('/admin_dashboard')
            return redirect(url_for('login'))

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    if g.user and session['role']=="admin":
        user = db.get_or_404(User, id)

        db.session.delete(user)
        db.session.commit()
        flash("Delete succed")
        return redirect(url_for("get_all_user"))
    return redirect('/login')

@app.route('/user/<int:id>/update', methods=["GET", "POST"])
def user_update(id):
    if g.user and session['role']=="admin":
        user = db.get_or_404(User, id)
        password = user.password           
        email = user.email
        mobile_no = user.mobile_no
        username = user.username
        id = user.id
        if request.method == "POST":
            db.session.delete(user)
            db.session.commit()
            user = User(
                name = request.form['name'],            
                role = request.form['role'],
                city = request.form['city'],
                age = request.form['age'],
                password = password,            
                email = email,
                mobile_no = mobile_no,
                username = username,
            )
            user.id = id
            # user.verified = True
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('get_all_user'))
        else:
            return render_template('update.html', user=user)
    return redirect('/login')
        
@app.before_request
def before_request():
    g.user = None
    g.role = None
    g.id = None
    if 'user' in session:
        g.user = session['user']
        g.role = session['role']
        g.id = session['id']

@app.route('/product', methods=['GET', 'POST'])
def product():
    if g.user and session['role']=='admin':
        if request.method == "GET":
            return render_template('add_product.html')
        else:
            category = request.form['category']
            product_name = request.form['product_name']
            quantity = request.form['quantity']
            price = request.form['price']
            Unit_price = request.form['unit_price']
            description = request.form['description']
            image = request.files['image'].read()
            product = Product(
                category = category,
                product_name = product_name,
                quantity = quantity,
                price = price,
                unit_price = Unit_price,
                description = description,
                image = image
            )
            db.session.add(product)
            db.session.commit()
            return flash("Product")
    else:
        return "Unauthorized Person"
    
@app.route("/product/<int:id>/delete", methods=["GET", "POST"])
def product_delete(id):
    if g.user and session['role']=="admin":
        product = db.get_or_404(Product, id)

        db.session.delete(product)
        db.session.commit()
        flash("Deleted Successfully")
        return redirect(url_for("get_all_user"))
    return redirect('/login')

@app.route('/product/<int:id>/update', methods=["GET", "POST"])
def product_update(id):
    if g.user and session['role']=="admin":
        product = db.get_or_404(Product, id)
        id = product.id
        image = product.image
        description = product.description
        if request.method == "POST":
            db.session.delete(product)
            db.session.commit()
            product = Product(
                product_name = request.form['product_name'],            
                price = request.form['price'],
                quantity = request.form['quantity'],
                unit_price = request.form['unit_price'],
                description = request.form['description'],         
                image = request.files['image'].read(),
                category = request.form['category']
            ) 
            if product.image:
                pass
            else:
                product.image=image
            if product.description:
                pass
            else:
                product.description = description
            product.id = id
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('get_all_user'))
        else:
            return render_template('pupdate.html', product=product)
    return redirect('/login')