from flask import Flask, jsonify
from app.Scraper import scrape_bycatch_solutions

app = Flask(__name__)

@app.route('/recommendations2', methods=['GET'])
def get_recommendations():
    try:
        # Call the scraper function
        solutions = scrape_bycatch_solutions()
        return jsonify({
            "status": "success",
            "data": solutions
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
