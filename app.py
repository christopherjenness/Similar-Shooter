from flask import Flask, render_template, request
from wtforms import Form, SelectField
from analysis import analysis
from shotchart import shotchart



app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        player_name = request.form['playername']
        FGA, FGP = analysis.load_data()
        similarities = analysis.get_similar_shooters(player_name, FGA, FGP)
        players = list(similarities.sort('KL-divergence', ascending=True).head()['player'])
        return render_template('results.html', players=players, target=player_name)
