from random import randint
from flask import Flask, request, session, redirect, url_for
from db_scripts import get_question_after, get_quizes

def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
def end_quiz():
    session.clear()
def quiz_form():
    html_beg='''<html><body><h2>Выберите викторину:</h2><form method="post" action="index"><select name="quiz">'''
    frm_submit = '''<p><input type="submit" value = "Выбрать", </p>'''
    html_end = '''</select>''' + frm_submit + '''</form><body></html>'''
    options = ''' '''
    q_list = get_quizes()
    for id, name in q_list:
        option_line = ('''<option value="''' + str(id) + '''">''' +str(name) + '''</option>''')
        options = options + option_line
    return html_beg+options+html_end
def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
    else:
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)
        return redirect(url_for('test'))
def test():
    result = get_question_after(session['last_question'], session['quiz'])
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            session['last_question'] = result[0]
            return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '<h1>'
    
def result():
    return "that's all folks!"

app = Flask(__name__)
app.add_url_rule('/', 'index', index)

app.add_url_rule('/index', 'index', methods=['post', 'get'])

app.add_url_rule('/test', 'test', test)
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
    app.run()