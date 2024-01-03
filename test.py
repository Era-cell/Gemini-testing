import pathlib

import cv2
import speech_recognition as sr
import webbrowser
import pyttsx3
import win32com.client
import google.ai.generativelanguage as glm
from pathlib import Path
import google.generativeai as genai

import PIL.Image

from PIL import Image

cap = cv2.VideoCapture(1)

cap.set(3, 640)
cap.set(4, 480)

cap.set(10, 100)

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

GOOGLE_API_KEY = "AIzaSyDSWFC0WIA4r7howth4K4MQccyqnjtLK24"
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

model = genai.GenerativeModel(model_name="gemini-pro-vision")

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def from_gemini(count, prompt):
    res = model.generate_content([prompt, PIL.Image.open(f"image{count}.jpg")], stream=True)

    # image_parts = [
    #     {
    #         "mime_type": "image/jpeg",
    #         "data": img.read_bytes()
    #     },
    # ]
    #
    # prompt_parts = [
    #     prompt,
    #     image_parts[0],
    # ]
    #
    # res = model.generate_content(
    #     glm.Content(
    #         parts=[
    #             glm.Part(text="Write a short, engaging blog post based on this picture."),
    #             glm.Part(
    #                 inline_data=glm.Blob(
    #                     mime_type='image/jpeg',
    #                     data=pathlib.Path('image.jpg').read_bytes()
    #                 )
    #             ),
    #         ],
    #     ),
    #     stream=True)
    res.resolve()
    print(res.text)
    return res.text


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(e)
            return "Try again"



while True:
    query = takeCommand().lower()
    success, img = cap.read()
    if "Hey".lower() in query:
        count = len(list(Path().glob('image*.jpg')))
        cv2.imwrite(f"image{count}.jpg", img)

        print(query)
        response = from_gemini(count, query)
        speaker.Speak(response)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.imshow("Image", img)
