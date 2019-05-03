from flask import Flask, flash , redirect, render_template , request, session, abort , Markup
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from time import sleep
import pyeeg
import pickle
# import warnings
from werkzeug import secure_filename
import os


from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB



app = Flask(__name__)

app.secret_key = os.urandom(12)

final_ans_g = list()
length_g=0
name_g=""


def seizures():

	names = ["Nearest Neighbors", "SVM","Decision Tree", "Random Forest", "AdaBoost","Naive Bayes"]
	classifiers = [
    KNeighborsClassifier(3),
    SVC(C=1),
    DecisionTreeClassifier(max_depth=3),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=4),
    AdaBoostClassifier(),
    GaussianNB()]

	clf_score = []
	X_test=pickle.load(open("X_TEST.txt","rb"))
	# f=open("X_TEST.txt","r")
	# X_test=pd.read_fwf("X_TEST.txt")
	# print("1111111111111111111111111111111")
	# print(X_test,"============================")
	# print("2222222222222222222222222222222222")
	# ans = pickle.load(open("Random Forest.h5",'rb'))
	# NN=pickle.load(open("Nearest Neighbors.h5",'rb'))
	final_ans=[]
	for i in names:
		model=pickle.load(open(i+".h5",'rb'))
		ans=model.predict(X_test)
		final_ans.append(ans)
		print(f"***********************{i}***********************")
		print(ans)
		print(f"Total Healthy : {sum([1 if i==1 else 0 for i in ans])}")
		print(f"Total Transition : {sum([1 if i==0 else 0 for i in ans])}")
		print(f"Total Epileptic : {sum([1 if i==-1 else 0 for i in ans])}")
		length=len(ans)
	return length,final_ans	








@app.route("/",methods=['GET','POST'])
def home():
	# seizures()
	# if request.methods=="POST"
	# print(request.form)
	# print(request.form['name'])
	return render_template("index.html")


@app.route("/sec",methods=['GET','POST'])
def sec():
	print("========================")
	print(request.form)
	print("dfdg")
	# print(request.files['file1'])
	session['name'] = request.form['name']
	global name_g 
	name_g=request.form['name']
	print(request.files)
	print("sd")
	# print(request.form['file'])	
	f = request.files['file']
	f.save(secure_filename("X_TEST.txt"))
	# print("f",f)

	# print(request.files["file1"])
	# print(request.files['file'])
	length,final_ans=seizures()
	print("end")
	# return "sdfsd"
	global final_ans_g
	final_ans_g=final_ans
	global length_g
	length_g=length
	# session['final_ans']=final_ans
	session['length']=length
	return render_template("dashboard.html",length=length,NN=final_ans[0],SVM=final_ans[1],DT=final_ans[2],RF=final_ans[3],AB=final_ans[4],NB=final_ans[5],
	NN_h=sum([1 if i==1 else 0 for i in final_ans[0]]),
	NN_t=sum([1 if i==0 else 0 for i in final_ans[0]]),
	NN_e=sum([1 if i==-1 else 0 for i in final_ans[0]]),
	SVM_h=sum([1 if i==1 else 0 for i in final_ans[1]]),
	SVM_t=sum([1 if i==0 else 0 for i in final_ans[1]]),
	SVM_e=sum([1 if i==-1 else 0 for i in final_ans[1]]),
	DT_h=sum([1 if i==1 else 0 for i in final_ans[2]]),
	DT_t=sum([1 if i==0 else 0 for i in final_ans[2]]),
	DT_e=sum([1 if i==-1 else 0 for i in final_ans[2]]),
	RF_h=sum([1 if i==1 else 0 for i in final_ans[3]]),
	RF_t=sum([1 if i==0 else 0 for i in final_ans[3]]),
	RF_e=sum([1 if i==-1 else 0 for i in final_ans[3]]),
	AB_h=sum([1 if i==1 else 0 for i in final_ans[4]]),
	AB_t=sum([1 if i==0 else 0 for i in final_ans[4]]),
	AB_e=sum([1 if i==-1 else 0 for i in final_ans[4]]),
	NB_h=sum([1 if i==1 else 0 for i in final_ans[5]]),
	NB_t=sum([1 if i==0 else 0 for i in final_ans[5]]),
	NB_e=sum([1 if i==-1 else 0 for i in final_ans[5]]),
	name=name_g)


@app.route("/NN",methods=['GET','POST'])
def NN():
	# final_ans=session["final_ans"]
	# length=session["length"]
	final_ans=final_ans_g
	length=length_g
	return render_template("NN.html",length=length,NN=final_ans[0],NN_h=sum([1 if i==1 else 0 for i in final_ans[0]]),
	NN_t=sum([1 if i==0 else 0 for i in final_ans[0]]),
	NN_e=sum([1 if i==-1 else 0 for i in final_ans[0]]),
	name=name_g)

@app.route("/SVM",methods=['GET','POST'])
def SVM():
	# final_ans=session["final_ans"]
	# length=session["length"]
	final_ans=final_ans_g
	length=length_g
	return render_template("SVM.html",length=length,SVM=final_ans[1],SVM_h=sum([1 if i==1 else 0 for i in final_ans[1]]),
	SVM_t=sum([1 if i==0 else 0 for i in final_ans[1]]),
	SVM_e=sum([1 if i==-1 else 0 for i in final_ans[1]]),
	name=name_g)


@app.route("/DT",methods=['GET','POST'])
def DT():
	# final_ans=session["final_ans"]
	# length=session["length"]
	final_ans=final_ans_g
	length=length_g
	return render_template("DT.html",length=length,DT=final_ans[2],DT_h=sum([1 if i==1 else 0 for i in final_ans[2]]),
	DT_t=sum([1 if i==0 else 0 for i in final_ans[2]]),
	DT_e=sum([1 if i==-1 else 0 for i in final_ans[2]]),
	name=name_g)


@app.route("/RF",methods=['GET','POST'])
def RF():
	# final_ans=session["final_ans"]
	# length=session["length"]
	final_ans=final_ans_g
	length=length_g
	return render_template("RF.html",length=length,RF=final_ans[3],RF_h=sum([1 if i==1 else 0 for i in final_ans[3]]),
	RF_t=sum([1 if i==0 else 0 for i in final_ans[3]]),
	RF_e=sum([1 if i==-1 else 0 for i in final_ans[3]]),
	name=name_g)


@app.route("/AB",methods=['GET','POST'])
def AB():
	# final_ans=session["final_ans"]
	# length=session["length"]
	final_ans=final_ans_g
	length=length_g
	return render_template("AB.html",length=length,AB=final_ans[4],AB_h=sum([1 if i==1 else 0 for i in final_ans[4]]),
	AB_t=sum([1 if i==0 else 0 for i in final_ans[4]]),
	AB_e=sum([1 if i==-1 else 0 for i in final_ans[4]]),
	name=name_g)


@app.route("/NB",methods=['GET','POST'])
def NB():
	# final_ans=session["final_ans"]
	# length=session["length"]
	final_ans=final_ans_g
	length=length_g
	return render_template("NB.html",length=length,NB=final_ans[5],NB_h=sum([1 if i==1 else 0 for i in final_ans[5]]),
	NB_t=sum([1 if i==0 else 0 for i in final_ans[5]]),
	NB_e=sum([1 if i==-1 else 0 for i in final_ans[5]]),
	name=name_g)


@app.route("/user",methods=['GET','POST'])
def usr():
	# final_ans=session["final_ans"]
	# length=session["length"]
	# final_ans=final_ans_g
	# length=length_g
	return render_template("user.html", name=name_g)





if __name__ == "__main__":

    app.run()