from flask import Flask, render_template, request, url_for
import file_minator

app = Flask(__name__)


@app.route('/')
def index():
    questions_only = file_minator.all_the_questions()
    return render_template("index.html", questions_only=questions_only)


@app.route('/<new_or_update>/<question_id>', methods=["GET", "POST"])
def details(new_or_update=None, question_id=None, selected_id=None):
    if request.method == "GET":
        result = file_minator.answer_for_question(int(question_id))
        return render_template(
            "form.html", aktion=new_or_update, question_id=question_id, result=result)
    elif request.method == "POST":
        requested = request.form['format']
        if requested == "new_answer":
            req_answer = request.form['new_answer']
            file_minator.new_answer_handler(question_id, req_answer, 0)
    result = file_minator.answer_for_question(int(question_id))
    return render_template(
            "form.html", aktion=new_or_update, question_id=question_id, result=result)


@app.route('/form', methods=['GET', 'POST'])
def form():
    selected = request.form['format']
    if "remove" in selected:
        remove = selected.split("+")[1]
        

if __name__ == '__main__':
    app.run(debug=True)
