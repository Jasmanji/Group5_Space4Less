# This script is where everything starts.
# It has the simple function of running the application.

# we start by importing the create_app fuction found in the __init__ module in the folder app.
from app import create_app

# first we run the method create_app from the __init__ module in the app package folder.
# That returns the instance of an app and we save it all under the variable 'app'.
app = create_app()


