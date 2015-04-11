from flask import Flask, request
import sys, subprocess, sendgrid

app = Flask(__name__)

@app.route('/newmail', methods=['POST'])
def execute():
    to_email = request.form['to']
    from_email = request.form['from']
    file_name = request.form['subject']
    program = request.form['text']

    #put the email message in a file
    f = open(file_name, "r+")    
    #return "file_name: "+file_name+"\nhtml: "+program
    f.write(program);

    #execute the file and redirect STDERROR and STDOUT to a file    
    cmd = ["python", file_name]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    reply(p.stdout.read(), to_email, from_email, file_name, program)   
    return ('', 204)

def reply(output, to_email, from_email, file_name, program):
    #put the output file in the reply message
    sg = sendgrid.SendGridClient("compilerapp", "mycompiler1")
    message = sendgrid.Mail()

    message.add_to(from_email)
    message.set_from(to_email)
    message.set_subject("Output of " + file_name)
    message.set_text(output)

    sg.send(message)

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 5000,
        debug = True
    )

