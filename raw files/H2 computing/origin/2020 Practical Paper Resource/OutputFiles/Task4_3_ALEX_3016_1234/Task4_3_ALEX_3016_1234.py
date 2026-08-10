from TASK4_2_ALEX_3016_1234 import *
import flask

app = flask.Flask(__name__)

@app.route('/')
def start():
    return flask.render_template('start.html')

@app.route('/display/')
def display():
    rows = []
    for line in all_info:
        rows.append((line.getFullName(),line.screen_name(),line.status()))
    return flask.render_template('display.html',rows=rows)

if __name__ == '__main__':
    app.run()
