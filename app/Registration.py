class Register:
    def _init_(self, first_name, surname, username, unique_email, password, date_of_birth):
        self.username = username
        self.first_name = first_name
        self.surname = surname
        self.password = password
        self.unique_email = unique_email
        self.date_of_birth = date_of_birth
    first_name = input("First Name: ")
    surname = input("Surname: ")
    username = input("Pick a Username: ")
    unique_email = input("Enter Email Address : ")
    password = input("Enter unique password: ")
    date_of_birth = int(input("Enter Date of Birth: "))
    user = first_name, surname, username, unique_email, password, date_of_birth
#save function to create the user object
    def __init__(self):
        if len(Register.username) > 20:
            print("This username is too long")
        else:
            return Register.username
