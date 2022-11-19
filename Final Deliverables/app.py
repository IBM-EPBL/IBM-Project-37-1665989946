from flask import Flask,redirect, render_template, request,session
from flask_session import Session
from connection import connect
from datetime import datetime
from sendgridMail import mailtest_request

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = connect.Connection()

#Index/Signin page
@app.route('/',methods=["GET","POST"])
def index():
    error = ""
    if request.method == "POST":
        email = str(request.form.get("UEmail"))
        password = str(request.form.get("UPassword"))
        flag = connect.Signin(email,password,con)
        if flag[0] == "no user" :
            error = "Email Id or Password Incorrect !"
            return render_template('index.html',error = error)
        elif flag[0] == "database error":
            error = "Error while retrying the data !"
            return render_template('index.html',error = error)
        elif flag[0]=="success":
            user = flag[1]

            # print(str(user["UUSERID"]))

            session["userid"] = str(user["UUSERID"])
            return redirect('./dashboard')
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
        flag = connect.Signup(name,email,phone,password,con)
        if(flag=="success"):
            return redirect("/")
        elif flag == "already present":
            error = "User email Id is already in use! Pls do login."
            return render_template('SignUp.html',error=error)
        else:
            error = "Error occered while SignUp!"
            return render_template('SignUp.html',error=error)
    return render_template('SignUp.html',error=error)

#Dashboard page
@app.route('/dashboard')
def Dashboard():
    connect.getIncome(session["userid"],con)
    connect.getexpense(session["userid"],con)
    if(int(session["expe"])>int(session["Userbudget"])):
        mail = session["userid"]+"@gmail.com"
        # print(mail)
        mailtest_request(mail)
    return render_template('Home.html')

#Add Income page
@app.route('/addincome', methods=["GET","POST"])
def AddIncome():
    error = ""
    if request.method == "POST":
        date = str(request.form.get("date_income"))
        cat = str(request.form.get("category_income"))
        li = cat.split(",")
        catogery =str(li[0])
        note = str(request.form.get("note_income"))
        amount = str(request.form.get("budget_income"))
        userid = str(session["userid"])
        catid = str(li[1])
        incomeid = str(datetime.today().strftime('%Y-%m-%d'))+"-"+str(datetime.today().strftime('%H-%M-%S'))
        
        # print(session["userid"])

        error = connect.Addincome(userid,amount,incomeid,date,note,catogery,catid,con)

        return render_template('AddIncome.html',error = error)

    return render_template('AddIncome.html',error = error)

#Add Expense page
@app.route('/addexpense', methods=["GET","POST"])
def AddExpense():
    error = ""
    if request.method == "POST":
        date = str(request.form.get("date_expense"))
        cat = str(request.form.get("category_expense"))
        li = cat.split(",")
        catogery =str(li[0])
        note = str(request.form.get("note_expense"))
        amount = str(request.form.get("budget_expense"))
        userid = str(session["userid"])
        catid = str(li[1])
        expenseid = str(datetime.today().strftime('%Y-%m-%d'))+"-"+str(datetime.today().strftime('%H-%M-%S'))
        
        # print(session["userid"])

        error = connect.Addexpense(userid,amount,expenseid,date,note,catogery,catid,con)

        return render_template('AddExpense.html',error = error)

    return render_template('AddExpense.html',error=error)

#Expense Analysis page
@app.route('/expenseanalysis')
def ExpenseAnalysis():
    return render_template('Analysis_2.html')

#Income Analysis page
@app.route('/incomeanalysis')
def IncomeAnalysis():
    return render_template('Analysis.html')

#List of Expense Page
@app.route('/expenselist')
def ExpenseList():
    return render_template('Expense_List.html')

#List of Income Page
@app.route('/incomelist')
def IncomeList():
    return render_template('Income_List.html')

@app.route('/showincome')
def showincome():
    error=""
    incomeid = request.args.get('incomeid')
    # print(incomeid)
    redirect('./showincome')
    data = connect.getincomevalues(incomeid,con)
    # print(data)
    return render_template("Show_Income.html",data= data,error=error)

@app.route('/showincome',methods=["POST","GET"])
def updateincome():
    error = ""
    if request.method == "POST":
        date = str(request.form.get("date_income"))
        cat = str(request.form.get("category_income"))
        li = cat.split(",")
        catogery =str(li[0])
        note = str(request.form.get("note_income"))
        amount = str(request.form.get("budget_income"))
        userid = str(session["userid"])
        incomeid = str(request.form.get("incomeid"))
        catid = str(request.form.get("catid"))
        print(date)
        data={"INCOMEDATE":date,"INCOMENOTE":note,"INCOMEAMOUNT":amount,"INCOMECATEGORY":catogery,"INCOMEID":incomeid,"CATOGERYNAME":catid}
        error = connect.updateincome(userid,amount,incomeid,date,note,catogery,catid,con)
        print(error)

    #     return render_template('AddIncome.html',error = error)

    return render_template("Show_Income.html",data=data,error=error)

#Delete income
@app.route('/deleteincome')
def deleteincome():
    error=""
    incomeid = request.args.get('incomeid')
    userid = session["userid"]
    connect.deleteincome(incomeid, userid,con)
    return redirect('./dashboard')

@app.route('/showexpense')
def showexpense():
    error=""
    expenseid = request.args.get('expenseid')
    # print(expenseid)
    redirect('./showexpense')
    data = connect.getexpensevalues(expenseid,con)
    # print(data)
    return render_template("Show_Expense.html",data= data,error=error)

@app.route('/showexpense',methods=["POST","GET"])
def updateexpense():
    error = ""
    if request.method == "POST":
        date = str(request.form.get("date_expense"))
        cat = str(request.form.get("category_expense"))
        li = cat.split(",")
        catogery =str(li[0])
        note = str(request.form.get("note_expense"))
        amount = str(request.form.get("budget_expense"))
        userid = str(session["userid"])
        expenseid = str(request.form.get("expenseid"))
        catid = str(request.form.get("catid"))
        print(date)
        data={"EXPENSEDATE":date,"EXPENSENOTE":note,"EXPENSEAMOUNT":amount,"EXPENSECATEGORY":catogery,"EXPENSEID":expenseid,"CATOGERYNAME":catid}
        error = connect.updateexpense(userid,amount,expenseid,date,note,catogery,catid,con)
        print(error)

    #     return render_template('AddExpense.html',error = error)

    return render_template("Show_Expense.html",data=data,error=error)

#Delete expense
@app.route('/deleteexpense')
def deleteexpense():
    error=""
    expenseid = request.args.get('expenseid')
    userid = session["userid"]
    connect.deleteexpense(expenseid, userid,con)
    return redirect('./dashboard')

#Profile page
@app.route('/profile', methods=["POST","GET"])
def Profile():
    error = ""
    userid = session["userid"]
    if(request.method == "POST"):
        name = request.form.get("name_user")
        email = request.form.get("email_user")
        phone = request.form.get("tel_user")
        password = session['userpassword']
        budget = request.form.get("budget_user")
        print(userid,name,email,phone,password,budget,con)
        error = connect.profile(userid,name,email,phone,password,budget,con)
    if(request.args.get("pass_user")):
        name = session['username']
        email = session['useremail']
        phone = session['userphone']
        password = request.args.get("pass_user","")
        budget = session['Userbudget']
        error = connect.profile(userid,name,email,phone,password,budget,con)
    return render_template('Profile.html',error=error)

#Profile page
@app.route('/logout')
def logout():
    session.clear()
    print("Session Cleared!")
    return redirect('/')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug = True)