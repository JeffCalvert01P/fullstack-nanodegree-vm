from flask import Flask, render_template, url_for, request, redirect,flash, jsonify
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Category, Base, CatalogItem, Users

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()		

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
                open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

@app.route('/<string:category_name>/JSON')
def categoryItemsJSON(category_name):

    category_item = session.query(Category).filter_by(name = category_name).one()
    catalog_items = session.query(CatalogItem).filter_by(id = category_item.id).all()
    
    return jsonify(items=[i.serialize for i in catalog_items])

@app.route('/users/JSON')
def usersJSON():

    users = session.query(Users).all()
    
    return jsonify(items=[i.serialize for i in users])


@app.route('/')
def catalog_landing():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
    login_session['state'] = state
    

    category_items = session.query(Category).all()
    items = session.query(Category, CatalogItem).filter(Category.id == CatalogItem.category_id).all()
        
    item_size = len(items)
    print "catalog landing", state
    return render_template('catalogpublic.html', category_items = category_items, items = items, item_size = item_size, STATE = state)

@app.route('/catalog')
def catalog():

    category_items = session.query(Category).all()
    items = session.query(Category, CatalogItem).filter(Category.id == CatalogItem.category_id).all()
        
    item_size = len(items)

    return render_template('catalog.html', category_items = category_items, items = items, item_size = item_size, category_name = "all")


@app.route('/<string:category_name>')
def displayCategoryItemList(category_name):

    if 'username' not in login_session:
        user_name = ""
    else:
        user_name = login_session['username']
    
    category_items = session.query(Category).all()
    category_selected = session.query(Category).filter_by(name = category_name).first()
    
    category_id = category_selected.id
    items = session.query(Category, CatalogItem).filter(Category.id == CatalogItem.category_id).filter(CatalogItem.category_id == category_id).all()
    
    item_size = session.query(CatalogItem).filter_by(category_id = category_id).count()

    return render_template('catalogcategory.html', category_items = category_items, items = items, item_size = item_size,category_name = category_selected.name, user_name = user_name)

@app.route('/<string:category_name>/<string:item_name>')
def displayCatalogItemDetail(category_name, item_name):

    print "Def DisplayCategoryItenDetail"
    if 'username' not in login_session:
        user_name = ""
    else:
        user_name = login_session['username']

    item = session.query(CatalogItem).filter_by(name = item_name).first()
    return render_template('catalogItem.html', item = item, category_name = category_name, user_name = user_name )

@app.route('/<string:category_name>/<string:item_name>/edit/', methods=['GET','POST'])
def editCatalogItem(category_name, item_name):

    if 'username' not in login_session:
         return redirect('/')

    item_id = request.args.get("item_id")
    item = session.query(CatalogItem).filter_by(id = item_id).one()

    if request.method == 'POST':
    	item.name = request.form['name']
    	item.description = request.form['description']
    	item.price = request.form['price']
    	item.category_id = request.form['category_id']
    	id = item_id
	session.add(item)
	session.commit()
        flash("Catalog Item has been updated")
	return redirect(url_for('catalog'))
    else:
        current_category = session.query(Category).filter_by(id = item.category_id).one()
        category_items = session.query(Category).all()
	return render_template('editcatalogitem.html', item = item, category_items = category_items, current_category = current_category)

@app.route('/<string:category_name>/<string:item_name>/delete/', methods=['GET','POST'])
def deleteCatalogItem(category_name, item_name):

    if 'username' not in login_session:
         return redirect('/')

    item_id = request.args.get("item_id")
    item = session.query(CatalogItem).filter_by(id = item_id).one()

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Catalog Item has been deleted")
        return redirect(url_for('catalog'))
    else:
        category_items = session.query(Category).filter_by(id = item.category_id).one()
	return render_template('deletecatalogitem.html', item = item, category_items = category_items)


@app.route('/new/', methods=['GET','POST'])
def addCatalogItem():

    if 'username' not in login_session:
         return redirect('/')

    if request.method == 'POST':
        item_size = session.query(CatalogItem).filter_by(name = request.form['name']).count()
        print "this is the item size: ", item_size
        if item_size == 0:
            newItem = CatalogItem(name = request.form['name'], description = request.form['description'], price = request.form['price'],
                            category_id = request.form['category_id'], user_id = login_session.get('appuserid'))
            session.add(newItem)
            session.commit()
            flash("New Catalog Item has been added")
            return redirect(url_for('catalog'))
        else:
            print "this is the desc: ", request.form['description']
            flash("Catalog item already exists")
            category_items = session.query(Category).all()
            return render_template('newcatalogitem.html', category_items = category_items, name = request.form['name'], description = request.form['description'],
                            price = request.form['price'], category_id = request.form['category_id'], user_id = login_session.get('appuserid'))
    else:
        category_items = session.query(Category).all()
	return render_template('newcatalogitem.html', category_items = category_items)

@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    print "login session: ", login_session
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    print "code: ", code

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print "gconnect access token: ", access_token
    login_session['access_token'] = access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print "Verify that the access token is valid for this app."
    if result['issued_to'] != CLIENT_ID:
        print "f"
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')


    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    print "here1"
    
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    login_session['access_token'] = access_token

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    email = data['email']

    item = session.query(Users).filter_by(email_addr = email).count()

    if item == 0:
    	newUser = Users(name = data['name'], email_addr = email)
	session.add(newUser)
	session.commit()
    print "here2"
    user_id = session.query(Users).filter_by(email_addr = email).one().id
    login_session['appuserid'] = user_id
    
    print "gconnect: ", login_session

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 50px; height: 50px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 25px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done! ", output

    return output

@app.route('/gdisconnect')
def gdisconnect():
    print "gdisconnect: ", login_session
    credentials = login_session['credentials']
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    if access_token is None:
 	print 'Access Token is None'
 	response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token'] 
	del login_session['credentials'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	# return response
        return redirect(url_for('catalog_landing'))

    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

if __name__ == '__main__':
    app.secret_key = 'VD5uVBSoIIduSPa8RqNv2e4Z'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

