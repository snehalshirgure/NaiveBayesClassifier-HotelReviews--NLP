import re
import operator
import json

f = open("train-labeled.txt", "r", encoding="utf8")

d_all = []

d_posclass = {}
d_negclass = {}
d_fakeclass = {}
d_trueclass = {}

count_pos = 0
count_neg = 0
count_fake = 0
count_true = 0
reviewcount = 0

review_fake = 0
review_true = 0
review_neg = 0
review_pos = 0

if f.mode == 'r':
    fl = f.readlines()
    #for each line
    for a in fl:
        reviewcount += 1
        b = a.split()
        class1 = b[1]
        class2 = b[2]

        if (class1 == 'Fake'):
            review_fake += 1
        if (class1 == 'True'):
            review_true += 1
        if (class2 == 'Neg'):
            review_neg += 1
        if (class2 == 'Pos'):
            review_pos += 1
        #for each word
        for x in range(3, len(b)):

            word = re.sub(r'\W', "", b[x]).lower()
            if word not in d_all:
                d_all.append(word)
             
            if (class1 == 'Fake'):
                if word not in d_fakeclass:
                    d_fakeclass[word] = 1
                else:
                    d_fakeclass[word] += 1
                count_fake += 1
            if (class1 == 'True'):
                if word not in d_trueclass:
                    d_trueclass[word] = 1
                else:
                    d_trueclass[word] += 1
                count_true += 1
            if (class2 == 'Neg'):
                if word not in d_negclass:
                    d_negclass[word] = 1
                else:
                    d_negclass[word] += 1
                count_neg += 1
            if (class2 == 'Pos'):
                if word not in d_posclass:
                    d_posclass[word] = 1
                else:
                    d_posclass[word] += 1
                count_pos += 1

    #sorted_neg = sorted(d_negclass.items(), key=operator.itemgetter(1))
    #sorted_pos = sorted(d_posclass.items(), key=operator.itemgetter(1))
    #sorted_fake = sorted(d_fakeclass.items(), key=operator.itemgetter(1))
    #sorted_true = sorted(d_trueclass.items(), key=operator.itemgetter(1))

    #sorted_y = sorted_x.reverse()

    count_posclass = 0
    count_negclass = 0
    count_fakeclass = 0
    count_trueclass = 0

    for key, value in list(d_posclass.items()):
        if (value>count_pos * 0.07):
            del d_posclass[key]
        else:
            count_posclass += value

    for key, value in list(d_negclass.items()):
        if (value>count_neg * 0.07):
            del d_negclass[key]
        else:
            count_negclass += value

    for key, value in list(d_fakeclass.items()):
        if (value>count_fake * 0.07):
            del d_fakeclass[key]
        else:
            count_fakeclass += value

    for key, value in list(d_trueclass.items()):
        if (value>count_true * 0.07):
            del d_trueclass[key]
        else:
            count_trueclass += value

    count=0
    for word in d_all:
        count+=1
        if word not in d_posclass:
            d_posclass[word]=0
            count_posclass+=1
        if word not in d_negclass:
            d_negclass[word]=0
            count_negclass+=1
        if word not in d_fakeclass:
            d_fakeclass[word]=0
            count_fakeclass+=1
        if word not in d_trueclass:
            d_trueclass[word]=0
            count_trueclass+=1
    
    
    i = 0

    for key in d_posclass:
        d_posclass[key] = (d_posclass[key]  + 1)/(count_posclass)
    for key in d_negclass:
        d_negclass[key] = (d_negclass[key]  + 1)/(count_negclass)
    for key in d_fakeclass:
        d_fakeclass[key] = (d_fakeclass[key]  + 1)/(count_fakeclass)
    for key in d_trueclass:
        d_trueclass[key] = (d_trueclass[key]  + 1)/(count_trueclass)

    d_posclass['prior_prob'] = review_pos / reviewcount
    d_negclass['prior_prob'] = review_neg / reviewcount
    d_fakeclass['prior_prob'] = review_fake / reviewcount
    d_trueclass['prior_prob'] = review_true / reviewcount

    d_posclass['unknown_prob'] = 1 / count_posclass
    d_negclass['unknown_prob'] = 1 / count_negclass
    d_fakeclass['unknown_prob'] = 1 / count_fakeclass
    d_trueclass['unknown_prob'] = 1 / count_trueclass

    data_list = {
        "pos_classifier": d_posclass,
        "neg_classifier": d_negclass,
        "fake_classifier": d_fakeclass,
        "true_classifier": d_trueclass
    }

    #print(str(d_negclass['prior_prob']))
    f2 = open("nbmodel.txt", "w+", encoding="utf8")

    data = json.dumps(data_list, ensure_ascii=False)
    f2.write(data)