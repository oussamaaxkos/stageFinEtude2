from flask import Flask , redirect , url_for ,  render_template , request , jsonify , session , redirect

import os
from werkzeug.utils import secure_filename
import mysql.connector
from datetime import datetime
from datetime import datetime, timedelta

# to search about a directory
# def find_file(filename):
#     for root, dirs, files in os.walk('/'):
#         if filename in files:
#             return os.path.join(root, filename)
#     return None





app = Flask(__name__)
app.secret_key = 'my_secret_key'
# where we save the images 
UPLOAD_FOLDER = 'static/profiles'
# respect those extenstion 
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Connect to the MySQL database
def connexion():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ajaxdb"
    )
    return conn

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/' )
def hello_world():
    if request.args.get('logout'):
        logout = request.args.get('logout')
        if logout == "True" :
            session.pop('profile', None)
            session.pop('name', None)
            session.pop('userId', None) 
            session.pop('email', None)

    conn = connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tpservice");
    rows = cursor.fetchall()
    return render_template("Home.html" , data = rows)
    


@app.route("/addService" , methods=["POST"])
def addService():
    
    idtpservice = request.form.get('idtpservice')
    now = datetime.now()
    
    delta = timedelta(days=8)

    later = now + delta


    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO command (datedebut, daterv, iduser, idtpservice)
                            VALUES (%s, %s, %s, %s)''', (now, later, session["userId"], idtpservice))
    conn.commit()
    return jsonify({'message': 'True'})

            
    

@app.route("/registerLogin")
def registerLogin():
    return render_template("registerLogin.html")

@app.route("/register" , methods=['POST'])
def register():
    # Get the form data
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    image = request.files.get('image')
    filename = 'noprofile.png'  # Set the default filename
    if image is not None:
        filename = secure_filename(image.filename)

    if ( not username or not email or not phone or not password ) :
        return  jsonify({'error': 'Please fill out all fields.'}), 400
    else:
        conn = connexion()
        cursor = conn.cursor()
        # Execute the SELECT statement to fetch all the rows from the users table
        cursor.execute("SELECT * FROM users")
        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()
        # Close the cursor and database connection
        sameUser = 0
        for user in rows :
            if user[2] == email :
                sameUser+=1
                return  jsonify({'error': 'Already we have that email.'}), 400
        samePhone = 0;
        for user in rows :
            if user[4] == phone :
                samePhonex+=1
                return  jsonify({'error': 'Already we have that number Phone.'}), 400
        
        
        if sameUser == 0 and samePhone == 0 :
            if image :
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
            conn = connexion()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (username, email, phone, profile, password)
                            VALUES (%s, %s, %s, %s, %s)''', (username, email, phone, filename, password))
            conn.commit()
            return jsonify({'message': 'User registered successfully'})
        cursor.close()
        conn.close()
        
        
@app.route("/login" , methods =["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = connexion()
    cursor = conn.cursor()
    # Execute the SELECT statement to fetch all the rows from the users table
    cursor.execute("SELECT * FROM users")
    # Fetch all the rows as a list of tuples
    rows = cursor.fetchall()
    correct = 0
    for user in rows :
        if user[2] == email and user[5] == password :
            print("you are here : ",user[2] )
            session["profile"] = user[4]
            session["name"] = user[1]
            session["userId"] = user[0]
            session["email"] = user[2]
            session["phone"] = user[3]
            session['password'] = user[5]
            correct+=1
            return jsonify({'message': 'User login successfully' , 'id' : user[0] , 'username' : user[1] , 'profile' : user[4]})
    if correct == 0 :
        return jsonify({'error': 'Yout information are not correct!'}), 400
    else :
        return jsonify({'error': 'Yout information are not correct!'}), 400
  
@app.route("/updateAccount", methods = ["POST"])
def updateAccount():
    conn = connexion()
    cursor = conn.cursor()
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    phone = request.form.get('phone')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print("your email is :"+email)
    for user in rows :
        if user[2] == email and user[2] != session["email"] :
            return jsonify({'error': 'Email already exist!' , 'phone' : "False"}), 400
        if user[3] == phone  :
            return jsonify({'error': 'phone already exist!' , 'phone' :  "True"}), 400

    session["name"] = username
    session["email"] = email
    session["phone"] = phone
    session['password'] = password
    session["name"] = username
    cursor2 = conn.cursor()
    cursor2.execute("UPDATE users SET username = %s ,  email = %s ,  phone = %s ,   password = %s where id = %s" , ( username , email , phone , password , session["userId"]  ) )
    conn.commit()
    conn.close()
    print(session["userId"])
    return jsonify({'message':'success'})
   
# Define a route to display the user data
@app.route('/users')
def show_users():
    conn = connexion()
    cursor = conn.cursor()

    # Execute the SELECT statement to fetch all the rows from the users table
    cursor.execute("SELECT * FROM users")

    # Fetch all the rows as a list of tuples
    rows = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Render the HTML template with the rows data
    return rows


@app.route("/myservices")
def myservices():

    conn = connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT c.id , c.datedebut , c.daterv ,  tps.title , u.profile ,  c.status FROM command c ,  users u , tpservice tps where c.iduser = u.id and c.idtpservice = tps.id and u.id = %s " , (session['userId'],));
    rows = cursor.fetchall()
    print(rows)

    return render_template("myservices.html" , rows = rows)


@app.route("/deleteCmnd" , methods=["POST" , "GET"])
def deleteCmnd():
    
    idDelete = request.form.get('idDelete')
    print(idDelete)
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM command where id = %s " , (idDelete,))
    conn.commit()
    return jsonify({'message': 'True'})
    
    
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html" )

@app.route("/sendMessage" , methods=["POST" , "GET"])
def sendMessage():
    
    email = request.form["email"]
    message = request.form["message"]
    username = request.form["username"]
    print(email,message)
    conn = connexion()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO messages (email , message , username)
                            VALUES (%s, %s, %s)''', (email , message , username))
    conn.commit()
    return redirect(url_for("contact"))

if __name__ == '__main__':
    app.run(debug=True)
