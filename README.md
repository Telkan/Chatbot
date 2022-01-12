# Chatbot

Voice controlled Chatbot interacting with various communications mediums.

To start all parts of this program you start the rasa chatbot first:

p.s. if you need conda env then this first:
```conda activate rasa2_2021```

then to start rasa servers
```cd Code```
```rasa run actions```
and in a new terminal at the same location:
```rasa run```

To start the alexa server, first go to the backend folder
```cd backend```

then run it using ngrok:
```ngrok http 5000```

the forwarding adress provided by the alexa server has to be set for the alexa.
example adress generated: https://d03b-185-219-140-212.ngrok.io 

finally to test the application, from the head directory, run the Main.py script.


