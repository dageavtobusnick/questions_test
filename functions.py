from mysql.connector import connect
import json

def get_keywords(question,config,kw_model):
    result=[]
    keywords=kw_model.extract_keywords(question, keyphrase_ngram_range=(1,1), stop_words=None)
    for word in keywords:
      if word[1]>float(config["Keyword"]["min_keyword_p"]):
        result.append(word[0])
    return result
    
def get_mysql_connection():
    connection=connect(
        host="localhost",
        user="root",
        password="root",
        database="urfu_questions_answers"
    )
    return connection;

def get_intersections_count(list1,list2):
    count=0
    for word in list1:
        if word in list2:
            count+=1
    return count

def init_databese():
    with get_mysql_connection() as connection:
        querry="SHOW TABLES LIKE 'questions_answers';"
        cursor=connection.cursor()
        cursor.execute(querry)
        if (len(cursor.fetchall())<=0):
                    querry="CREATE TABLE `questions_answers` (" \
                                        "`id` int(11) NOT NULL,"  \
                                        "`question` text,"  \
                                        "`answer` text," \
                                        "`keywords` text"  \
                    ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
                    connection.cursor().execute(querry)
                    querry="ALTER TABLE `questions_answers`"\
                            "ADD PRIMARY KEY (`id`);"
                    connection.cursor().execute(querry)
                    querry="ALTER TABLE `questions_answers`" \
                            "MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;"
                    connection.cursor().execute(querry)
        
def load_questions(kw_model,connection,config):
    f = open('data.txt', 'r',encoding="utf-8")
    question=''
    answer=''
    for line in f.readlines():
        if line[len(line)-2]=='?':
            if question!='':
                querry="INSERT INTO questions_answers SET " \
                    "question = '"+question.replace('\n', '\\n').replace("'", "\\'")+"',"\
                    "answer = '"+answer.replace('\n', '\\n').replace("'", "\\'")+"',"\
                    "keywords = '"+json.dumps(get_keywords(question,config,kw_model))+"'"
                connection.cursor().execute(querry)
                connection.commit()
                question=''
                answer=''
            question=line
        else:
            answer+=line 
        

def init_insert(kw_model,config):
    with get_mysql_connection() as connection:
        querry="SELECT * FROM `questions_answers` LIMIT 1;"
        cursor=connection.cursor()
        cursor.execute(querry)
        if (len(cursor.fetchall())<=0):
                    load_questions(kw_model,connection,config)