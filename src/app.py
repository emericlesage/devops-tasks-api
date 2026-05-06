from flask import Flask, jsonify, request
app = Flask(__name__)
tasks = []  # Base de données en mémoire
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {"id": len(tasks)+1, "title": data['title'], "done": False}
    tasks.append(task)
    return jsonify(task), 201
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
