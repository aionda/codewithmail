from flask import Flask, request


app = Flask(__name__)

@app.route('/newmail', methods=['POST'])
def newmail():
    print request.form
    return "woo a new email!"

if __name__ == "__main__":
    app.run(
        host = '0.0.0.0', 
        port = 5000,
        debug = True
    )

