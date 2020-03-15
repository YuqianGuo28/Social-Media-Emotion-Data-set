# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:03:26 2020

@author: Daisy
"""
import re
import pandas as pd
import csv

happy_active_words = ["astonished","excited","excitement","happy","delighted","glad","amused","pleased"]
happy_inactive_words = ["content","satisfied","as ease","calm","relaxed","serene","sleepy","tired"]
unhappy_active_words = ["afraid","angry","alarmed","tense","frustrated","annoyed","distressed"]
unhappy_inactive_words = ["miserable","sad","depressed","gloomy","bored","droopy"]
sadness_emoji = [">:[",":-(",":(",":-C",":C",":-<",":<",":-[",":[",":{"]
anger_emoji = [":-||",":@>",":("]
happy_emoji = [":)",";)","=)",":]",":P",":-P",";P",":D",";D",":>",":3",":-)",";-)",":^)",":o)",";^)",":-D",":->"]
surprise_emoji = [":-o",":-O","o_O","O_o"]
disgust_emoji = ["D:<","D:","D8","D;","D=","DX","v.v"]
FILE_NAME = ["excitement_tweet1.json","happy_tweet1.json","pleasant_tweet1.json","sad_tweet1.json","fear_tweet1.json","angry_tweet1.json"]  # file name to save
emotions=[["excitement","excited","astonished"],["happy","joy","love"],["pleasant","delighted","glad","pleased"],["down","sad","frustration","depressed","gloomy","depression"],["fear","disgust"],["angry","anger","annoyed"]]
with open("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt",encoding="utf-8") as fo:
        t = fo.readlines()
        anger_list=[]
        fear_list=[]
        happy_list=[]
        sad_list=[]
        excitement_list=[]
        pleasant_list=[]
        for i in range(0,len(t)):
            t[i] = t[i].split()
            if "anger" in t[i] and t[i][2] == "1":
                anger_list.append(t[i][0])
            elif "disgust" in t[i] and t[i][2] == "1":
                fear_list.append(t[i][0])
            elif "fear" in t[i] and t[i][2] == "1":
                fear_list.append(t[i][0])
            elif "joy" in t[i] and t[i][2] == "1":
                happy_list.append(t[i][0])
            elif "sadness" in t[i] and t[i][2] == "1":
                sad_list.append(t[i][0])
            elif "surprise" in t[i] and t[i][2] == "1":
                excitement_list.append(t[i][0])
            elif "positive" in t[i] and t[i][2] == "1":
                pleasant_list.append(t[i][0])
        fo.close()
        
def replacer(text):
    replacement_patterns = [
                (r'won\'t', 'will not'),
                (r'can\'t', 'cannot'),
                (r'I\'m', 'I am'),
                (r'i\'m', 'i am'),
                (r'ain\'t', 'is not'),
                (r'(\w+)\'ll', r'\g<1> will'),
                (r'(\w+)n\'t', r'\g<1> not'),
                (r'(\w+)\'ve', r'\g<1> have'),
                (r'(\w+)\'s', r'\g<1> is'),
                (r'(\w+)\'re', r'\g<1> are'),
                (r'(\w+)\'d', r'\g<1> would')]
    patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]
    s = text
    for (pattern, repl) in patterns:
        (s, _) = re.subn(pattern, repl, s)
    return s
    
class tweetCleaner(object):
    def get_words_after_flag(self, flag):
        """
        function：get the words after flag
        input: flag='#' represents hashtag，flag='@'represents user_metioned
        output: the word list after flag
        """
        list = []
        i = 0
        end = 0
        while (i < len(self.text)):
            if self.text[i:i + 1] == flag:
                i += 1
                if (i > len(self.text) - 1):
                    break
                start = i
                if self.text[i] == ' ':
                    start += 1
                    while (self.text[i].isalpha() or self.text[i] == ' ' or self.text[i] == '\''):
                        if (i == len(self.text) - 1):
                            break
                        i += 1
                        end = i
                    temp = self.text[start: end].split(' ')
                    for item in temp:
                        if item.isalpha():
                            list.append(item.lower())
                else:
                    while (self.text[i].isalpha()):
                        if (i == len(self.text) - 1):
                            break
                        i += 1
                        end = i
                    list.append(self.text[start: end].lower())
            i += 1
        return list

    def hashtag(self):
        return self.get_words_after_flag('#')


    def user_mentioned(self):
        return self.get_words_after_flag('@')
    
    
    def url(self):
        i = self.text.find("https")
        return self.text[i:], i
    
    def words(self):
        length = len(self.text)
        newText = ""  
        for i in range(length):
            if (self.text[i].isalpha() or self.text[i].isdigit() or self.text[i] == '\''):
                newText += self.text[i]
            elif (self.text[-1] != ' '):
                newText += ' '
        return newText.lower()  
        
    def cleaner(self, text):
        self.text = text
        url, i = self.url()
        self.text = self.text[:i - 1]
        words = self.words()  
        hashtag = self.hashtag()  
        userMentioned = self.user_mentioned()  
        return {"label":"","words": words, "hashtag": hashtag, "@": userMentioned, "url": url}
    

#tweers2.csv is the file where stores the tweets I crawled using api 
with open("tweets2.csv",encoding="utf-8") as fs:
    m = list(csv.reader(fs))
    url_reg  = r'[a-z]*[:.]+\S+'
    for i in range(0,len(m)):
        m[i][1] = re.sub('\$%&*\d|\'s|\'', '', m[i][1]) #delete speacial characters
        m[i][1] = re.sub(url_reg, '', m[i][1])#delete the url in the tweet
        m[i][1] = re.sub(r'&amp;',"&",m[i][1])#replace the &amp; in the text with &
        m[i][1] = replacer(m[i][1])#extend abbreviation
    fs.close()
    
with open("clean_test2.csv","a", encoding="utf-8",newline='' "") as fw:
    csv_writer = csv.writer(fw)
    csv_writer.writerow(["user_ID","tweet","creation time"])
    for i in range(1,len(m)):
        for j in range(0,len(m[i][1])):
            if m[i][1][j:j+1] in sadness_emoji: #delete the ambiguous tweets by emoji
                m[i][1] = None
            elif t[i][1][j:j+2] in sadness_emoji:
                m[i][1] = None
        csv_writer.writerow([m[i][0],m[i][1],m[i][2]])
    fw.close()
    

  
if __name__ == '__main__':
    with open("tweets2.csv",encoding="utf-8") as fo:
        t = list(csv.reader(fo))
        url_reg  = r'[a-z]*[:.]+\S+'
        for i in range(0,len(t)):
            t[i][1] = re.sub('\$%&*\d|\'s|\'', '', t[i][1]) #delete speacial characters
            t[i][1] = re.sub(url_reg, '', t[i][1])#delete the url in the tweet
            t[i][1] = re.sub(r'&amp;',"&",t[i][1])#replace the &amp; in the text with &
            t[i][1] = replacer(t[i][1])
        obj = tweetCleaner()
        word_list={}
        final_list={}
        
        zero = len(t)
        word_count_anger = [0]*zero
        word_count_fear = [0]*zero
        word_count_happy = [0]*zero
        word_count_sad = [0]*zero
        word_count_excitement = [0]*zero
        word_count_pleasant = [0]*zero
        
        for i in range(1,len(t)):
            word_list[i] = obj.cleaner(t[i][1])
            #find emotion words from hashtags
            if word_list[i]["hashtag"]:
                for j in word_list[i]["hashtag"]:
                    if j in emotions[5]:
                        word_count_anger[i] += 1
                    elif j in emotions[4]:
                        word_count_fear[i] += 1
                    elif j in emotions[1]:
                        word_count_happy[i] +=1    
                    elif j in emotions[3]:
                        word_count_sad[i] +=1
                    elif j in emotions[0]:
                        word_count_excitement[i] +=1  
                    elif j in emotions[2]:
                        word_count_pleasant[i] +=1
                    elif j in anger_list:
                        word_count_anger[i] += 1
                    elif j in fear_list:
                        word_count_fear[i] += 1
                    elif j in happy_list:
                        word_count_happy[i] +=1
                    elif j in sad_list:
                        word_count_sad[i] +=1
                    elif j in excitement_list:
                        word_count_excitement[i] +=1
                    elif j in pleasant_list:
                        word_count_pleasant[i] +=1
                    else:
                        pass
                if(word_count_anger[i] or word_count_fear[i] or word_count_happy[i] or word_count_sad[i] or word_count_excitement[i] or word_count_pleasant[i])>0:
                    c = [word_count_anger[i],word_count_fear[i],word_count_happy[i],word_count_sad[i],word_count_excitement[i],word_count_pleasant[i]]
                    which_max = c.index(max(c))
                    max_count = c.count(max(c))
                    if max_count == 1:
                        word_list[i]["label"] = ["anger","fear","happy","sad","excitement","pleasant"][which_max]
                        final_list[i]=[t[i][0],t[i][1],word_list[i]["label"],word_list[i]["words"],word_list[i]["hashtag"],word_list[i]["@"],t[i][2]]
                    else:
                        for w in word_list[i]["words"].split(' '):
		                # count if it is a positive word
                            if w in anger_list:
                                word_count_anger[i] += 1
                            elif w in fear_list:
                                word_count_fear[i] += 1
                            elif w in happy_list:
                                word_count_happy[i] +=1
                            elif w in sad_list:
                                word_count_sad[i] +=1
                            elif w in excitement_list:
                                word_count_excitement[i] +=1
                            elif w in pleasant_list:
                                word_count_pleasant[i] +=1
                            else:
                                pass
                        if(word_count_anger[i] or word_count_fear[i] or word_count_happy[i] or word_count_sad[i] or word_count_excitement[i] or word_count_pleasant[i])>0:
                            c = [word_count_anger[i],word_count_fear[i],word_count_happy[i],word_count_sad[i],word_count_excitement[i],word_count_pleasant[i]]
                            which_max = c.index(max(c))
                            word_list[i]["label"] = ["anger","fear","happy","sad","excitement","pleasant"][which_max]
                            final_list[i]=[t[i][0],t[i][1],word_list[i]["label"],word_list[i]["words"],word_list[i]["hashtag"],word_list[i]["@"],t[i][2]]
                else:
                    pass
            #find emotion words from text if there is no hashtag
            else:
                for j in word_list[i]["words"].split(' '):
		        # count if it is a positive word
                    if j in anger_list:
                        word_count_anger[i] += 1
                    elif j in fear_list:
                        word_count_fear[i] += 1
                    elif j in happy_list:
                        word_count_happy[i] +=1
                    elif j in sad_list:
                        word_count_sad[i] +=1
                    elif j in excitement_list:
                        word_count_excitement[i] +=1
                    elif j in pleasant_list:
                        word_count_pleasant[i] +=1
                    else:
                        pass
                if(word_count_anger[i] or word_count_fear[i] or word_count_happy[i] or word_count_sad[i] or word_count_excitement[i] or word_count_pleasant[i])>0:
                    c = [word_count_anger[i],word_count_fear[i],word_count_happy[i],word_count_sad[i],word_count_excitement[i],word_count_pleasant[i]]
                    which_max = c.index(max(c))
                    word_list[i]["label"] = ["anger","fear","happy","sad","excitement","pleasant"][which_max]
                    final_list[i]=[t[i][0],t[i][1],word_list[i]["label"],word_list[i]["words"],word_list[i]["hashtag"],word_list[i]["@"],word_list[i],t[i][2]]
                else:
                    pass
            print(word_count_anger[i],word_count_fear[i],word_count_happy[i],word_count_sad[i],word_count_excitement[i],word_count_pleasant[i])
        print(final_list)
        fo.close()
  

            
    with open("sad_word_list.csv", "a", encoding = "utf-8",newline='' "") as fm:
        csv_writer = csv.writer(fm)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="sad":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in happy_active_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        fm.close()
        
    with open("happy_word_list.csv","a",encoding = "utf-8",newline='' "") as fa:
        csv_writer = csv.writer(fa)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="happy":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in unhappy_inactive_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        fa.close()

    with open("happy_word_list.json", "a", encoding = "utf-8") as fu:
        csv_writer = csv.writer(fu)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="happy":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in unhappy_inactive_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        fu.close()
        
    with open("anger_word_list.csv","a",encoding = "utf-8",newline='' "") as fd:
        csv_writer = csv.writer(fd)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="anger":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in happy_inactive_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        fd.close()   

    with open("fear_word_list.csv","a",encoding = "utf-8",newline='' "") as fs:
        csv_writer = csv.writer(fs)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="fear":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in happy_active_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        fs.close()

    with open("excitement_word_list.csv","a",encoding = "utf-8",newline='' "") as ft:
        csv_writer = csv.writer(ft)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="excitement":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in unhappy_inactive_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        ft.close()

    with open("pleasant_word_list.csv","a",encoding = "utf-8",newline='' "") as fh:
        csv_writer = csv.writer(fh)
        csv_writer.writerow(["user_ID","rough clean text","label","clean words","hashtag","@","creation time"])
        for i in range(1,len(t)):
            if word_list[i]["label"]=="pleasant":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in unhappy_active_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        csv_writer.writerow(final_list[i])
                else:
                    csv_writer.writerow(final_list[i])
            else:
                pass
        fh.close()
        
    with open("pleasant_word_list.json", "a", encoding = "utf-8") as fu:
        for i in range(1,len(t)):
            if word_list[i]["label"]=="pleasant":
                if word_list[i]["hashtag"]:
                    if word_list[i]["hashtag"][-1] in unhappy_active_words:  #delete the ambiguous tweets by hashtag
                        pass
                    else:
                        fu.write(str(word_list[i])+"\n")
                else:
                    fu.write(str(word_list[i])+"\n")
            else:
                pass
        fu.close()