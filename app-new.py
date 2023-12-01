from flask import Flask, request, jsonify, render_template, session
from threading import Thread
import time

# Import your utility functions
from src.utils.utilCode import get_reddit_data_for_team, extract_comments_and_scores
from src.utils.utilCode import batch_predict, calculate_sentiment_scores
from src.utils.utilCode import load_model, load_scaler, predict_match_result
from src.utils.utilCode import get_match_odds, oddsScrapper
from src.utils.utilCode import normalize_score
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Load models and scaler
model_home = load_model('models/model_home.joblib')
model_away = load_model('models/model_away.joblib')
scaler = load_scaler('models/scaler.joblib')

# Initialize tokenizer and model for sentiment analysis
tokenizer = AutoTokenizer.from_pretrained('roberta-base')
sentiment_model = TFAutoModelForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')

# Global dictionary to store task status and results
tasks = {}

def long_running_task(home_team, away_team, task_id):
    try:
        # Fetch Reddit data for both teams
        home_team_data = get_reddit_data_for_team(home_team)
        away_team_data = get_reddit_data_for_team(away_team)

        # Extracting comment bodies 
        comment_bodies_Home, _ = extract_comments_and_scores(home_team_data)
        comment_bodies_Away, _ = extract_comments_and_scores(away_team_data)

        # Sentiment Analysis
        home_team_sentiments = batch_predict(comment_bodies_Home, tokenizer, sentiment_model)
        away_team_sentiments = batch_predict(comment_bodies_Away, tokenizer, sentiment_model)


        # Calculate sentiment scores
        current_date = datetime.now()
        home_team_scores = calculate_sentiment_scores(home_team_sentiments, current_date)
        away_team_scores = calculate_sentiment_scores(away_team_sentiments, current_date)

        # Normalize sentiment scores
        home_team_scores = normalize_score(home_team_scores)
        away_team_scores = normalize_score(away_team_scores)


        # Getting match odds
        odd_dict = get_match_odds(oddsScrapper(), home_team, away_team) 

        # Prepare input data for prediction
        match_data = {
            'Home': home_team,
            'Away': away_team,
            'HomeTeam_PositiveSentiment': home_team_scores[0],
            'HomeTeam_NeutralSentiment': home_team_scores[1],
            'HomeTeam_NegativeSentiment': home_team_scores[2],
            'AwayTeam_PositiveSentiment': away_team_scores[0],
            'AwayTeam_NeutralSentiment': away_team_scores[1],
            'AwayTeam_NegativeSentiment': away_team_scores[2],
            'AvgOdds_HomeWin': float(odd_dict['AvgOdds_HomeWin']),
            'AvgOdds_Draw': float(odd_dict['AvgOdds_Draw']),
            'AvgOdds_AwayWin': float(odd_dict['AvgOdds_AwayWin'])
        }
        
        print(match_data)

        # Prediction
        predictions = predict_match_result(match_data, model_home, model_away, scaler)

        # Store the results in the session
        tasks[task_id] = {'status': 'complete', 'data': predictions}
    except Exception as e:
        tasks[task_id] = {'status': 'error', 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-predict', methods=['POST'])
def start_predict():
    home_team = request.form['home_team']
    away_team = request.form['away_team']
    task_id = f"predict_{home_team}_{away_team}"
    tasks[task_id] = {'status': 'pending'}

    thread = Thread(target=long_running_task, args=(home_team, away_team, task_id))
    thread.start()

    return jsonify({'task_id': task_id})

@app.route('/get-results', methods=['POST'])
def get_results():
    task_id = request.form['task_id']
    return jsonify(tasks.get(task_id, {'status': 'pending'}))

if __name__ == '__main__':
    app.run()
