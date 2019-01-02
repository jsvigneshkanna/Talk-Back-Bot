#importing the wolframalpha API to access it's portal
#importing wikipedia API, MODULE to access it' portal
import wolframalpha
import wikipedia

#passing the question ang language in which answer to be seen
def search(question, lang):

    q = question
#try the wolframalpha search
    try:
        app_id = "ADD THE APP ID FROM WOLFRAMALPHA"
        client = wolframalpha.Client(app_id)
        result = client.query(q)
        answer = next(result.results).text
        print(answer)
        
#if above doesn't satisfy then try wikipedia search
    except:

        wikipedia.set_lang(lang)
        answer = wikipedia.summary(q)
        print(answer)

#get question and language from the user
        
ques = input("enter the question:  ")
lang = input("enter the language to be answer shown:  ")

#change lang string to standard of wikipedia
if(lang.lower() == 'english'):
            lang ='en'
elif(lang.lower() == 'tamil'):
            lang = 'ta'
else:
            print("this works only in english and tamil")

#start the search function
search(ques,lang)
