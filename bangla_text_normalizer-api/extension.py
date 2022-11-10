from data import * 
from crypt import methods
from flask import Flask, request, render_template, jsonify
import re


def Normalization1():
    if request.method == 'POST':
        text = request.form['text']
    

    pattern = r"(([০-৯]+(লা|রা|ঠা|ই|শে))|(১\/২|১\/৩|১\/৪|১.৫|২.৫|১.২৫|৷৶|৷৵|৷৴|৷|৶|৵|৴|৷৷|৷৷৴|৷৷৵|৳)|([০-৯]+(ম|য়|র্থ|ষ্ঠ|তম)))"
    y = re.findall(pattern,text)
    matched = [x[0] for x in y]
    
    for i in range(len(matched)):
        z = matched[i]
    
        text = text.replace(z, dict1[z])
    
    return text

def Normalization2():
    text = Normalization1()
    splitter = r'(!|,|-|/|:|;|।|–|—|\(|\)|\{|\}|\[|\]|\?|\.|\'|")'
    text_splitted = [y for x in re.split(splitter,text) for y in x.split()]

    lst = []
    for i in range(len(text_splitted)):
        z = text_splitted[i]
    
        if z in dict1:
            lst.append(dict1[z])
        else:
            lst.append(z)
    
    result = ' '.join(lst)
    return result


def num_conversion(z):
    
    if (len(z) == 1):
        return dict[z]
    
    elif (len(z) == 2):
        return dict[z]
    
    elif len(z) == 3:
        if (z[1] == '০' and z[2] == '০'):
            return (dict[z[0]] + "শো")
        else:
            return(dict[z[0]] + "শো " + dict[z[1:]])
        
    elif len(z) == 4:
        if (z[1] == '০' and z[2] == '০' and z[3] == '০'):
            return (dict[z[0]] + " হাজার")
        elif (z[2] == '০' and z[3] == '০'):
            return (dict[z[:2]] + " শো ")
        elif (z[1] == '০' and z[3] == '০'):
            return (dict[z[0]] + " হাজার" + dict[z[2:]])
        elif (z[1] == '০'):
            return (dict[z[0]] + " হাজার " + dict[z[2:]])
        

        else:
            return (dict[z[0]] + " হাজার " + dict[z[1]] + " শো " + dict[z[2:]])
        
    elif len(z) == 5:
        if (z[1] == '০' and z[2] == '০' and z[3] == '০' and z[4] == '০'):
            return (dict[z[:2]]  + " হাজার")
    
        elif (z[2] == '০' and z[3] == '০' and z[4] == '০'):
            return (dict[z[:2]]  + " হাজার")
    
        elif (z[3] == '০' and z[4] == '০'):
            return (dict[z[:2]]  + " হাজার " + dict[z[2]] + "শো")
    
        elif (z[2] == '০'):
            return (dict[z[:2]]  + " হাজার " + dict[z[3:]])
    
        else:
            return (dict[z[:2]] + " হাজার " + dict[z[2]] + "শো " + dict[z[3:]])
    

    elif len(z) == 6:
        if(z[1] == '০' and z[2] == '০' and z[3] == '০' and z[4] == '০' and z[5] == '০'):
            return ((dict[z[0]])  + " লক্ষ")
    
        elif(z[1] == '০' and z[2] == '০' and z[4] == '০' and z[5] == '০'):
            return ((dict[z[0]])  + " লক্ষ" +  dict[z[3]] + " শো " ) 
        
        elif(z[1] == '০' and z[2] == '০' and z[3] == '০'):
            return (dict[z[0]] + " লক্ষ " +  dict[z[4:]]) 
        
        elif(z[1] == '০' and z[3] == '০' and z[4] == '০'):
            return (dict[z[0]]  + " লক্ষ " + dict[z[1:3]]  + " হাজার " + dict[z[4:]])
        
        elif(z[1] == '০' and z[2] == '০'):
            return (dict[z[0]]  + " লক্ষ " + dict[z[3]] + " শো " + dict[z[4:]]) 
        
        elif(z[2] == '০' and z[3] == '০'):
            return (dict[z[0]]  + " লক্ষ " + dict[z[1:3]]  + " হাজার " + dict[z[4:]]) 
        
        elif(z[1] == '০' and z[2] == '০'):
            return (dict[z[0]]  + " লক্ষ " + dict[z[4:]])
        
        else:
            return (dict[z[0]] + " লক্ষ " + dict[z[1:3]]  + " হাজার " + dict[z[3]] + "শো " + dict[z[4:]]) 
        
    elif len(z) == 7:

        if(z[1] == '০' and z[2] == '০' and z[3] == '০' and z[4] == '০' and z[5] == '০' and z[6] == '০'):
            return ((dict[z[:2]])  + " লক্ষ")

        elif(z[1] == '০' and z[2] == '০' and z[3] == '০' and z[4] == '০' and z[5] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + dict[z[5:]])

        elif (z[1] == '০' and z[2] == '০' and z[3] == '০' and z[4] == '০'):
            return (dict[z[:2]] + " লক্ষ " + dict[z[5:]]) 

        elif (z[1] == '০' and z[2] == '০' and z[3] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + dict[z[4]] + "শো "  + dict[z[5:]]) 

        elif(z[2] == '০' and z[3] == '০' and z[4] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + dict[z[5:]])       

        elif(z[2] == '০' and z[4] == '০' and z[5] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + (dict[z[2:4]])  + " হাজার " + dict[z[5:]])   

        elif(z[2] == '০' and z[3] == '০' and z[5] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + dict[z[4]] + "শো " + dict[z[5:]])  

        elif(z[2] == '০' and z[4] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + (dict[z[2:4]])  + " হাজার " + dict[z[5:]]) 

        elif(z[2] == '০' and z[3] == '০'):
            return ((dict[z[:2]])  + " লক্ষ " + dict[z[4]] + "শো " + dict[z[5:]]) 

        elif(z[4] == '০'):
            return (dict[z[:2]] + " লক্ষ " + (dict[z[2:4]])  + " হাজার " + dict[z[5:]]) 

        else:
            return (dict[z[:2]] + " লক্ষ " + (dict[z[2:4]])  + " হাজার " + dict[z[4]] + "শো " + dict[z[5:]]) 
