import eel 
from random import randint 
  
eel.init("web")   
  
# Exposing the random_python function to javascript 
@eel.expose     
def sendMessage(message): 
    print("test3")
    return f"-->{message}"
  
# Start the index.html file 
eel.start("index.html")