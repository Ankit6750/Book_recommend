from flask import Flask, render_template, request
import pickle
import numpy as np
import requests

popular_df = pickle.load(open("popular_df.pkl", 'rb'))
pt = pickle.load(open("pt.pkl", 'rb'))
books = pickle.load(open("books.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# print(popular_df)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           name=list(popular_df['Book-Title'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           author=list(popular_df['Book-Author'].values),
                           vote=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_sy():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend_book():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_list = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_list:
        item = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M']))
        data.append(item)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
