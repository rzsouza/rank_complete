from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from match import Match

app = Flask(__name__)

ranking = []

points: dict[str, int] = {}

matches: list[Match] = []


@app.route("/")
def index():
    return render_template("index.j2", ranking=ranking)


@app.route("/admin")
def admin():
    return render_template("admin.j2")


def update_ranking(match: Match):
    global ranking
    home_points = 1
    away_points = 1

    if match.home_team_score > match.away_team_score:
        home_points = 3
        away_points = 0
    if match.home_team_score < match.away_team_score:
        home_points = 0
        away_points = 3

    points[match.home_team] = points.get(match.home_team, 0) + home_points
    points[match.away_team] = points.get(match.away_team, 0) + away_points

    ranking = sorted(points.items(), key=lambda item: item[1], reverse=True)


@app.route("/match", methods=["POST"])
def add_match():
    home_team = request.form["home_team"]
    home_team_score = int(request.form["home_team_score"])
    away_team = request.form["away_team"]
    away_team_team_score = int(request.form["away_team_score"])
    date = datetime.now()
    match = Match(home_team, home_team_score, away_team, away_team_team_score, date)
    matches.append(match)
    update_ranking(match)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
