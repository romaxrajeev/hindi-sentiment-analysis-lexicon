import pandas as pd
hi_SWN = pd.read_csv("D:\CodeMix\hinSWN.csv", sep=",")
length = hi_SWN[hi_SWN.columns[0]].count()

tagsDict = {
    "ADJ" : "a",
    "NOUN" : "n",
    "ADV" : "r",
    "VERB" : "v"
}

def get_pos_tag(cols):
    return cols[0]

def get_words(cols):
    words = cols[4].split(",")
    return words

def get_positive(cols):
    return cols[2]

def get_negative(cols):
    return cols[3]

def get_objective(cols):
    return 1 - (float(cols[2]) + float(cols[3]))

def get_scores(sentiword):
    res = 0
    wordList = {}
    count = 0
    score = 0.0
    for i in range(length):
        cols = hi_SWN.iloc[i]
        words = get_words(cols)
        pos = get_pos_tag(cols)
        for word in sentiword:
                negate = False
                if word[0] == '!':
                    negate = True
                    actualWord = word[1:]
                else:
                    actualWord = word
                actualWordW,tagWord = actualWord.split("/")[0], actualWord.split("/")[1]
                if tagWord == "ADJ" or tagWord == "ADV" or tagWord == "VERB" or tagWord == "NOUN":
                    tag = tagsDict[tagWord]
                    if actualWordW in words and pos == tag:
                        if not negate:
                            res += float(get_positive(cols)) - float(get_negative(cols))
                        else:
                            res += (float(get_positive(cols)) - float(get_negative(cols))) * -1
                        count = count + 1
                        if actualWordW in wordList.keys():
                            wordList.update({actualWordW : wordList[actualWordW] + float(get_positive(cols)) - float(get_negative(cols))})
                        else:
                            wordList.update({actualWordW : float(get_positive(cols)) - float(get_negative(cols))})
    if len(wordList.keys()) > 0:
        score = res / len(wordList.keys())
    if score > 0:
        return ("Positive",score)
    elif res < 0:
        return ("Negative",score)
    return ("Neutral",score)