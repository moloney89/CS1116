from flask import Flask, render_template, request, make_response
from database import get_db, close_db
from forms import * 

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.teardown_appcontext(close_db) # This line calls the function within the brackets when the app has finished

@app.route("/vote", methods=["POST","GET"])
def vote():
    if request.cookies.get("voted") == "yes":
        return render_template("feedback.html", message = "Sorry! You already voted.")

    form = VoteForm()

    if form.validate_on_submit():
        vote = form.vote.data
        # Update database with the new vote
        db = get_db()
        db.execute("""UPDATE votes SET total_votes = total_votes + 1 WHERE number = ?;""", (vote,))
        db.commit()

        response = make_response(render_template('feedback.html', message='Thanks for your vote!'))
        response.set_cookie("voted", "yes")
        return response

    return render_template("vote_form.html", form=form)
