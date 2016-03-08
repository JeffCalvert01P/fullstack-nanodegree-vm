# Catalog Application

## Application Description
The Catalog Application can be useed to create a store catalog based on pre-defined 
categories configured in a database.  The application allows for catalog items to be 
added, modified and deleted and also allows images to be attached to the categories. 
Login to the application requires a google account.  Users are only able to add, modify 
and delete the records they added to the database.

## Installation Instructions
1) Retrieve files from gihub.
2) Run catalog_database_setup.py to create the database.  
2) Run catalog_load.py to load the database
3) Create images directory under catalog
4) Run the application by running application.py

## Features
### Base features
1) Allows browse or login access
2) After logging-in users can add, update or delete records
3) Users can only update or delete records they created

### Features beyond basic specs
1) Avoid duplicate records
2) Required fields must be entered
3) Allow adding, deleting, and updating images
