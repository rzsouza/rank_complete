from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    ranking = [
        {'position': 1, 'name': 'Argentina', 'points': 6},
        {'position': 2, 'name': 'France', 'points': 4},
        {'position': 3, 'name': 'Brazil', 'points': 2},
        {'position': 4, 'name': 'Germany', 'points': 1},
    ]
    return render_template('index.j2', ranking=ranking)


if __name__ == '__main__':
    app.run()
