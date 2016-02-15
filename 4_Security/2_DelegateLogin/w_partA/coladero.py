# -*- coding: utf-8 -*-
"""
@title: El Coladero
@description: Aplicación web para detectar y corregir vulnerabilidades
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from bottle import run, template, get, post, request
import sqlite3


@get('/show_all_questions')
def show_all_questions():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    query = """SELECT author,title,time,tags,id 
               FROM Questions 
               ORDER BY time DESC"""
    cur.execute(query)
    res = list(cur.fetchall())
    conn.close()
    return template('messages.html', questions=res)
    

@post('/insert_question')
def insert_question():
    author = request.forms['author']
    title = request.forms['title']
    tags = request.forms['tags']
    body = request.forms['body']
        
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    qbody = """INSERT INTO Questions(author, title, tags, body, time) 
               VALUES ('{0}','{1}','{2}','{3}',CURRENT_TIMESTAMP)"""
    query = qbody.format(author, title, tags, body)
    cur.executescript(query)
    conn.commit()
    conn.close()
    return "Pregunta insertada con exito"

        
@get('/show_question')
def show_question():
    ident = request.query['id']
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    qbody1 = """SELECT author,title,time,tags,body 
                FROM Questions 
                WHERE id={0}"""
    qbody2 = """SELECT author,time,body 
                FROM Replies 
                WHERE question_id={0}"""
    query1 = qbody1.format(ident)
    query2 = qbody2.format(ident)
    cur.execute(query1)
    question = cur.fetchone()
    cur.execute(query2)
    replies = list(cur.fetchall())
    conn.close()
    return template("message_detail.html", q=question, replies=replies, ident=ident)


@post('/insert_reply')
def insert_reply():
    author = request.forms['author']
    body = request.forms['body']
    question_id = request.forms['question_id']
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    qbody = """INSERT INTO Replies(author,body,time,question_id) 
               VALUES ('{0}', '{1}', CURRENT_TIMESTAMP, {2})"""
    query = qbody.format(author, body, question_id)
    cur.execute(query)
    conn.commit()
    conn.close()
    return "Contestación insertada con éxito"
    

@get('/search_question')
def search_question():
    tag = request.query['tag']
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    qbody = """SELECT author,title,time,tags 
               FROM Questions 
               WHERE tags LIKE '%{0}%'
               ORDER BY time DESC"""
    print tag
    print qbody.format(tag)
    query = qbody.format(tag)
    cur.execute(query)
    res = list(cur.fetchall())
    conn.close()
    return template('messages_search.html', questions=res, tag=tag)

    
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
