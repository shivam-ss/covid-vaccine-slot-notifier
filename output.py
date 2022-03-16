#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask, request
from vaccine import show_availability


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    errors = ""
    state =""
    district =""
    if request.method == "POST":
        state = request.form["number1"]
        district = request.form["number2"]
        choice = request.form['choice']
        email = request.form['email']
        
        if state !=None:
            result = show_availability(state , district, int(choice) , email)
            return '''
                    <html>
                        <body>
                            <p> Thanks. </p>
                            <p>You will receive an email when slot is available,  </p>
                            <p><a href="/">Click here to get new alerts</a>
                        </body>
                    </html>
            '''.format(result=result)

        
        
    return '''
        <html>
            <body>
                <h1 style="background-color: red;" style="font-family:verdana;"> <p> COWIN AVAILABILITY CHECKER </p> </h1> 
                <form method="post" action=".">
                    <p> Enter State:  <input name="number1" /></p>
                    <p> Enter District : <input name="number2" /></p>
                    <p> Choice: 1 for 18+ , 2 for all] <input name="choice" /> </p>
                    <p> Enter email for receiving alert [gmail only] <input name="email" /> </p>
                    <p><input type="submit" value="Check Availability" /></p>
                </form>
            </body>
        </html>
    '''


if __name__ == "__main__":
    app.run()


# In[ ]:




