from flask import Flask, render_template, request, redirect, url_for

from models.match import Match
from services.ranking_service import RankingService

app = Flask(__name__)

ranking_service = RankingService()


@app.route("/")
def index():
    return render_template("index.j2", ranking=ranking_service.ranking)


@app.route("/admin")
def admin():
    return render_template("admin.j2")


@app.route("/match", methods=["POST"])
def add_match():
    match = _extract_match()
    ranking_service.add_match(match)

    return redirect(url_for("index"))


def _extract_match():
    home_team = request.form["home_team"]
    home_team_score = int(request.form["home_team_score"])
    away_team = request.form["away_team"]
    away_team_team_score = int(request.form["away_team_score"])
    return Match(home_team, home_team_score, away_team, away_team_team_score)


if __name__ == "__main__":
    app.run()
