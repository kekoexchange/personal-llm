import eel   
eel.init("web")   
  
# Exposing the "send message" function to javascript
@eel.expose     
def sendMessage(message): 
    print(f"executing sendMessage function with ${message}")
    return f"from python-->{message}"
  
# Start the index.html file 
eel.start("index.html")