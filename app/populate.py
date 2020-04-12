# # we import the instance of the database that we will be populating
from app import db
# # we also import the tables of the database
from app.models import User


def populate_db():
    # 5. Create people objects then add to the database using the session object
    if not User.query.first():
        user1 = User(username='user1',
                     first_name='aure',
                     last_name='enkaoua',
                     email='property@gmail.com',
                     roles='property_owner')
        user1.set_password('1234')
        # adding the role of the user- property_owner or renter

        db.session.add(user1)

        user2 = User(username='user2',
                     first_name='kowther',
                     last_name='hanan',
                     email='renter@gmail.com',
                     roles='renter')
        user2.set_password('1234')

        db.session.add(user2)

        db.session.commit()

    # 6. Commit the changes to the database
