from flask import Flask, request
from Helpers import clickup

app = Flask(__name__)


@app.route('/api/auth/clickup')
def clickup_api():
    text = '<a href="#"> %s</a>'
    return text % clickup.callback()



if __name__ == '__main__':
    app.run(debug=True, port=8027)
