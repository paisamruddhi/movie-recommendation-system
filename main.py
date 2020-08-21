from flask import render_template,Flask,request
import combined

app=Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')
@app.route("/recommend",methods=['POST'])
def recommend():
    data=str(request.form['fname'])
    data=data.lower()
    data=data.split()
    temp=""
    for i in data:
        temp=temp+i.capitalize()+" "
    data=temp.strip()
    d1=combined.content_based_recomendation(data)
    d2=combined.ratings_based_recomendation(data)
    if d1==0 and d2==0:
        tag='false'
    else:
        tag='true'
    return render_template('recommend.html',data1=d1,data2=d2,name=data,t=tag)

if __name__=="__main__":
    app.run()

