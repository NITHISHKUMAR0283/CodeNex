from flask import Flask, send_file, request, jsonify
from movie_recommender import MovieRec
import os
app=Flask(__name__)
recommender=None
def init():
    global recommender
    print("Starting...")
    recommender=MovieRec()
    success=recommender.setup()
    if success:
        print("Ready!")
    else:
        print("Failed")
    return success
@app.route('/')
def home():
    return send_file('index.html')
@app.route('/api/search')
def search():
    query=request.args.get('q', '')
    if not query:
        return jsonify({'movies': []})
    try:
        results=recommender.search(query)
        return jsonify({'movies': results})
    except Exception as error:
        return jsonify({'movies': []})
@app.route('/api/recommend')
def recommend():
    movie=request.args.get('movie', '')
    if not movie:
        return jsonify({'error': 'Need movie name'})
    try:
        recommendations=recommender.recommend(movie)
        if not recommendations:
            return jsonify({'error': f'Movie "{movie}" not found'})
        return jsonify({'recommendations': recommendations})
    except Exception as error:
        print(f"Error: {error}")
        return jsonify({'error': 'Error occurred'})
if __name__=='__main__':
    print("Starting app...")
    if init():
        port = int(os.environ.get('PORT', 5000))
        print(f"Server starting on port {port}...")
        app.run(debug=False, port=port, host='0.0.0.0')
    else:
        print("Could not start")