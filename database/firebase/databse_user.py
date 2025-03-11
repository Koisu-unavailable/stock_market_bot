import firebase_admin
from firebase_admin import firestore
from database.firebase.User import User

app = firebase_admin.initialize_app()
db = firestore.client()

def get_user_by_id(userId : int):
    try:
        users = db.collection("users").get()
    except KeyError:
        return None
    for  doc in users:
        if doc.to_dict()["userId"] == userId:
            return User.from_dict(doc.to_dict())

if __name__ == "__main__":
    get_user_by_id("danDadanPeak")
