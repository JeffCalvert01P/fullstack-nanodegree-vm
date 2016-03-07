from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from catalog_database_setup import Category, Base, CatalogItem, Users
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Category Load
category1 = Category(name = "Basketball")

session.add(category1)

category2 = Category(name = "Football")

session.add(category2)

category3 = Category(name = "Softball")

session.add(category3)

category4 = Category(name = "Skiing")

session.add(category4)

session.commit()

print "added categories items!"

users1 = Users(name = "Jeff Calvert", email_addr = "JeffCalvert01@gmail.com")

session.add(users1)
session.commit()

print "added users!"

items1 = CatalogItem(name = "Shoes", description = "Really nice basketball shoes", price = "$1000", category = category1, user = users1, filetype = "none")

session.add(items1)

items2 = CatalogItem(name = "Shorts", description = "Really nice basketball shorts", price = "$75", category = category1, user = users1, filetype = "none")

session.add(items2)

items3 = CatalogItem(name = "Jersey", description = "Really nice basketball jersey", price = "$50", category = category1, user = users1, filetype = "none")

session.add(items3)

items4 = CatalogItem(name = "Basketball Shoes", description = "Really nice basketbll shoes", price = "$1000", category = category1, user = users1, filetype = "none")

session.add(items4)

items5 = CatalogItem(name = "Shoes", description = "Really nice football shoes", price = "$500", category = category2, user = users1, filetype = "none")

session.add(items5)

items6 = CatalogItem(name = "Helmet", description = "Football helmet", price = "$99", category = category2, user = users1, filetype = "none")

session.add(items6)

items7 = CatalogItem(name = "Helmet", description = "Softball helmet", price = "$99", category = category3, user = users1, filetype = "none")

session.add(items7)

items8 = CatalogItem(name = "Shoes", description = "Softball Shoes", price = "$99", category = category3, user = users1, filetype = "none")

session.add(items8)

items9 = CatalogItem(name = "Bat", description = "Softball Bat", price = "$35", category = category3, user = users1, filetype = "none")

session.add(items9)

items10 = CatalogItem(name = "Skis", description = "Skis", price = "$2000", category = category4, user = users1, filetype = "none")

session.add(items10)

session.commit()

print "added Items!"
