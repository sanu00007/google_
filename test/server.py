import os
import time
import pyaudio
import speech_recognition as sr
import playsound 
from gtts import gTTS
import openai
import uuid
from flask import Flask, render_template

app = Flask(__name__)

# ... (other code remains the same)

guy = ""  # Initialize the global variable here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio', methods=['GET'])
def get_audio():
    global guy  # Use the global variable within the function
    while True:
        try:
            get_audio_from_mic()
            
            if "stop" in guy:
                break
            else:
                return guy
        except Exception as e:
            return str(e)
    return "Recording Stopped!"

def get_audio_from_mic():
    global guy  # Use the global variable within the function
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)  # Optional: Keep the print statement for debugging purposes
            guy = said

            if "Google" in said:
                new_string = said.replace("Google", "")
                new_string = new_string.strip()
                print(new_string) 
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": said}])
                text = completion.choices[0].message.content
                displayRecognizedText(text)  # Call the JavaScript function to update the webpage
                speech = gTTS(text=text, lang='en', slow=False, tld="com.au")
                file_name = f"welcome_{str(uuid.uuid4())}.mp3"
                speech.save(file_name)
                playsound.playsound(file_name, block=False)
        except Exception as e:
            print("Audio not clear!!!")

if __name__ == '__main__':
    app.run(debug=True)
