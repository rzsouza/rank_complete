from datetime import datetime

from flask import Flask, render_template, request

from match import Match

app = Flask(__name__)

ranking = [
    {'position': 1, 'name': 'Argentina', 'points': 6},
    {'position': 2, 'name': 'France', 'points': 4},
    {'position': 3, 'name': 'Brazil', 'points': 2},
    {'position': 4, 'name': 'Germany', 'points': 1},
]

matches: list[Match] = []


@app.route('/')
def index():
    return render_template('index.j2', ranking=ranking)


@app.route('/admin')
def admin():
    return render_template('admin.j2')


@app.route('/match', methods=['POST'])
def add_match():
    home_team = request.form['home_team']
    home_team_score = int(request.form['home_team_score'])
    away_team = request.form['away_team']
    away_team_team_score = int(request.form['away_team_score'])
    date = datetime.now()
    matches.append(Match(home_team, home_team_score, away_team, away_team_team_score, date))
    return f"{matches}"


if __name__ == '__main__':
    app.run()
