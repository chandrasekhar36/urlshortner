from flask import render_template, request, redirect,url_for,flash, abort, session, jsonify,Blueprint
import os.path
import os
import json
from werkzeug.utils import secure_filename

bp=Blueprint('urlshort',__name__)

@bp.route('/')
def home():
    return render_template("home.html",codes=session.keys())

@bp.route('/about')
def about():
    return "You can use me to shorten URL"

@bp.route('/your_url', methods=["GET","POST"])
def your_url():
    if request.method=="POST":
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls=json.load(url_file)
        if request.form['code'] in urls.keys():
            flash('Sorry! Its already taken.... select another short Name')
            return redirect(url_for('urlshort.home'))
        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
        else:
            f=request.files['file']
            full_name=request.form['code']+secure_filename(f.filename)
            f.save(os.getcwd()+'/urlshort/static/user_files/'+full_name)
            urls[request.form['code']]={'file':full_name}
        with open('urls.json','w') as url_file:
            session[request.form['code']]=True
            json.dump(urls, url_file)
        return render_template('your_url.html',code=request.form['code'])
    else:
        return redirect('/')

@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            url=json.load(url_file)
            if code in url.keys():
                if 'url' in url[code].keys():
                    return redirect(url[code]['url'])
                else:
                    return redirect(url_for('static',filename="user_files/"+url[code]['file']))
    return abort(404)



@bp.errorhandler(404)
def url_not_found(error):
    return render_template('page_not_found.html'),404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
