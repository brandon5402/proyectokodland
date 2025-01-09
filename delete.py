from main import db

db.drop_all()  # Caution: This will delete all data
db.create_all()