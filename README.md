# DrinksCatalog
DrinksCatalog is a web application built with Flask and MongoDB that allows users to manage a catalog of drinks. It provides a simple and intuitive interface to add, view, edit, and delete drinks from the catalog. This README file contains all the necessary information on how to install and use the application.

## Getting started
Before running the application, you will need to make sure that you have Python 3.x installed on your computer, along with the Flask and pymongo packages. You will also need to have MongoDB installed and running on your computer.

To install Flask and pymongo, open a terminal or command prompt and run:
``python pip install Flask pymongo``

To install MongoDB, follow the instructions on the MongoDB website.

## Setting up the database
The application requires a MongoDB database to store the drink data. Before running the application, you will need to create a database and a collection for the drinks. You can do this using the MongoDB shell or a MongoDB GUI such as MongoDB Compass.

Once you have created the database and collection, you will need to update the config.py file with the database connection information. The default settings assume that the database is running on the local machine on port 27017 with no authentication. If your database is running on a different machine or with authentication, you will need to update the settings accordingly.

## Running the application
To run the application, open a terminal or command prompt and navigate to the directory containing the application files. Then run the following command:

``python app.py``

This will start the Flask development server and make the application available at http://localhost:5000.

## Using the application
- The application provides a simple and intuitive interface to manage a catalog of drinks. When you first open the application, you will see a list of all the drinks in the catalog. You can click on a drink to view its details, or click on the "Add Drink" button to add a new drink.

- To add a new drink, click on the "Add Drink" button and fill out the form with the details of the new drink. The form requires a name, a description, a price, and an optional image URL. Once you have filled out the form, click the "Add Drink" button to add the drink to the catalog.

- To edit an existing drink, click on the drink you want to edit and then click the "Edit" button. This will bring up a form with the current details of the drink. You can edit any of the fields and then click the "Save Changes" button to update the drink in the catalog.

- To delete a drink, click on the drink you want to delete and then click the "Delete" button. This will remove the drink from the catalog.

## Authentication and authorization
The application provides basic authentication and authorization to restrict access to certain features. By default, the application comes with a single user account with administrator privileges. You can log in with this account by clicking on the "Log In" button in the top right corner of the application.

To create additional user accounts, you can use the create_user.py script. This script will prompt you for a username and password, and then create a new user account with standard privileges. To create an administrator account, use the create_admin.py script instead.

To restrict access to certain features, the application uses Flask-Login to check the user's authentication status and Flask-Principal to check the user's authorization status. Only authenticated users can add, edit, or delete drinks, and only administrators can edit or delete drinks.



