from flask import Flask, render_template
app = Flask(__name__, template_folder='views', static_folder='static')

@app.route('/athletes')
def athlete_view():
    return render_template('athlete_view.html')

@app.route('/events')
def event_view():
    return render_template('event_view.html')

if __name__ == '__main__':
    app.run(debug=True)
