from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pymongo, os

app = Flask(__name__)

# Establish connection with database
client = pymongo.MongoClient(open("config.txt").read())
db = client['toddler-time-registration']
entries = db.get_collection('entries')

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generateNewEntry(data):
    new_entry = dict()
    new_entry["date"] = datetime.today().strftime('%b-%d-%Y')
    for item in list(data.lists()):
        if item[0] == 'phone' and item[1]:
            print(standardize(item[1][0]))
        entry = ""
        for sub_item in item[1]:
            if(sub_item != ''):
                entry = entry + str(sub_item) + ";"
            new_entry[item[0]] = entry[:-1]
    return new_entry
    
def getChildNames(entry):
    res=[]
    for key in entry:
        if "child-name" in key:
            res.append(entry.get(key))
    return res

def standardize(num):
    return num.replace("(", "").replace(")","").replace("-","").replace(" ","")
    
@app.route("/")
def index():
    return render_template("register.html")

@app.route("/confirm-registration", methods=["GET", "POST"])
def confirmRegistration():
    if request.method=="POST":
        id = entries.insert_one(generateNewEntry(request.form))
        if(id):
            return render_template("confirmation.html", entry=getChildNames(entries.find_one(id.inserted_id)))
        else:
            return redirect("/")
    else:
        return redirect("/")

@app.route("/confirm-checkin", methods=["GET","POST"])
def confirmCheckin():
    if request.method == "POST":
        id = entries.insert_one(generateNewEntry(request.form))
        if(id):
            return render_template("confirmation.html", entry=getChildNames(entries.find_one(id.inserted_id)))
        else:
            return redirect("/")
    else:
        return redirect("/checkin")

@app.route("/checkin")
def checkin():
    return render_template("checkin.html")

@app.route("/check_existing", methods=["GET","POST"])
def check_existing():
    if request.method == "POST":
        if entries.find_one({"phone": standardize(request.form["phone"])}):
            return render_template("review.html", entry=entries.find_one({"phone": standardize(request.form["phone"])}))
        else:
            return redirect("/")
    else:
        return redirect("/checkin")
                
                
                
                
if __name__ == "__main__":
    app.run()
