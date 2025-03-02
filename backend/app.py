from flask import Flask, jsonify, request
from flask_cors import CORS
import helpers

app = Flask(__name__)
CORS(app, resources={"/date": {"origins": "http://localhost"}, "/dates:" : {"origins": "http://localhost"}})

@app.route('/')
def index():
    return jsonify({"message": "Hello from the backend!"})

@app.route('/date', methods=['GET'])
def get_articles_for_date():
    # Expect a query parameter like ?date=2025.02.28
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'The "date" parameter is required.'}), 400
    
    topics = helpers.get_topics_by_date(date_str.replace(".", "-"))
    if not topics:
        return jsonify({'error': 'No topics found for the given date.'}), 404
    
    articles_dict = {}

    for index, (id, date, title, text) in enumerate(topics):
        articles = helpers.get_articles_by_topic_id(id)
        articles_dict[str(index)] = {"title": title, "articles": articles}
    
    print(articles_dict)
    
    return jsonify(articles_dict)

@app.route('/dates', methods=['GET'])
def get_possible_dates():
    dates_lists = helpers.get_topic_dates()
    if not dates_lists:
        return jsonify({'error': 'No topics.'}), 404

    dates = []
    for date in dates_lists:
        dates.append(date[0])

    return jsonify(dates)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
