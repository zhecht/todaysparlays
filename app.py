from flask import Flask, render_template
import os
import controllers

app = Flask(__name__, template_folder='views')

app.register_blueprint(controllers.home)

app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)

