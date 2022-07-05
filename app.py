from flask import Flask,render_template,session,request,jsonify
import pandas as pd
import numpy as np
import json
import string
import random
app= Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 14))
data = pd.read_excel('captions.xlsx')
captions=data['Caption'].to_numpy()
seq = np.array([i for i in range(10)])
print(captions)
np.random.shuffle(seq)
print(seq)
@app.route("/")
def index():
    return render_template("disc.html")
@app.route('/home',methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        session["qno"]=1
        session['answers']=[]
        inp_path = f"input_{str(seq[session['qno']-1]+1)}.jpg"
        gan_path = f"gan_{str(seq[session['qno']-1]+1)}.jpg"
        grad_path=f"grad_{str(seq[session['qno']-1]+1)}.jpg"
        print(inp_path)
        return render_template("page.html",qno=session["qno"],ino=inp_path,gan_no=gan_path,grad_no=grad_path,caption= captions[seq[session["qno"]-1]])
    else:
        session["qno"]+=1
        session["answers"].append(request.form['Image'])
        
        #return jsonify({"qno":session["qno"], "answers":session["answers"]})
        if session["qno"] == 11:
            N = 7
            res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N))
            f_name="resp/response_"+res+".json"
            dic ={str(i+1):v for i,v in zip(seq,session["answers"])}
            print(dic)
            with open(f_name, 'w') as f:
                json.dump(dic, f)
            return "Thank You! Response has been saved"
        else:
            inp_path = f"input_{str(seq[session['qno']-1]+1)}.jpg"
            gan_path = f"gan_{str(seq[session['qno']-1]+1)}.jpg"
            grad_path=f"grad_{str(seq[session['qno']-1]+1)}.jpg"
            print(inp_path)
            return render_template("page.html",qno=session["qno"],ino=inp_path,gan_no=gan_path,grad_no=grad_path,caption= captions[seq[session["qno"]-1]])

if __name__ =="__main__":
    app.run(debug=True)