from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_click', methods=['POST'])
def log_click():
    # Perform any backend logic here
    return jsonify({"status": "success", "message": "Click logged"})

if __name__ == '__main__':
    app.run(debug=True)