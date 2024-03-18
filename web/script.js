// Onclick of the button 
const form = document.querySelector("form");
form.addEventListener("submit", (e) => {   
    e.preventDefault("llm-chat-message");

    const formData = new FormData(form);
    const message = formData.get("llm-chat-message")

    // Call python's random_python function 
    eel.sendMessage(message)(function(newMessage){                       
      // Update the div with a random number returned by python 
      document.querySelector("#llm-chat").innerHTML += `</p>${newMessage}</p>`; 
    }) 
    
  });