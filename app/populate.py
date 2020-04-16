# Contributors:

# # we import the instance of the database that we will be populating
from app import db
# # we also import the tables of the database
from app.models import User, Post


def populate_db():
    # 5. Create people objects then add to the database using the session object
    if not User.query.first():
        user1 = User(username='Bob',
                     first_name='PO1',
                     last_name='enkaoua',
                     email='property@gmail.com',
                     roles='property_owner')
        user1.set_password('1234')
        # adding the user to db
        db.session.add(user1)

        user2 = User(username='Jake',
                     first_name='PO2',
                     last_name='two',
                     email='property2@gmail.com',
                     roles='property_owner')
        user2.set_password('1234')
        db.session.add(user2)

        user3 = User(username='Miriam',
                     first_name='PO3',
                     last_name='three',
                     email='property3@gmail.com',
                     roles='property_owner')
        user3.set_password('1234')
        db.session.add(user3)

        user4 = User(username='Djudith',
                     first_name='PO4',
                     last_name='four',
                     email='property3@gmail.com',
                     roles='property_owner')
        user4.set_password('1234')
        db.session.add(user4)

        user5 = User(username='Cameron',
                     first_name='PO5',
                     last_name='five',
                     email='property5@gmail.com',
                     roles='property_owner')
        user5.set_password('1234')
        db.session.add(user5)

        user6 = User(username='Hailey',
                     first_name='PO6',
                     last_name='six',
                     email='renter6@gmail.com',
                     roles='property_owner')
        user6.set_password('1234')
        db.session.add(user6)

        user7 = User(username='Greg',
                     first_name='RE1',
                     last_name='one',
                     email='renter@gmail.com',
                     roles='renter')
        user7.set_password('1234')
        db.session.add(user7)

        user8 = User(username='Daniel',
                     first_name='RE2',
                     last_name='two',
                     email='renter2@gmail.com',
                     roles='renter')
        user8.set_password('1234')
        db.session.add(user8)

        user9 = User(username='Sarah',
                     first_name='RE3',
                     last_name='three',
                     email='renter3@gmail.com',
                     roles='renter')
        user9.set_password('1234')
        db.session.add(user9)

        db.session.commit()
        # 6. Commit the changes to the database

    if not Post.query.first():
        post1 = Post(
            title='Large space near kings cross station',
            image='post1-image.jpg',
            location='N1C4AX',
            space_size='XL',
            content='I have a car so can help carry things from the station. Very good price of 4£ a ',
            user_id=1
        )
        db.session.add(post1)
        db.session.commit()

        post2 = Post(
            title='Space in central London',
            image='post2-image.jpg',
            location='NW102LP',
            space_size='M',
            content='Live in a flat but there is a working lift, would prefer everything boxed up but its not a requirement.',
            user_id=2
        )
        db.session.add(post2)
        db.session.commit()

        post3 = Post(
            title='Small space for emergency storage',
            image='post3-image.jpg',
            location='UB3 4AZ',
            space_size='S',
            content='Its just a small closet under the stairs able to store a couple boxes of stuff',
            user_id=3
        )
        db.session.add(post3)
        db.session.commit()

        post4 = Post(
            title='Space in my shed for large belongings',
            image='post4-image.jpg',
            location='N3 3HP',
            space_size='XL',
            content='Have space to store things like bikes or even furniture',
            user_id=4
        )
        db.session.add(post4)
        db.session.commit()

        post5 = Post(
            title='Basement storage available',
            image='post5-image.jpg',
            location='NW10 5AH',
            space_size='M',
            content='Can’t take large objects but good space for boxes full of things like books and kitchen equipment',
            user_id=5
        )
        db.session.add(post5)
        db.session.commit()

        post6 = Post(
            title='Space in my clothes closets and drawers',
            image='post6-image.jpg',
            location='SW5 0TU',
            space_size='S',
            content='Just got rid of lots of clothes so able to store loads of clothes in neat way for a while',
            user_id=6
        )
        db.session.add(post6)
        db.session.commit()

        post7 = Post(
            title='Whole spare room just for storage',
            image='post7-image.jpg',
            location='N6 4RU',
            space_size='ML',
            content='Roommate just moved out and cant find a new one for next 5 months so using the room for storage instead. Have boxes too but cant take large individual items',
            user_id=1
        )
        db.session.add(post7)
        db.session.commit()

        post8 = Post(
            title='Space for kitchen equipment in kitchen cupboards',
            image='post8-image.jpg',
            location='EC4A 2BB',
            space_size='S',
            content='Space for boxes with delicate items like nice plates or cutlery',
            user_id=2
        )
        db.session.add(post8)
        db.session.commit()

        post9 = Post(
            title='Space in garage',
            image='post9-image.jpg',
            location='NW5 1TN',
            space_size='L',
            content=' Loads of space for boxes of clothes, books, anything really',
            user_id=3
        )
        db.session.add(post9)
        db.session.commit()

        post10 = Post(
            title='Space for furniture',
            image='post10-image.jpg',
            location='SE6 3BT',
            space_size='XL',
            content='Big space in basement for things like chairs, tables, lighting, etc...',
            user_id=3
        )
        db.session.add(post10)
        db.session.commit()

        post11 = Post(
            title='some space in my garage',
            image='post11-image.jpg',
            location='NW110JS',
            space_size='M',
            content='I have some space for a few boxes in my garage. Would appreciate if they are fully sealed in boxes',
            user_id=1
        )
        db.session.add(post11)
        db.session.commit()

