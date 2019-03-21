from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS

from service.question_service import search as search_question, question_search as detail_question

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 用于处理跨域问题


# 首页
@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search/<question>')
def search(question):
    response = make_response(jsonify({
        'success': True,
        "data": search_question(question)
    }))
    return response


@app.route('/detail/<question>')
def question(question):
    response = make_response(jsonify({
        'success': True,
        "data": detail_question(question)
    }))
    return response


if __name__ == '__main__':
    app.run(debug=True)
