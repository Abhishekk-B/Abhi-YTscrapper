import pandas as pd
import sqlite3, json
import pymongo
import pymysql


def commentFile(chan):
    with open(chan + ".json", "r") as json_data:
        data1 = json.load(json_data)
        commentorList = []
        commentList = []
        for i in range(len(data1)):
            commentorList.append((data1[chan + " "+ str(i + 1)]["commentor"]))
            commentList.append(data1[chan + " "+ str(i + 1)]["comment"])
        commentorNames = [val.lstrip().rstrip().replace('"',"'") for sublist in commentorList for val in sublist]
        finalcomments = [val.replace('"',"'") for sublist in commentList for val in sublist]
        sr_no = [x + 1 for x in range(len(commentorNames))]
        zipped = list(zip(sr_no, commentorNames, finalcomments))
        dataframe = pd.DataFrame(zipped, columns=["Sr.NO", "Commentor", "Comments"])
        return dataframe


def mysqlfirstdata(channel_name, zipped):
    channel = channel_name.replace(' ', '')
    df = pd.DataFrame(zipped)
    conn = pymysql.connect(user='root', password='SQLab21#')
    cursor = conn.cursor()
    try:
        query = "create database if not exists ytdb;"
        cursor.execute(query)
        conn.commit()
        query1 = "use ytdb;"
        cursor.execute(query1)
        conn.commit()
    except:
        pass
    try:
        query3 = "create table " + channel + " (id int, title varchar(250), link varchar(250), image varchar(250), views varchar(250), subscribers varchar(250), primary key(id));"
        cursor.execute(query3)
        conn.commit()
    except:
        query = "DROP TABLE " + channel + ";"
        cursor.execute(query)
        conn.commit()
        query3 = "create table " + channel + " (id int, title varchar(250), link varchar(250), image varchar(250), views varchar(250), subscribers varchar(250), primary key(id));"
        cursor.execute(query3)
        conn.commit()
    insert_query = 'INSERT INTO ' + channel + ' VALUES '
    for i in range(df.shape[0]):
        insert_query += "("

        for j in range(df.shape[1]):
            insert_query += '"' + str(df[df.columns.values[j]][i]) + '"' + ", "
        insert_query = insert_query[:-2] + "), "

    insert_query = insert_query[:-2] + ";"
    cursor.execute(insert_query)
    conn.commit()
    print("MYSQL Table 1 created")



def mysqldatabase(channel_name):
    channel = channel_name.replace(' ', '')
    df2 = commentFile(channel_name)
    conn = pymysql.connect(user='root', password='SQLab21#')
    cursor = conn.cursor()
    try:
        query = "create database if not exists ytdb;"
        cursor.execute(query)
        conn.commit()
        query1 = "use ytdb;"
        cursor.execute(query1)
        conn.commit()
    except:
        pass
    try:
        query4 = "create table " + channel + "comments (id int, commentor varchar(250), comments text, primary key(id));"
        cursor.execute(query4)
        conn.commit()
    except:
        query = "DROP TABLE " + channel + "comments;"
        cursor.execute(query)
        conn.commit()
        query4 = "create table " + channel + "comments (id int, commentor varchar(250), comments text, primary key(id));"
        cursor.execute(query4)
        conn.commit()

    query4 = "create table if not exists " + channel + "comments (id int, commentor varchar(250), comments text, primary key(id));"
    cursor.execute(query4)
    conn.commit()
    insert_query = 'INSERT INTO ' + channel + 'comments VALUES '
    for i in range(df2.shape[0]):
        insert_query += "("

        for j in range(df2.shape[1]):
            insert_query += '"' + str(df2[df2.columns.values[j]][i]) + '"' + ", "
        insert_query = insert_query[:-2] + "), "

    insert_query = insert_query[:-2] + ";"
    cursor.execute(insert_query)
    conn.commit()
    print("MYSQL Database added")


def firstdata(channel_name, zipped):
    channel = channel_name.replace(' ', '')
    df = pd.DataFrame(zipped)
    db = sqlite3.connect("project.db")
    cursor = db.cursor()
    try:
        query3 = "create table " + channel + " (id int, title varchar(250), link varchar(250), image varchar(250), views varchar(250), subscribers varchar(250), primary key(id));"
        cursor.execute(query3)
        db.commit()
    except:
        query = "DROP TABLE " + channel + ";"
        cursor.execute(query)
        db.commit()
        query3 = "create table " + channel + " (id int, title varchar(250), link varchar(250), image varchar(250), views varchar(250), subscribers varchar(250), primary key(id));"
        cursor.execute(query3)
        db.commit()
    insert_query = 'INSERT INTO ' + channel + ' VALUES '
    for i in range(df.shape[0]):
        insert_query += "("

        for j in range(df.shape[1]):
            insert_query += '"' + str(df[df.columns.values[j]][i]) + '"' + ", "
        insert_query = insert_query[:-2] + "), "

    insert_query = insert_query[:-2] + ";"
    cursor.execute(insert_query)
    db.commit()
    print("Table 1 created")



def database(channel_name):
    channel = channel_name.replace(' ', '')
    db = sqlite3.connect("project.db")
    cursor = db.cursor()
    df2 = commentFile(channel_name)
    try:
        query4 = "create table " + channel + "comments (id int, commentor varchar(250), comments text, primary key(id));"
        cursor.execute(query4)
        db.commit()
    except:
        query = "DROP TABLE " + channel + "comments;"
        cursor.execute(query)
        db.commit()
        query4 = "create table " + channel + "comments (id int, commentor varchar(250), comments text, primary key(id));"
        cursor.execute(query4)
        db.commit()

    query4 = "create table if not exists " + channel + "comments (id int, commentor varchar(250), comments text, primary key(id));"
    cursor.execute(query4)
    db.commit()
    insert_query = 'INSERT INTO ' + channel + 'comments VALUES '
    for i in range(df2.shape[0]):
        insert_query += "("

        for j in range(df2.shape[1]):
            insert_query += '"' + str(df2[df2.columns.values[j]][i]) + '"' + ", "
        insert_query = insert_query[:-2] + "), "

    insert_query = insert_query[:-2] + ";"
    cursor.execute(insert_query)
    db.commit()
    print("Database added")


def getinfofirst(channel_name):
    channel = channel_name.replace(' ', '')
    db = sqlite3.connect("project.db")
    cursor = db.cursor()
    query3 = "Select * from " + channel + ";"
    ab = cursor.execute(query3).fetchall()
    db.commit()
    df = pd.DataFrame(ab,columns=["Sr.NO","Title", "Links", "Image Link", "Views", "Subscriber"])
    return df

def getcomments(channel_name):
    channel = channel_name.replace(' ', '')
    db = sqlite3.connect("project.db")
    cursor = db.cursor()
    query3 = "Select * from " + channel + "comments;"
    ab = cursor.execute(query3).fetchall()
    db.commit()
    df = pd.DataFrame(ab,columns=["Sr.NO","commentor", "comments text"])
    return df


def mongodata(dictionary, channel):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['YTScrapperdb']
    collection = db[channel]
    collection.insert_one(dictionary)
    print("Mongodb Data Added")



