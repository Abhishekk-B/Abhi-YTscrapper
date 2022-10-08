from flask import render_template, request
from website import app
from website.ytfile import youTubeScrapper, ytScrapper, commentFile, jsonfile
import pandas as pd
import time
from website.database import database, getinfofirst, getcomments, mysqldatabase





@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        product = request.form["product"]
        print(product)
        return render_template("home.html", product = product)
    return render_template("home.html")



    
@app.route("/value/<channel>", methods = ["GET", "POST"])
def value(channel):
    if request.method == 'POST':
        if request.form['btn'] == 'Reload':
            df = youTubeScrapper(channel)
            titles = df['Title'].tolist()
            links = df['Links'].tolist()
            images = df['Image Link'].tolist()
            view = df['Views'].tolist()
            subscriber = df['Subscriber'].tolist()
            numbers = df['Sr.NO'].tolist()
            length = len(numbers)
            return render_template("show.html", product=channel, length=length, titles=titles, images=images,
                                   links=links, numbers=numbers, view=view, subscriber=subscriber)
        else:
            pass
    try:
        try:
            df = getinfofirst(channel)
            titles = df['Title'].tolist()
            links = df['Links'].tolist()
            images = df['Image Link'].tolist()
            view = df['Views'].tolist()
            subscriber = df['Subscriber'].tolist()
            numbers = df['Sr.NO'].tolist()
            length = len(numbers)
            return render_template("show.html", product=channel, length=length, titles=titles, images=images,
                                   links=links, numbers=numbers, view=view, subscriber=subscriber)
        except:
            df = youTubeScrapper(channel)
            titles = df['Title'].tolist()
            links = df['Links'].tolist()
            images = df['Image Link'].tolist()
            view = df['Views'].tolist()
            subscriber = df['Subscriber'].tolist()
            numbers = df['Sr.NO'].tolist()
            length = len(numbers)
            return render_template("show.html", product=channel, length=length, titles=titles, images=images,
                                   links=links, numbers=numbers, view=view, subscriber=subscriber)
    except:
        pass
    return render_template("error.html")



@app.route("/comment/<channel>")
def comment(channel):
    try:
        df = getcomments(channel)
        data = df.values
        return render_template("comment.html", csv=data)
    except:
        try:
            df = getinfofirst(channel)
            links = df['Links'].tolist()
            ytScrapper(links, channel)
            print("video link scraped")
            df = commentFile(channel)
            time.sleep(1)
            database(channel)
            mysqldatabase(channel)
            # df = pd.read_csv(channel + " videos comments.csv", header=0)
            data = df.values
            return render_template("comment.html", csv=data)
        except:
            pass

        return render_template("error.html")


@app.route("/newcomment/<channel>")
def newcomment(channel):
    try:
        k = request.args.get('k', None)
        df = jsonfile(channel, k)
        data = df.values
        title = data[int(k)][1]
        return render_template("new comment.html", csv=data, j= k, title = title)
    except:
        return render_template("commenterror.html")

