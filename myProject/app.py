from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# method 명시되어 있지 않으면 GET, POST 모두 가능
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/write', methods=['GET'])
def write_form():
    return render_template('write.html')


@app.route('/write', methods=['POST'])
def write_review():
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    review = request.form['review']
    thumbnail = request.form['thumbnail']

    print(title, author, publisher, review, thumbnail)

    doc = {
        'title': title,
        'author': author,
        'publisher': publisher,
        'review': review,
        'thumbnail': thumbnail
    }

    db.booked.insert_one(doc)
    print(doc)
    return jsonify({'result': 'success', 'msg': '리뷰가 작성되었습니다!'})


@app.route('/review', methods=['GET'])
def read_all_reviews():
    title = request.args.get('title', 'all')
    print(title)
    filter = {}
    if title != 'all':
        filter = {"title": title}

    review_list = list(db.booked.find(filter, {'_id': False}))
    print(review_list)

    return jsonify({'result': 'success', 'reviews': review_list})


@app.route('/viewReview', methods=['GET'])
def read_review():
    title = request.args.get('title')
    return render_template('readReview.html', title=title)


# index.html에서 책 클릭할 때 책 정보 가져옴
@app.route('/viewReview', methods=['POST'])
def get_title():
    title = request.form['title']
    print(title)
    review = list(db.booked.find({'title': title}, {'_id': False}))
    print(review)
    return jsonify({'result': 'success', 'reviews': review})


@app.route('/search_popup')
def search_popup():
    return render_template('search_popup.html')

# 리뷰 삭제
@app.route('/deleteReview', methods=['POST'])
def delete_review():
    print("deleteReview")
    title = request.form['title']
    print(title)
    delete = db.booked.delete_one({"title": title})
    return jsonify({'result': 'success', 'msg': '리뷰가 작성되었습니다!'})


@app.route('/test', methods=['GET'])
def test_get():
    title_receive = request.args.get('title_give')
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


@app.route('/test', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
