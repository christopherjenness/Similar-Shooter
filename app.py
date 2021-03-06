"""
Flask app for finding players with similar shot charts
"""
import matplotlib

matplotlib.use('Agg')

import os
from flask import Flask, render_template, request
from analysis import analysis


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Function called on main page
    Returns:
        Renders a template of home page
    """
    return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    """
    Function called after a player is selected
    Returns:
        Reners a template of results with target player and matches
    """
    if request.method == 'POST':
        player_name = request.form['playername']
        FGA, FGP = analysis.load_data()
        similarities = analysis.get_similar_shooters(player_name, FGA, FGP)
        players = list(similarities.sort('KL-divergence',
                                         ascending=True).head()['player'])
        return render_template('results.html', players=players,
                               target=player_name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
