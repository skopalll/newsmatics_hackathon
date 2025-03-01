from flask import Flask, jsonify
import helpers

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello from the backend!"})

@app.route('/date', methods=['GET'])
def date_endpoint():
    # Expect a query parameter like ?date=2025.02.28
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'The "date" parameter is required.'}), 400
    
    topics = helpers.get_topic_by_date(date_str.replace(".", "-"))
    
    articles_dict = {}

    for index, (id, date, title, text) in enumerate(topics):
        articles = helpers.get_article_by_topic_id(id)
        articles_dict[index] = articles
    
    return jsonify(articles_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
