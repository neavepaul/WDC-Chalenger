from flask import Flask, jsonify, Response
from flask_cors import CORS
from tree import build_tree_stream

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

scores = {
    'max': 362,
    'lando': 315
}

race_schedule = {
    "Brazil": {"type": "sprint", "main_date": "2024-11-03", "sprint_date": "2024-11-02"},
    "Las Vegas": {"type": "main", "main_date": "2024-11-18"},
    "Qatar": {"type": "sprint", "main_date": "2024-12-01", "sprint_date": "2024-11-30"},
    "Abu Dhabi": {"type": "main", "main_date": "2024-12-08"}
}

@app.route('/api/get-tree', methods=['GET'])
def get_tree():
    remaining_races = [
        race_schedule["Brazil"],
        race_schedule["Las Vegas"],
        race_schedule["Qatar"],
        race_schedule["Abu Dhabi"]
    ]
    initial_max_points = scores['max']
    initial_lando_points = scores['lando']

    def tree_stream():
        for node_data in build_tree_stream(initial_max_points, initial_lando_points, remaining_races):
            yield f'data: {node_data}\n\n'

    return Response(tree_stream(), content_type='text/event-stream')

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
