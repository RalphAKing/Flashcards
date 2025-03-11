from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory, url_for
from pymongo import MongoClient
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta
from bson import ObjectId
from bleach import clean
from werkzeug.security import check_password_hash
import os
from flask import send_file
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
UPLOAD_FOLDER = 'storage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Database configuration
with open('config.yaml') as f:
    config = yaml.load(f, Loader=SafeLoader)

# Database collections
def accounts():
    cluster = MongoClient(config["mongodbaddress"], connect=False)
    return cluster["RKingIndustries"]["accounts"]

def unverified_accounts():
    cluster = MongoClient(config["mongodbaddress"], connect=False)
    return cluster["RKingIndustries"]["unverified_accounts"]

def boards():
    cluster = MongoClient(config["mongodbaddress"], connect=False)
    return cluster["RKingIndustries"]["boards"]

# Routes
@app.route('/login', methods=["GET", "POST"])
def login():
    if 'userid' in session:
        logged_accounts=accounts()
        account = logged_accounts.find_one({'userid':session['userid']})
        if account != None:
            return redirect('/')
        else:
            session.pop('userid', None)
    if request.method == 'POST':
        logged_accounts=accounts()
        email = (request.form['email']).lower()
        password = request.form['password']

        account = logged_accounts.find_one({'email':email})
        if account != None:
            if check_password_hash(account['password'], password):
                session['userid'] = account['userid']
                try:
                    try:
                        account['score']
                    except:
                        account['score'] = 0
                        logged_accounts.replace_one({'userid':session['userid']}, account)
                    data=boards()
                    found = data.find_one({'owner':account['userid']})
                    if found == None:
                        name=f"{account['username']}'s Board"
                        number=0
                        while data.find_one({"name":name}) != None:
                            number+=1
                            name=f"{account['username']}'s Board {number}"
                        data.insert_one({"name": name, "description":f"{account['username']}'s Board", "owner":account['userid'], "members":[]})                          
                except:
                    print('failed')
                return redirect('/')
            else:
                return render_template('login.html', error='Invalid Password')
        else:
            unaccounts = unverified_accounts()
            if unaccounts.find_one({'email':email}):
                return redirect('/verify')
            return render_template('login.html', error='Invalid Email')

    return render_template('login.html')





@app.route('/flashcards')
def portfolio():
    return render_template('flashcards.html')


@app.route('/deck/create', methods=['POST'])
def create_deck():
    if 'userid' not in session:
        return redirect('/login')
        
    deck_name = clean(request.form['deck_name'])
    file_name = f"{session['userid']}-{deck_name}.csv"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    if request.files['file']:
        csv_file = request.files['file']
        csv_file.save(file_path)
    else:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['question', 'answer'])
    
    return redirect('/decks')

@app.route('/deck/download/<deck_name>')
def download_deck(deck_name):
    if 'userid' not in session:
        return redirect('/login')
        
    file_name = f"{session['userid']}-{deck_name}.csv"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    return send_file(
        file_path,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"{deck_name}.csv"
    )

@app.route('/decks')
def list_decks():
    if 'userid' not in session:
        return redirect('/login')
        
    user_decks = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if file.startswith(session['userid']):
            deck_name = file.replace(f"{session['userid']}-", "").replace(".csv", "")
            user_decks.append(deck_name)
            
    return render_template('decks.html', decks=user_decks)

@app.route('/deck/edit/<deck_name>', methods=['GET', 'POST'])
def edit_deck(deck_name):
    if 'userid' not in session:
        return redirect('/login')
        
    file_name = f"{session['userid']}-{deck_name}.csv"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    if request.method == 'POST':
        questions = request.form.getlist('question')
        answers = request.form.getlist('answer')
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['question', 'answer'])
            for q, a in zip(questions, answers):
                writer.writerow([clean(q), clean(a)])
        return redirect('/decks')
        
    cards = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            cards = list(reader)
            
    return render_template('edit_deck.html', deck_name=deck_name, cards=cards)

@app.route('/study/<deck_name>')
def study_deck(deck_name):
    if 'userid' not in session:
        return redirect('/login')
        
    file_name = f"{session['userid']}-{deck_name}.csv"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    cards = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        cards = list(reader)
    
    if not cards:
        return redirect(url_for('edit_deck', deck_name=deck_name))
        
    return render_template('study.html', deck_name=deck_name, flashcards=cards)

@app.route('/deck/delete/<deck_name>')
def delete_deck(deck_name):
    if 'userid' not in session:
        return redirect('/login')
        
    file_name = f"{session['userid']}-{deck_name}.csv"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return redirect('/decks')



@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/') 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)