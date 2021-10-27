from flask import Flask, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import response

from db import db_init, db
from models import Img


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///img.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pic = request.files['pic']

        if not pic:
            return 'no pic upload', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        print('succes')

        return redirect(url_for('upload_file'))


@app.route('/imgs')
def get_img():
    img = Img.query.all()


    return response(render_template('all.html', imgs = img))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
