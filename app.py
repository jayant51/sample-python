import os
import sys
import select
import paramiko
import time
import smtplib
import platform
import subprocess
from flask import Flask, jsonify, request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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


@app.route('/checkVMStatus')
@app.route('/verifyVMStatus')
@app.route('/isVMUp')
def isvmup():
    try:
        timeout = 1
        host = "10.0.0.1"
        retval = "True"
        if platform.system() == "Windows":
            command = "ping "+host+" -n 1 -w "+str(timeout*1000)
        else:
            command = "ping -i "+str(timeout)+" -c 1 " + host
        response = os.system(command)
        if response == 0:
            retval = "True"
        else:
            retVal = "False"
    except Exception as ex:
        print("Error: ping exception = ", ex)
    return retval


@app.route('/isVMDown')
def isvmdown():
    if isvmup() == "True":
        return "False"
    else:
        return "True"


@app.route('/postmsg', methods=['POST'])
def post_msg():
    log = "in post msg"
    data = request.get_json()

    toaddrs = data.get("emailid")
    log = log + toaddrs
    email_msg = data.get("msg")
    log = log + email_msg
    email_subj = data.get("subject")
    log = log + email_subj
    slog = send_email(toaddrs, email_subj, email_msg)

    return log + " " + slog + "  message : Completed Send Email"


def send_email(toaddrs, email_subj, email_msg):
    #The mail addresses and password
    sender_address = 'testibmvz@gmail.com'
    sender_pass = 'password!2E'
    receiver_address = 'testibmvz@gmail.com'

    mail_content = " Hello,  This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library. Thank You"


    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address

    fromaddr = "some.body@ibm.com"
    #toaddrs  = ["Jayant.kulkarni@ibm.com;Jayant.kulkarni@ibm.com"]

    msg = MIMEText(email_msg)
    msg['Subject'] = email_subj

    try:
        log = "creating SMTP"
        #server = smtplib.SMTP( ============, 25)
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line

        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        # login with mail_id and password
        session.login("testibmvz@gmail.com", "password!2E")
        session.set_debuglevel(1)
        text = message.as_string()
        log = log + "calling send email"
        session.sendmail(sender_address, receiver_address, text)
        log = log + "done send email"
        session.quit()
        log = log + "Successfully sent email"
    except Exception as ex:
        print("Error: unable to send email", ex)
        log = log + "Error: unable to send email" + str(ex)
    return log
    # -----------------------------------------------------------------------------------------------------------------------
# Utils class
# getSSHClient : Obtains SSHClient to execute command over SSH
# execCommand : function to execute command over SSH, which also closes connection after command execution
# -----------------------------------------------------------------------------------------------------------------------


class utils():
    def getSSHClient():
        sshclnt = paramiko.SSHClient()
        sshclnt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #sshclnt.connect("***REMOVED***", port=****, username=******, password=********)
        #sshclnt.connect("***REMOVED***", port=****, username=******, password=============)
        sshclnt.connect("***REMOVED***",
                        port=*****, username=******, password=============)
        return sshclnt

    def execCommand(command):
        try:
            sshclnt = utils.getSSHClient()
            stdin, stdout, stderr = sshclnt.exec_command(command)
            print("stdin", file=sys.stdin)
            print("stdout", file=sys.stdout)
            print("stderr=", file=sys.stderr)
            opt = stdout.readlines()
            opt = "".join(opt)
            print(opt)
        except Exception as ex:
            print("Authentication failed, please verify your credentials: %s" % ex)
        finally:
            sshclnt.close()


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
