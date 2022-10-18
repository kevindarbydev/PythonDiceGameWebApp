from flask import Flask, redirect, url_for, render_template, request, session
import random

app = Flask(__name__)

app.secret_key = "hello"
      
@app.route("/index.html", methods=["POST", "GET"])    
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":           
        p1Turn = True
        session["p1t"] = p1Turn
        p1 = str(request.form["playerOne"])
        p2 = str(request.form["playerTwo"])     
        session["p1"] = p1
        session["p2"] = p2     
        session["p1S"] = 0
        session["p2S"] = 0      
        return redirect( url_for("gamePage"))
    else:
        return render_template("index.html")

@app.route('/game', methods=["POST", "GET"])
def gamePage():
 if "p1"  and "p2" and "p1t" in session: 
        p1= session["p1"] 
        p2 =session["p2"] 
        p1Score = session["p1S"]
        p2Score = session["p2S"]
        p1t = session["p1t"]
        return render_template('game.html',p1=p1,p2=p2, p2Score=p2Score,p1Score=p1Score,p1t=p1t)           
 else:
    return render_template('index.html')

@app.route('/roll', methods=["POST", "GET"])
def rollDice():
  if "p1"  and "p2" and  "p1t" in session: 
       p1t = session["p1t"]            
       p1Score = session["p1S"]
       p2Score = session["p2S"]
       p1= session["p1"] 
       p2 =session["p2"]       
       avail_choices = [1,2,3,4,5,6]
       rollOfDie = int(random.choice(avail_choices))  
       
       imgString = "Die" + str(rollOfDie) + ".bmp"      
       if p1t == True:
         if rollOfDie == 1:#resets p1 score to 0 and p1t is now False
            errorMsg = "{p1} rolled a one so your score is reset and your turn is over".format(p1=p1)
            p1Score = 0
            session["p1S"] = p1Score           
            p1t = False
            session["p1t"] = p1t
            return render_template('game.html',p1t=p1t, imgString= imgString,p1=p1,p2=p2,p1Score=p1Score, p2Score= p2Score, errorMsg= errorMsg)
         else:
            successMsg = '{p1} rolled a {x}!'.format(x=rollOfDie,p1=p1)             
            p1Score = p1Score + rollOfDie
            session["p1S"] = p1Score
            if p1Score >= 20:
                return render_template('gameOver.html', msg="success", player = p1)                        
            return render_template('game.html',p1t=p1t, imgString= imgString,p1=p1,p2=p2,p1Score=p1Score,p2Score=p2Score,successMsg=successMsg)
       else:
         if rollOfDie ==1:
            errorMsg = "{p2} rolled a one so your score is reset and your turn is over".format(p2=p2)
            p2Score = 0
            session["p2S"] = p2Score
            p1t = True
            session["p1t"] = p1t
            return render_template('game.html',p1t=p1t, imgString= imgString,p1=p1,p2=p2,p1Score=p1Score, p2Score= p2Score, errorMsg= errorMsg)
         else:
            successMsg = '{p2} rolled a {x}!'.format(x=rollOfDie,p2=p2)       
            p2Score = p2Score + rollOfDie
            session["p2S"] = p2Score
            if p2Score >= 20:
                return render_template('gameOver.html', msg="success", player = p2)            
       return render_template('game.html', imgString= imgString,successMsg=successMsg,p1=p1,p2=p2,p1Score=p1Score,p2Score=p2Score,p1t=p1t)        
  else:        
     return render_template('index.html') 


@app.route('/passturn', methods=["POST", "GET"])
def passTurn():
    if "p1"  and "p2"  and "p1t" and "p1s" and "p2s" in session:         
        p1= session["p1"] 
        p2 =session["p2"] 
        p1Score = session["p1s"] 
        p2Score = session["p2s"]        
        p1t = session["p1t"]
        if p1t == True:
            p1t = False
            session["p1t"] = p1t
        else:
            p1t = True       
            session["p1t"] = p1t             
     
        return render_template('game.html',p1t=p1t, p1=p1,p2=p2,p1Score=p1Score,p2Score=p2Score)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True) 
    
    