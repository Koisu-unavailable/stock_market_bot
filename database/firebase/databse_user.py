import firebase_admin
from firebase_admin import firestore

from database.firebase.User import User

app = firebase_admin.initialize_app()
db = firestore.client()


def get_user_by_id(userId: int):
    users = db.collection("users").get()
    for doc in users:
        if doc.to_dict()["userId"] == userId:
            return User.from_dict(doc.to_dict())
        return None


def add_or_update_user(user: User):
    user_doc = db.collection("users").document(str(user.userId))
    user_doc.set(user.to_dict())


if __name__ == "__main__":
    get_user_by_id("danDadanPeak")
