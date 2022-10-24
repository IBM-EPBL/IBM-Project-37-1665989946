from flask import Flask,redirect, render_template, request
import Connection
 
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')

conn = Connection.Connect()
files = Connection.get_bucket_contents("nalaiyathiransample",conn)
print(files)

#Index page
@app.route('/',)
def index():
    return render_template('index.html',files = files,len=len(files))

if __name__=='__main__':
    # Connection.get_bucket_contents("nalaiyathiransample",conn)
    # Connection.get_buckets(conn)
    app.run(debug = True)