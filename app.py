import os
import sys
import select
import paramiko
import time
import smtplib
from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
def apiCheck():
    return "Message : Remote VM Execution!"

@app.route('/df')
def dfExec():
    return "Message : Sent SSH df -H to remote server : ***REMOVED***!"    

@app.route('/restart')
def restartVM():
    sshclnt = utils.getSSHClient()
    s = sshclnt.get_transport().open_session()
    paramiko.agent.AgentRequestHandler(s)
    sshclnt.exec_command("sudo /sbin/reboot", get_pty=True)
    return "Message : Sent Restart remote server : ***REMOVED***!"  


#-----------------------------------------------------------------------------------------------------------------------
# Utils class 
# getSSHClient : Obtains SSHClient to execute command over SSH
# execCommand : function to execute command over SSH, which also closes connection after command execution
#-----------------------------------------------------------------------------------------------------------------------
class utils():
	def getSSHClient():
		sshclnt = paramiko.SSHClient()
		sshclnt.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
		#sshclnt.connect("***REMOVED***", port=****, username=******, password=********)
		#sshclnt.connect("***REMOVED***", port=****, username=******, password=============)
		sshclnt.connect("***REMOVED***", port=*****, username=******, password=============)
		return sshclnt

	def execCommand(command):
		try:
			sshclnt = utils.getSSHClient()
			stdin, stdout, stderr = sshclnt.exec_command(command)
			print ("stdin", file=sys.stdin)
			print ("stdout", file=sys.stdout)
			print ("stderr=", file=sys.stderr)
			opt = stdout.readlines()
			opt = "".join(opt)
			print(opt)
		except Exception as ex:
			print("Authentication failed, please verify your credentials: %s" % ex)
		finally:
			sshclnt.close() 

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
