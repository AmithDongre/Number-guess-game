from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "guessing-secret-key"

LEVELS = {
    "easy": (10, 5),
    "medium": (50, 7),
    "hard": (100, 10)
}

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    game_over = False
    won = False

    # Initialize best score
    if "best_score" not in session:
        session["best_score"] = None

    if request.method == "POST":

        # Restart game
        if "restart" in request.form:
            session.pop("number", None)
            session.pop("attempts", None)
            session.pop("max", None)
            return redirect(url_for("index"))

        # Start new game
        if "level" in request.form:
            level = request.form["level"]
            max_num, attempts = LEVELS[level]

            session["number"] = random.randint(1, max_num)
            session["attempts"] = attempts
            session["max"] = max_num
            session["initial_attempts"] = attempts

            message = f"Game started! Guess a number between 1 and {max_num}."

        # Handle guess
        elif "guess" in request.form and "number" in session:
            guess = int(request.form["guess"])
            number = session["number"]
            attempts = session["attempts"]

            if attempts <= 0:
                game_over = True
                message = f"😢 You lost! The number was {number}."
            else:
                session["attempts"] -= 1

                if guess == number:
                    won = True
                    game_over = True
                    used_attempts = session["initial_attempts"] - session["attempts"]

                    # Update best score
                    if session["best_score"] is None or used_attempts < session["best_score"]:
                        session["best_score"] = used_attempts

                    message = f"🎉 You won in {used_attempts} attempts!"
                elif guess < number:
                    message = "📉 Too low!"
                else:
                    message = "📈 Too high!"

                if session["attempts"] == 0 and not won:
                    game_over = True
                    message = f"😢 You lost! The number was {number}."

    return render_template(
        "index.html",
        message=message,
        attempts=session.get("attempts"),
        max_num=session.get("max"),
        game_over=game_over,
        won=won,
        best_score=session.get("best_score")
    )

if __name__ == "__main__":
    app.run(debug=True)
