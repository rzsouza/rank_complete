from flask import Flask, render_template, request

app = Flask(__name__)

ranking = [
    {'position': 1, 'name': 'Argentina', 'points': 6},
    {'position': 2, 'name': 'France', 'points': 4},
    {'position': 3, 'name': 'Brazil', 'points': 2},
    {'position': 4, 'name': 'Germany', 'points': 1},
]

matchs = []


@app.route('/')
def index():
    return render_template('index.j2', ranking=ranking)


@app.route('/admin')
def admin():
    return render_template('admin.j2')


@app.route('/match', methods=['POST'])
def add_match():
    home_team = request.form['home_team']
    home_team_score = request.form['home_team_score']
    away_team = request.form['away_team']
    away_team_team_score = request.form['away_team_score']
    return f"{home_team} {home_team_score} X {away_team} {away_team_team_score}"


if __name__ == '__main__':
    app.run()
