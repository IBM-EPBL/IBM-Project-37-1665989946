import ibm_db
from flask import session

def Connection():
    try:
        conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vtb79713;PWD=fdcQZgusRLFiLTgU", "", "")
        print ("Database Connected Successfully !")
        return conn
    except:
        print ("Unable to connect: ", ibm_db.conn_errormsg())

def getincomevalues(id,conn):
    sql = "SELECT * FROM vtb79713.INCOME WHERE INCOMEID = '"+id+"'"
    lis={}
    try:
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        # print(dictionary)
        while dictionary!=False:
            lis=dictionary
            dictionary = False
        print("income value got sucessfully !")
    except:
        print("Error while get the income value")
    return lis

def getexpensevalues(id,conn):
    sql = "SELECT * FROM VTB79713.EXPENSE WHERE EXPENSEID = '"+id+"'"
    lis={}
    try:
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary!=False:
            lis=dictionary
            dictionary = False
        print("expense value got sucessfully !")
    except:
        print("Error while get the expense value")
    return lis

def inco(dict):
    incomedate = []
    incomemonth = []
    incomevalues = []
    incomedatemth=[]
    for i in dict:
        incomevalues.append(i["INCOMEAMOUNT"])
        lis = i["INCOMEDATE"].split("-")
        date = int(lis[2])
        incomedate.append(date)
        mont = str(lis[0])+"-"+str(lis[1])
        incomedatemth.append(str(mont)+"-"+str(lis[2]))
        incomemonth.append(mont)

    session["incomedate"] = incomedate
    session["incomemonth"] = incomemonth
    session["incomedatmth"] = incomedatemth
    # print(session["incomedatmth"])
    session["incomevalue"] = incomevalues

def getIncome(userid,conn):
    lis = []    
    incomevalues = {"Salery":0,"Profit":0,"Bonus":0,"Other":0}
    sum = 0
    try:
        sql = "SELECT * FROM VTB79713.INCOME WHERE UUSERID = '"+userid+"' ORDER BY  INCOMEDATE ASC"
        stmt = ibm_db.exec_immediate(conn, sql)

        dictionary = ibm_db.fetch_assoc(stmt)
        while dictionary != False:
            sum=sum+dictionary["INCOMEAMOUNT"]
            if dictionary["INCOMECATEGORY"] == "Salery":
                incomevalues["Salery"] = incomevalues["Salery"]+int(dictionary["INCOMEAMOUNT"])
            elif dictionary["INCOMECATEGORY"] == "Profit":
                incomevalues["Profit"] = incomevalues["Profit"]+int(dictionary["INCOMEAMOUNT"])
            elif dictionary["INCOMECATEGORY"] == "Bonus":
                incomevalues["Bonus"] = incomevalues["Bonus"]+int(dictionary["INCOMEAMOUNT"])
            elif dictionary["INCOMECATEGORY"] == "Other":
                incomevalues["Other"] = incomevalues["Other"]+int(dictionary["INCOMEAMOUNT"])
            lis.append(dictionary)
            dictionary = ibm_db.fetch_assoc(stmt)
        inco(lis)
        session["incomecat"] = incomevalues
        session["inco"] = sum
        session["income"] = lis
        return lis
    except:
        print("Error during retrying Income !")


def profile(userid,name,email,phone,password,budget,con):
    budget = str(budget)
    columns = '"UNAME","UEMAIL","UPHONE","UPASSWORD","UUSERID","UBUDGET"'
    val = "'"+name+"','"+email+"','"+phone+"','"+password+"','"+userid+"','"+budget+"'"
    sql = 'UPDATE VTB79713.USER SET (' + columns + ') = ('+val+') WHERE UUSERID ='+"'"+userid+"'"
    # print(sql)
    try:
        stmt = ibm_db.prepare(con, sql)
        ibm_db.execute(stmt)
        updateuser(name,email,phone,password,budget)
        print("Update Success")
        return "Update Success !"
    except:
        print("Update error !")
        return "Update Error!"


def expe(dict):
    expensedate = []
    expensemonth = []
    expensevalues = []
    expensedatemth=[]
    for i in dict:
        expensevalues.append(i["EXPENSEAMOUNT"])
        lis = i["EXPENSEDATE"].split("-")
        date = int(lis[2])
        expensedate.append(date)
        mont = str(lis[0])+"-"+str(lis[1])
        expensedatemth.append(str(mont)+"-"+str(lis[2]))
        expensemonth.append(mont)

    session["expensedate"] = expensedate
    session["expensemonth"] = expensemonth
    session["expensedatmth"] = expensedatemth
    # print(session["expensedatmth"])
    session["expensevalue"] = expensevalues


def getexpense(userid,conn):
    lis = []
    sum = 0
    expensevalues = {"Entertainment":0,"Food":0,"Fuel":0,"Other":0}
    try:
        sql = "SELECT * FROM VTB79713.EXPENSE WHERE UUSERID = '"+userid+"' ORDER BY EXPENSEDATE ASC"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_assoc(stmt)
        while dictionary != False:
            sum+=dictionary["EXPENSEAMOUNT"]
            if dictionary["EXPENSECATEGORY"] == "Entertainment":
                expensevalues["Entertainment"] = expensevalues["Entertainment"]+int(dictionary["EXPENSEAMOUNT"])
            elif dictionary["EXPENSECATEGORY"] == "Food":
                expensevalues["Food"] = expensevalues["Food"]+int(dictionary["EXPENSEAMOUNT"])
            elif dictionary["EXPENSECATEGORY"] == "Fuel":
                expensevalues["Fuel"] = expensevalues["Fuel"]+int(dictionary["EXPENSEAMOUNT"])
            elif dictionary["EXPENSECATEGORY"] == "Other":
                expensevalues["Other"] = expensevalues["Other"]+int(dictionary["EXPENSEAMOUNT"])
            lis.append(dictionary)
            dictionary = ibm_db.fetch_assoc(stmt)
        expe(lis)
        session["expensecat"] = expensevalues
        session["expe"] = sum
        session["expense"] = lis
        return lis
    except:
        print("Error during retrying expense !")

def updateuser(name,email,phone,password,budget):
    session["username"] = str(name)
    session["useremail"] = str(email)
    session["userpassword"] = str(password)
    session["userphone"] = str(phone)
    session["Userbudget"] = str(budget)

def Signup(name,email,phone,password,conn):

    lis = email.split("@")
    userid = str(lis[0])
    budget = str(0)

    columns = '"UNAME","UEMAIL","UPHONE","UPASSWORD","UUSERID","UBUDGET"'
    val = "'"+name+"','"+email+"','"+phone+"','"+password+"','"+userid+"','"+budget+"'"
    sql = 'Insert into VTB79713.USER(' + columns + ') values('+val+')'
    try:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        print ("added :-)")
        return "success"
    except Exception as e:
        if ibm_db.stmt_error() == "23505" :
            print("already have an account")
            return "already present"
        else:
            print("Error While Adding the User ! ")
            return "database error"

def Signin(email,password,conn):

    sql = "SELECT * FROM vtb79713.USER WHERE UEMAIL = '"+email+"' AND UPASSWORD = '"+password+"'"
    arr=[]
    try:
       stmt = ibm_db.exec_immediate(conn, sql)
       dictionary = ibm_db.fetch_both(stmt)
       if dictionary != False:
        if not dictionary == {}:
            print("Log in Success !")
            arr.append("success")
            arr.append(dictionary)
            getIncome(dictionary["UUSERID"],conn)
            getexpense(dictionary["UUSERID"],conn)
            updateuser(str(dictionary["UNAME"]),email,str(dictionary["UPHONE"]),password,str(dictionary["UBUDGET"]))
            # print(session["income"])
            return arr
       else:
            print("No user is found !")
            arr.append("no user")
            arr.append(dictionary)
            return arr
    except:
        print("Error while retrying data !")
        arr.append("database errors")
        arr.append({})
        return arr
    return arr

def Addincome(userid,amount,incomeid,date,note,category,catid,conn):
    columns = '"UUSERID","INCOMEAMOUNT","INCOMEID","INCOMEDATE","INCOMENOTE","INCOMECATEGORY","CATOGERYNAME"'
    val = "'"+userid+"','"+amount+"','"+incomeid+"','"+date+"','"+note+"','"+category+"','"+catid+"'"
    sql = 'Insert into vtb79713.INCOME(' + columns + ') values('+val+')'
    try:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        print ("Added !")
        return "Income added successfully !"
    except Exception as e:
        print(ibm_db.stmt_errormsg())
        return ibm_db.stmt_error()

def Addexpense(userid,amount,expenseid,date,note,category,catid,conn):
    columns = '"UUSERID","EXPENSEAMOUNT","EXPENSEID","EXPENSEDATE","EXPENSENOTE","EXPENSECATEGORY","CATOGERYNAME"'
    val = "'"+userid+"','"+amount+"','"+expenseid+"','"+date+"','"+note+"','"+category+"','"+catid+"'"
    sql = 'Insert into vtb79713.EXPENSE(' + columns + ') values('+val+')'
    try:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        print ("Added !")
        return "Expense added successfully !"
    except Exception as e:
        print(ibm_db.stmt_errormsg())
        return ibm_db.stmt_error()

def updateincome(userid,amount,incomeid,date,note,catogery,catid,con):
    columns = '"UUSERID","INCOMEAMOUNT","INCOMEID","INCOMEDATE","INCOMENOTE","INCOMECATEGORY","CATOGERYNAME"'
    val = "'"+userid+"','"+amount+"','"+incomeid+"','"+date+"','"+note+"','"+catogery+"','"+catid+"'"
    sql = 'UPDATE vtb79713.INCOME SET (' + columns + ') = ('+val+') WHERE UUSERID ='+"'"+userid+"' AND INCOMEID ='"+incomeid+"'"
    try:
        stmt = ibm_db.prepare(con, sql)
        ibm_db.execute(stmt)
        # print("Update Success")
        return "Update Success"
    except:
        # print("Update error !")
        return "Update Failed"


def deleteincome(incomeid, userid,conn):
    sql="DELETE FROM vtb79713.INCOME WHERE INCOMEID='"+incomeid+"' AND UUSERID='"+userid+"';"
    try:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        print("Delete Success")
        return "Delete Success"
    except:
        print("Delete error !")
        return "Delete Failed"

def updateexpense(userid,amount,expenseid,date,note,catogery,catid,con):
    columns = '"UUSERID","EXPENSEAMOUNT","EXPENSEID","EXPENSEDATE","EXPENSENOTE","EXPENSECATEGORY","CATOGERYNAME"'
    val = "'"+userid+"','"+amount+"','"+expenseid+"','"+date+"','"+note+"','"+catogery+"','"+catid+"'"
    sql = 'UPDATE vtb79713.EXPENSE SET (' + columns + ') = ('+val+') WHERE UUSERID ='+"'"+userid+"' AND EXPENSEID ='"+expenseid+"'"
    try:
        stmt = ibm_db.prepare(con, sql)
        ibm_db.execute(stmt)
        return "Update Success"
    except:
        return "Update Failed"


def deleteexpense(expenseid, userid,conn):
    sql="DELETE FROM vtb79713.EXPENSE WHERE EXPENSEID='"+expenseid+"' AND UUSERID='"+userid+"';"
    try:
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        print("Delete Success")
        return "Delete Success"
    except:
        print("Delete error !")
        return "Delete Failed"