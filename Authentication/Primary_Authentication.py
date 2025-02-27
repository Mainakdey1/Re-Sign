import bcrypt
import pyrebase
import firebase_admin
from firebase_admin import credentials, db


#important note: Please use pip install pyrebase4 or whatever the lates version of pyrebase is. There is module and package naming discrepancy for pyrebase.

# Firebase configuration
firebase_config = {
    'apiKey': "AIzaSyC7EXl7sMRE1rrwRted_kYKybecl0IQajk",
  'authDomain': "ssenc-96031.firebaseapp.com",
  'databaseURL': "https://ssenc-96031-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "ssenc-96031",
  'storageBucket': "ssenc-96031.firebasestorage.app",
  'messagingSenderId': "371333696694",
  'appId': "1:371333696694:web:37043b8b1212e36796ea17",
  'measurementId': "G-NGPL08S15H"

}


# Initialize Firebase app
cred = credentials.Certificate(r"C:\Users\chestor\Desktop\Project_tempfiles\Units\ssenc_json.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ssenc-96031-default-rtdb.asia-southeast1.firebasedatabase.app"
})

def change_password_in_database(username, new_password):
    ref = db.reference("users")  # Reference the "users" node in the database
    user_ref = ref.child(username)  # Locate the specific user

    if user_ref.get():
        user_ref.update({"password": new_password})
        print("Password updated successfully in the database!")
    else:
        print("User not found.")


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

newpassword='catcatcat'
hashed_new_pw= hash_password(newpassword)
# Example usage
change_password_in_database('bobcat', hashed_new_pw.decode('utf-8'))

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()


def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def sign_up(username, password):
    users = db.child("users").get().val()
    if users and username in users:
        print("Username already exists.")
        return
    
    hashed_password = hash_password(password)
    db.child("users").child(username).set({"password": hashed_password.decode('utf-8')})
    print("User registered successfully!")

def login(username, password):
    user = db.child("users").child(username).get().val()
    if not user:
        print("User not found.")
        return
    
    stored_password = user["password"].encode('utf-8')
    if verify_password(stored_password, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")

def main():
    print("Welcome to the Authenticator!")
    while True:
        print("\nOptions:")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            sign_up(username, password)
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login(username, password)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
