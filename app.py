from flask import Flask, request
import sys, subprocess, sendgrid, os, time

app = Flask(__name__)

@app.route('/newmail', methods=['POST'])
def execute():
    to_email = request.form['to']
    from_email = request.form['from']
    file_name = request.form['subject'] 
    file_name_unique = file_name + from_email + str(int(time.time()))
    program = request.form['text'].replace(u'\xa0', u' ')

    #put the email message in a file
    f = open(file_name_unique, "w")    
    f.write(program)
    f.close()

    #execute the file and redirect STDERROR and STDOUT to a file    
    cmd = ["python", file_name_unique]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    reply(p.stdout.read(), to_email, from_email, file_name, program, file_name_unique)   
    return ('', 204)

def reply(output, to_email, from_email, file_name, program, file_name_unique):
    #put the output file in the reply message
    sg = sendgrid.SendGridClient("compilerapp", "mycompiler1")
    message = sendgrid.Mail()

    message.add_to(from_email)
    message.set_from(to_email)
    message.set_subject("Output of " + file_name)
    message.set_text(output)

    sg.send(message)
    os.remove(file_name_unique)

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 5000,
        debug = True
    )

