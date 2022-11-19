from flask import Flask,redirect, render_template, request
 
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')

@app.route('/',methods=["GET","POST"])
def index():
    error = ""
    if request.method == "POST":
        email = str(request.form.get("UEmail"))
        password = str(request.form.get("UPassword"))
        # flag = connect.Signin(email,password)
        # if(flag!=""):
        #     user_id = flag
        #     return redirect('/dashboard')
        # else:
        #     error = "Email or Password is incorrect !"

    return render_template('index.html',error = error)

#SignUp page
@app.route('/signup',methods=["GET","POST"])
def Signup():
    error = ""
    if request.method == "POST":
        email = str(request.form.get("UEmail"))
        name = str(request.form.get("UName"))
        phone = str(request.form.get("UPhone"))
        password = str(request.form.get("UPassword"))
        # flag = connect.Signup(name,email,phone,password)
        # if(flag=="success"):
        #     return redirect("/signin")
        # elif flag == "already present":
        #     error = "User email Id is already Present! Pls do login."
        # else:
        #     error = "Error occered while SignUp!"
    return render_template('SignUp.html',error=error)

if __name__=='__main__':
    app.run(debug = True)