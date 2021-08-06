#Imports
from preprocessing import *
import urllib.request as ur, json

#Get the comments
def get_comments(data):
    for i in data['items']:
        for k, v in i['snippet']['topLevelComment']['snippet'].items():
            if k == "textDisplay":
                comments.append(v)

comments = ["में बहुत खुश था आज नहीं"]

#Run task
for comment in comments:
    #Filter
    #print("Original:",comment)
    fitered_comment = filter(comment)
    #print("After Filtration:",fitered_comment)
    #Tokenize
    tokens = tokenize(fitered_comment)
    #print("After Tokenization:",tokens)
    #Removing empty chararcters
    tokensFinal = [tokens[i] for i in range(len(tokens)) if len(tokens[i]) > 1 and tokens[i] != '']
    if script_validation(tokensFinal):
        #Converting tokens to dictionary
        tokDict = separate_into_dict(tokensFinal)
        #Removing stopwords
        stopRemoved = hindiStopwordsRemover(tokDict)
        #print("Removed Stopwords:",stopRemoved)
        #Lemmatization
        lemmHin = lemmatize_hi(stopRemoved)
        #print("Lemmatization:",lemmHin)
        #POS Tagging
        postag = postagger_hi(lemmHin)
        #print("POS Tagging:",postag)
        #Negation Handling
        negHin = negation_handling_hin(postag)
        #print("Negation Handling:",negHin)
        #Sentiment Score
        senti = sentiment(negHin)
        print(comment,senti)
