from data import * 
from extension import *
from crypt import methods
from flask import Flask, request, render_template, jsonify
import re

app = Flask(__name__)



@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['GET','POST'])




def final_normalization():
    x = Normalization2()
    
    pattern = r"[০-৯]+"
    y = re.findall(pattern, x)

    for i in range(len(y)):
        z = y[i]
    
        x = x.replace(z,  num_conversion(z))
    
    
    return render_template('index.html', text = x)




if __name__ == "__main__":
    app.run(debug=True)