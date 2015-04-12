from flask import Flask, request
import sys, subprocess, sendgrid, os, time, threading

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
    start_time = time.time();
    #command = Command("python " + file_name_unique)
    #result = command.run(timeout = 5)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
    reply(p.stdout.read(), to_email, from_email, file_name, program, file_name_unique)   
    '''
    if(result != 0):
        print "infinite loop"
    else:
        print "good result"
    '''

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

class Command(object):
    def __init__ (self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell = True)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)

        if thread.is_alive():
            self.process.terminate()
            thread.join()
        return self.process.returncode

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 5000,
        debug = True
    )

