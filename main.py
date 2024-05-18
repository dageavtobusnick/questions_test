from keybert import KeyBERT
from fastapi import FastAPI
import json
import configparser
import models
import functions



kw_model=KeyBERT()
config = configparser.ConfigParser()
config.read("settings.ini")
functions.init_databese()
functions.init_insert(kw_model,config)
app = FastAPI()
    
@app.post("/answer")         
def answer(question:models.TextToAnswer): 
    with functions.get_mysql_connection() as connection:
        keyword=functions.get_keywords(question.question,config,kw_model)
        querry="SELECT answer,keywords,question FROM `questions_answers`;"
        cursor=connection.cursor()
        cursor.execute(querry)
        res=cursor.fetchall()
        keywords=list(map(lambda x: json.loads(x[1]), res))
        possible_indexes=[]
        for i in range(0,len(keywords)):
             count=functions.get_intersections_count(keyword,keywords[i])
             if count>0:
                 possible_indexes.append((count,i))
        possible_indexes=sorted(possible_indexes, key=lambda x: x[0],reverse=True)
        result=[]
        for index in possible_indexes:
            result.append({'question':res[index[1]][2],'answer':res[index[1]][0]})
        return result;
    
@app.post("/answer/add")         
def add(question:models.newQuestion): 
    with functions.get_mysql_connection() as connection:
        querry="INSERT INTO questions_answers SET " \
            "question = '"+question.question.replace('\n', '\\n').replace("'", "\\'")+"',"\
            "answer = '"+question.answer.replace('\n', '\\n').replace("'", "\\'")+"',"\
            "keywords = '"+json.dumps(functions.get_keywords(question.question,config,kw_model))+"'"
        cursor=connection.cursor()
        cursor.execute(querry)
        connection.commit()
        return  {"message": "ОК"};
    
@app.get("/answer/all")         
def all_answers(): 
    with functions.get_mysql_connection() as connection:
        querry="SELECT id,question,answer FROM `questions_answers`;"
        cursor=connection.cursor()
        cursor.execute(querry)
        res=list(map(lambda x: {"id":x[0],"question":x[1],"answer":x[2]},cursor.fetchall()))
        return  res;
    
@app.put("/answer/edit")         
def edit(question:models.editQuestion): 
    with functions.get_mysql_connection() as connection:
        querry="UPDATE questions_answers SET " \
            "question = '"+question.question.replace('\n', '\\n').replace("'", "\\'")+"',"\
            "answer = '"+question.answer.replace('\n', '\\n').replace("'", "\\'")+"',"\
            "keywords = '"+json.dumps(functions.get_keywords(question.question,config,kw_model))+"' WHERE id="+str(question.id)+";"
        cursor=connection.cursor()
        cursor.execute(querry)
        connection.commit()
        return  {"message": "ОК"};
    
@app.delete("/answer/delete")         
def delete(id:int): 
    with functions.get_mysql_connection() as connection:
        querry="DELETE FROM questions_answers WHERE id="+str(id)+";"
        cursor=connection.cursor()
        cursor.execute(querry)
        connection.commit()
        return  {"message": "ОК"};