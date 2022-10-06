from analysis import app
from flask import render_template, request, request, session, jsonify,redirect
from . import records
import bcrypt
import datetime
from .functionquery import verified_unverified_user, case_search_year, top_tweet_count, topinfluncer_hashtags, location_of_tweet, location_of_influncer, user_age_count, top_influncer_shared, top_hashtags_of_tweet, all_hashtags, sentiment_anlysis, topinfluncer_url, total_number_of_user, verifieduser,user_data,url_created
from CrimeAnalysis.function import clean_tweet

@app.route('/tweet')
def text():
  if ('email' in session):   
    toptweet=top_tweet_count("mongodb://localhost:27017", "twitter_db", "twitter_collection")
    output=[]
    for val in toptweet:
     text=clean_tweet(val["text"])
     output.append([val["name"],text])
    return render_template("textdisplay.html",fullname=session["name"],tweet=output,len2=len(output))
  return redirect('/')


@app.route('/maps')
def maps():
  if ('email' in session):   
    return render_template("maps.html",fullname=session["name"])
  return redirect('/')

@app.route('/charts')
def charts():
  if ('email' in session):   
    created= datetime.date.today()
    date=int(created.strftime("%Y"))
    return render_template("charts.html",fullname=session["name"],createdaccount=date)
  return redirect('/')


@app.route('/sourcelable')
def sourcelable():
  if ('email' in session):   
    return jsonify(url_created("mongodb://localhost:27017", "twitter_db", "twitter_collection"))
  return redirect('/')


@app.route('/urltopinfluncer')
def topinfluncerurl():
 if ('email' in session):   
    return jsonify(topinfluncer_url())
 return redirect('/')


@app.route('/sentiment')
def sentiment():
 if ('email' in session):   
    return jsonify(sentiment_anlysis("mongodb://localhost:27017", "twitter_db", "sentiment"))
 return redirect('/')







@app.route('/CaseSearch')
def case_search():
  if ('email' in session):   
    return jsonify(case_search_year("mongodb://localhost:27017", "twitter_db", "twitter_collection"))
  return redirect('/')


@app.route('/toptweet')
def top_tweet():
 if ('email' in session):   
    return jsonify(top_tweet_count("mongodb://localhost:27017", "twitter_db", "twitter_collection"))
 return redirect('/')




@app.route('/topinfluncerhashtags')
def top_influncer_hashtags():
 if ('email' in session):   
    return jsonify(topinfluncer_hashtags())
 return redirect('/')



@app.route('/location')
def location():
 if ('email' in session):   
    return jsonify(location_of_tweet("mongodb://localhost:27017", "twitter_db", "location"))
 return redirect('/')


@app.route('/influncerlocation')
def ifluncerlocation():
  if ('email' in session):   
    return jsonify(location_of_influncer("mongodb://localhost:27017", "twitter_db", "locationofinfluncer"))
  return redirect('/')


@app.route('/topinfluncer')
def top_influncer():
  if ('email' in session):   
    return jsonify(top_influncer_shared())
  return redirect('/')


@app.route('/tophashtags')
def top_hashtags():
   if ('email' in session):    
    return jsonify(top_hashtags_of_tweet())
   return redirect('/') 


@app.route('/hashtagsframework')
def hashtag_framework():
  if ('email' in session):   
    return jsonify(all_hashtags("mongodb://localhost:27017", "twitter_db", "twitter_collection"))
  return redirect('/')


@app.route('/UserAgePercentage')
def User_Age():
   if ('email' in session):    
    return jsonify(user_age_count("mongodb://localhost:27017", "twitter_db", "twitter_collection"))
   return redirect('/') 

@app.route('/dashboard')
def dashboard():
  message=''  
    # check session email
  if ('email' in session):  
      total = total_number_of_user(
        "mongodb://localhost:27017", "twitter_db", "twitter_collection")
      verified = verifieduser("mongodb://localhost:27017",
                            "twitter_db", "twitter_collection")
      percentageofVerified = round(verified*100/total, 0)
      sent=sentiment_anlysis("mongodb://localhost:27017", "twitter_db", "sentiment")
      topinflu=user_data()
    
      output=[]
      for val in sent:
        output.append([val["name"],round(val["percentage"],0)])
        
      return render_template('dashboard.html', totalnumber=total, percentage=percentageofVerified, fullname=session["name"],topinfluncer=topinflu,len=len(topinflu),sentiment=output,len1=len(output))
  
  return redirect('/')
      
      
         
  
  



@app.route('/display')
def display():
    # check session email
    return render_template('display.html', fullname=session["name"])





@app.route('/verification')
def verification():
    return jsonify(verified_unverified_user("mongodb://localhost:27017", "twitter_db", "twitter_collection"))





@app.route("/register", methods=['post', 'get'])
def register():
    message = ''
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            return render_template('register.html', email=new_email)
    return render_template('register.html')


@app.route("/", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            username = email_found["name"]

            if bcrypt.checkpw(password1.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                session["name"] = username
              
                return redirect('/dashboard')
            else:
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        session.pop("name", None)
        return redirect("/")
    else:
        return redirect("/register")
