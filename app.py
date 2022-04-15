from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/')
def apiCheck():
    return "Message : Remote VM Execution!"

@app.route('/df')
def dfExec():
    return "Message : Sent SSH df -H to remote server : ***REMOVED***!"    

@app.route('/restart')
def dfExec():
    return "Message : Sent Restart remote server : ***REMOVED***!"  


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
