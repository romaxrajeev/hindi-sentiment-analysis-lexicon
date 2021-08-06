#Imports and initialization of pipeline
import stanza
import string
import HindiSWN
import re
#For lemmatization
nlp_hi = stanza.Pipeline('hi')

#Function to tokenize
def tokenize(sentence):
    hindi_tokens = []
    word = ''
    for j in sentence:
        if j == ' ':
            hindi_tokens.append(word)
            word = ''
        else:
            word = word + j
    hindi_tokens.append(word)
    return(hindi_tokens)

#Make into dict
def separate_into_dict(tokens):
    return {i:token for i,token in enumerate(tokens)}


#Function to remove unwanted characters
def filter(tokenString):
    #Remove numbers
    tokenString = re.sub(r"\d+", '', tokenString)
    #Remove URLS
    tokenString = re.sub(r'(https?|ftp|www)\S+', '', tokenString)
    #Remove punctuations
    exclist = string.punctuation
    table_ = tokenString.maketrans('', '', exclist)
    tokenString = tokenString.translate(table_)
    #Remove extra spaces
    tokenString = re.sub(' +'," ",tokenString).strip()
    #Remove hashtags
    tokenString = ''.join([x + ' ' for x in tokenString.split(" ") if not x.startswith("#")]).strip()
    #Remove emojis
    pattenr = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    tokenString = pattenr.sub(r'',tokenString)
    return tokenString    

#Function to remove stopwords
def hindiStopwordsRemover(hinDict):
    stopwords = ['मैं', 'मुझको', 'मेरा', 'अपने आप को', 'हमने', 'हमारा', 'अपना', 'हम', 'आप', 'आपका', 'तुम्हारा', 'अपने आप', 'स्वयं',
             'वह', 'इसे, उसके', 'खुद को', 'कि वह', 'उसकी', 'उसका', 'खुद ही', 'यह', 'इसके', 'उन्होने', 'अपने', 'क्या', 'जो', 'किसे',
             'किसको', 'कि', 'ये', 'हूँ', 'होता है', 'रहे', 'थी', 'थे', 'होना', 'गया', 'किया जा रहा है', 'किया है', 'है', 'पडा', 'होने', 'करना',
             'करता है', 'किया', 'रही', 'एक', 'लेकिन', 'अगर', 'या', 'क्यूंकि', 'जैसा', 'जब तक', 'जबकि', 'की', 'पर', 'द्वारा', 'के लिए', 'साथ',
             'के बारे में', 'खिलाफ', 'बीच', 'में', 'के माध्यम से', 'दौरान', 'से पहले', 'के बाद', 'ऊपर', 'नीचे', 'को', 'से', 'तक', 'से नीचे', 'करने में', 'निकल', 'बंद', 'से अधिक',
             'तहत', 'दुबारा', 'आगे', 'फिर', 'एक बार', 'यहाँ', 'वहाँ', 'कब', 'कहाँ', 'क्यों', 'कैसे', 'सारे', 'किसी', 'दोनो', 'प्रत्येक', 'ज्यादा', 'अधिकांश', 'अन्य', 'में कुछ', 'ऐसा', 
             'में कोई', 'मात्र', 'खुद', 'समान', 'इसलिए', 'बहुत', 'सकता', 'जायेंगे', 'जरा', 'चाहिए', 'अभी', 'और', 'कर दिया', 'रखें', 'का', 'हैं', 'इस', 'होता', 'करने', 'ने', 'बनी', 'तो',
             'ही', 'हो','इसका', 'था', 'हुआ', 'वाले', 'बाद', 'लिए', 'सकते', 'इसमें', 'दो', 'वे', 'करते', 'कहा', 'वर्ग', 'कई', 'करें', 'होती', 'अपनी', 'उनके', 'यदि', 'हुई', 'जा', 'कहते',
             'जब', 'होते', 'कोई', 'हुए', 'व', 'जैसे', 'सभी', 'करता', 'उनकी', 'तरह', 'उस', 'आदि', 'इसकी', 'उनका', 'इसी', 'पे', 'तथा', 'भी', 'परंतु', 'इन', 'कम', 'दूर', 'पूरे', 'गये', 
             'तुम', 'मै', 'यहां', 'हुये', 'कभी', 'अथवा', 'गयी', 'प्रति', 'जाता', 'इन्हें', 'गई', 'अब', 'जिसमें', 'लिया', 'बड़ा', 'जाती', 'तब', 'उसे', 'जाते', 'लेकर', 'बड़े', 'दूसरे', 'जाने',
             'बाहर', 'स्थान', 'उन्हें', 'गए', 'ऐसे', 'जिससे', 'समय', 'दोनों', 'किए', 'रहती', 'इनके', 'इनका', 'इनकी', 'सकती', 'आज', 'कल', 'जिन्हें', 'जिन्हों', 'तिन्हें', 'तिन्हों', 'किन्हों', 
             'किन्हें', 'इत्यादि', 'इन्हों', 'उन्हों', 'बिलकुल', 'निहायत', 'इन्हीं', 'उन्हीं', 'जितना', 'दूसरा', 'कितना', 'साबुत', 'वग़ैरह', 'कौनसा', 'लिये', 'दिया', 'जिसे', 'तिसे', 'काफ़ी', 'पहले',
             'बाला', 'मानो', 'अंदर', 'भीतर', 'पूरा', 'सारा', 'उनको', 'वहीं', 'जहाँ', 'जीधर', 'के', 'एवं', 'कुछ', 'कुल', 'रहा', 'जिस', 'जिन', 'तिस', 'तिन', 'कौन', 'किस', 'संग', 'यही',
             'बही', 'उसी', 'मगर', 'कर', 'मे', 'एस', 'उन', 'सो', 'अत' ]
    newHinDict = {}
    for index,hiToken in hinDict.items():
        if hiToken not in stopwords:
            newHinDict.update({index:hiToken})
    return newHinDict
    
#Function to lemmatize
def lemmatize_hi(filtered_hin):                      
    newDict = {}
    keys=list(filtered_hin.keys())
    values=filtered_hin.values()
    string=' '.join(values)
    dochi = nlp_hi(string)
    lemmatized_list = []
    for sent in dochi.sentences:
        for word in sent.words:
            lemmatized_list.append(word.lemma)
    if len(lemmatized_list):
        for i in range(len(values)):
            newDict.update({keys[i]:lemmatized_list[i]})
    return(newDict)

#Function to tag Part of Speech
def postagger_hi(lemmahin):                   
    newDict = {}
    keys=list(lemmahin.keys())
    values=lemmahin.values()
    string=' '.join(values)
    dochi = nlp_hi(string)
    pos_list=[]
    for sent in dochi.sentences:
        for word in sent.words:
            pos_list.append(word.text+'/'+word.upos)
    for i in range(len(values)) :
        newDict.update({keys[i]:pos_list[i]})        
    return(newDict)

#Function to handle negation
def negation_handling_hin(pos_dict):
    newDict = {}
    exclamation = False
    skip = False
    for index,word in pos_dict.items():
        actualWord = word.split("/")[0]
        pos = word.split("/")[1]
        #Check if the word is नहीं
        if actualWord == "नहीं":
            #Do backward negation
            skip = True
            #Get the list of words backwards
            wordsChange = reversed([(x,y) for x,y in newDict.items()])
            for i,w in wordsChange:
                #Get POS Tag
                p = w.split("/")[1]
                #Exclamation is Alive
                newWord = "!" + w
                #Update in the dictionary
                newDict.update({i : newWord})
                if p == 'ADJ' or p == 'NOUN' or p == 'VERB':
                    break
        elif actualWord == "न":
            #Do forward negation
            exclamation = not exclamation
            skip = True
            #Add the exclamation
            word = '!' + word
            #Check if the word is adjective, noun or a verb
            if pos == 'ADJ' or pos == 'NOUN' or pos == 'VERB':
                #Set exclamation to False
                exclamation = False
        if skip == False:
            newDict.update({index : word})
        else:
            skip = False
    return newDict

#Function to determine sentiment
def sentiment(hinDict):
    return HindiSWN.get_scores(list(hinDict.values()))

def script_validation(tokens):
    for word in tokens:
        word = word.strip()
        for ch in word:
            c = ch
            if len(c) == 1:
                if ord(c) not in range(2304,2432):
                    return(0)
    return 1