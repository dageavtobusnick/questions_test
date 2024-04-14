from keybert import KeyBERT


def get_keywords(question):
    result=[]
    keywords=kw_model.extract_keywords(question, keyphrase_ngram_range=(1,1), stop_words=None)
    for word in keywords:
      if word[1]>0.3:
        result.append(word[0])
    return result

def get_intersections_count(list1,list2):
    count=0
    for word in list1:
        if word in list2:
            count+=1
    return count

f = open('data.txt', 'r')
questions=[]
answers=[]
question=''
answer=''
for line in f:
    print(line)
    if line[len(line)-2]=='?':
        if question!='':
            questions.append(question)
            answers.append(answer)
            question=''
            answer=''
        question=line
    else:
        answer+=line +'\n'
#print(questions)
#print(answers)
keywords=[]
kw_model=KeyBERT()
for question in questions:
    keywords.append(get_keywords(question))
#print(keywords)
while True:
    print("Ask your question.")
    question = input()
    keyword=get_keywords(question)
    possible_indexes=[]
    for i in range(0,len(keywords)):
        count=get_intersections_count(keyword,keywords[i])
        if count>0:
            possible_indexes.append((count,i))
    possible_indexes=sorted(possible_indexes, key=lambda x: x[0],reverse=True)
    for index in possible_indexes:
        print(questions[index[1]])
        print(answers[index[1]])