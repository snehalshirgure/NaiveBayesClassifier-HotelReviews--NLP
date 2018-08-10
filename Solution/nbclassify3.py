import json
import math

def main():   
    
    f1 = open("nbmodel.txt", "r" , encoding="utf-8")
    f2 = open("dev-text.txt", "r", encoding="utf-8")
    f3 = open("nboutput.txt", "w+" , encoding="utf-8")

    d_posclass = {}
    d_negclass = {}
    d_fakeclass = {}
    d_trueclass = {}

    if f1.mode=="r":
        ff = f1.readlines()
        for lines in ff:
            jsonfile = json.loads(lines,encoding="utf-8")
            d_posclass = jsonfile["pos_classifier"]
            d_negclass = jsonfile["neg_classifier"]
            d_fakeclass = jsonfile["fake_classifier"]
            d_trueclass = jsonfile["true_classifier"]

    taglist = {}

    if f2.mode=="r":
        fl = f2.readlines()
        
        #for each line
        for line in fl:
            
            count_pos=0
            count_neg=0
            count_fake=0
            count_true=0

            a = line.split()
            reviewid = a[0]

            pos_prob = d_posclass['prior_prob']
            neg_prob= d_negclass['prior_prob']
            fake_prob = d_fakeclass['prior_prob']
            true_prob = d_trueclass['prior_prob']
            
            #for each word
            for x in range(1,len(a)):
                word = re.sub(r'\W', "", a[x]).lower()

                if word in d_posclass :
                    pos_prob += math.log(d_posclass[word])
                else:
                    pos_prob += math.log(d_posclass['unknown_prob'])

                if word in d_negclass :
                    neg_prob += math.log(d_negclass[word])
                else:
                    neg_prob += math.log(d_negclass['unknown_prob'])

                if word in d_fakeclass :
                    fake_prob += math.log(d_fakeclass[word])
                else:
                    fake_prob += math.log(d_fakeclass['unknown_prob'])
                  
                if word in d_trueclass :
                    true_prob += math.log(d_trueclass[word])   
                else:
                    true_prob += math.log(d_trueclass['unknown_prob'])  

                       

            if(pos_prob>neg_prob):
                count_pos=1
            else:
                count_neg=1
            
            if(fake_prob>true_prob):
                count_fake=1
            else:
                count_true=1  

            #print(str(count_fake)+ "  " + str(count_true))
            #print(str(count_pos)+ " " +str(count_neg))
            if(count_pos>count_neg):
                if(count_fake>count_true):
                    taglist[reviewid] ={'POS','FAKE'}
                    f3.write(str(reviewid)+" Fake Pos\n")
                else:
                    taglist[reviewid] ={'POS','TRUE'}
                    f3.write(str(reviewid)+" True Pos\n")
            else:
                if(count_fake>count_true):
                    taglist[reviewid] ={'NEG','FAKE'}
                    f3.write(str(reviewid)+" Fake Neg\n")
                else:
                    taglist[reviewid] ={'NEG','TRUE'}
                    f3.write(str(reviewid)+" True Neg\n")


if  __name__ ==  "__main__":
    main()           
            
