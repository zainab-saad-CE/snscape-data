from flask import Flask
import pymongo

# also we can include app.config['key_name']="sqlite:///analysis.db" db=?? 
app = Flask(__name__)
app.config["SECRET_KEY"]='18f4c187bbf89997161ed25f'
app.secret_key = "testing"

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.get_database('total_records')
records = db.register


from analysis import routes


