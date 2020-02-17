# we import the instance of the database that we will be populating
from app import db
# we also import the tables of the database
from app.models import User

def populate_db():
    # 5. Create people objects then add to the database using the session object
    if not User.query.first():
        db.session.add_all([
            User(username='weatherman', email='jo@bloggs.com', first_name='kowther', last_name='hanan', role='0'),
            User(username='itrains', email='itrains@alot.co.uk',first_name='aure', last_name='enkaoua', role='1')
        ])

        # 6. Commit the changes to the database
        db.session.commit()

