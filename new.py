import os
import sys
import requests
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pyautogui
import pyjokes
import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup

# ------------------ Auto-Update Feature ------------------
UPDATE_URL = "https://raw.githubusercontent.com/YourGitHubUsername/YourRepo/main/assistant.py"  # Change to your repo
VERSION_URL = "https://raw.githubusercontent.com/YourGitHubUsername/YourRepo/main/version.txt"  # Version file

CURRENT_VERSION = "1.0"

def check_for_updates():
    try:
        response = requests.get(VERSION_URL)
        latest_version = response.text.strip()

        if latest_version != CURRENT_VERSION:
            print("⚡ New update available! Downloading now...")
            update_script()
        else:
            print("✅ You have the latest version.")
    except Exception as e:
        print("⚠️ Update check failed:", e)

def update_script():
    try:
        response = requests.get(UPDATE_URL)
        new_code = response.text

        with open(sys.argv[0], "w", encoding="utf-8") as file:
            file.write(new_code)

        print("✅ Update successful! Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print("⚠️ Update failed:", e)

# ------------------ Text-to-Speech Initialization ------------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# ------------------ Command Recognition ------------------
def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Processing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You just said: {query}\n")
    except Exception as e:
        print(e)
        speak("Please say that again.")
        query = "none"
    return query.lower()

# ------------------ Wishing User ------------------
def wishings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning, Boss")
        speak("Good Morning, Boss")
    elif hour >= 12 and hour < 17:
        print("Good Afternoon, Boss")
        speak("Good Afternoon, Boss")
    elif hour >= 17 and hour < 21:
        print("Good Evening, Boss")
        speak("Good Evening, Boss")
    else:
        print("Good Night, Boss")
        speak("Good Night, Boss")

# ------------------ Wikipedia Search ------------------
def search_wikipedia(query):
    speak("Searching in Wikipedia...")
    try:
        results = wikipedia.summary(query, sentences=1)
        speak("According to Wikipedia...")
        print(results)
        speak(results)
    except Exception as e:
        print("No results found.")
        speak("No results found.")

# ------------------ Google Search ------------------
def search_google(query):
    print(f"Searching Google for: {query}")
    query_string = "+".join(query.split())
    url = f"https://www.google.com/search?q={query_string}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("div", class_="tF2Cxc"):
        title = result.find("h3").text if result.find("h3") else "No Title"
        link = result.find("a")["href"] if result.find("a") else "No Link"
        snippet = result.find("span", class_="aCOpRe").text if result.find("span", class_="aCOpRe") else "No Snippet"
        results.append({"title": title, "link": link, "snippet": snippet})

    return results

def display_results(results):
    if not results:
        print("No results found.")
        return

    print("\nTop Google Search Results:\n")
    for idx, result in enumerate(results[:5], start=1):
        print(f"{idx}. {result['title']}")
        print(f"   Link: {result['link']}")
        print(f"   Snippet: {result['snippet']}\n")

    print("Opening the top result in your browser...")
    webbrowser.open(results[0]['link'])

# ------------------ Main Program ------------------
if __name__ == "__main__":
    check_for_updates()  # Check for updates before starting
    wishings()
    
    while True:
        query = commands()

        if "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "google" in query:
            query = query.replace("search google for", "").strip()
            results = search_google(query)
            display_results(results)

        elif "exit" in query:
            speak("Goodbye, Boss.")
            break
import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import webbrowser
import pyautogui
import pyjokes
import urllib.parse
import urllib.request
import re
import requests
from bs4 import BeautifulSoup

# ------------------ Text-to-Speech Initialization ------------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# ------------------ Command Recognition ------------------
def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Processing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You just said: {query}\n")
    except Exception as e:
        print(e)
        speak("Please say that again.")
        query = "none"
    return query.lower()

# ------------------ Wishing User ------------------
def wishings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        print("Good Morning, Boss")
        speak("Good Morning, Boss")
    elif hour >= 12 and hour < 17:
        print("Good Afternoon, Boss")
        speak("Good Afternoon, Boss")
    elif hour >= 17 and hour < 21:
        print("Good Evening, Boss")
        speak("Good Evening, Boss")
    else:
        print("Good Night, Boss")
        speak("Good Night, Boss")

# ------------------ Wikipedia Search ------------------
def search_wikipedia(query):
    speak("Searching in Wikipedia...")
    try:
        results = wikipedia.summary(query, sentences=1)
        speak("According to Wikipedia...")
        print(results)
        speak(results)
    except Exception as e:
        print("No results found.")
        speak("No results found.")

# ------------------ YouTube Search ------------------
def search_youtube(query):
    print(f"Searching YouTube for: {query}")
    query_string = urllib.parse.urlencode({"search_query": query})
    html_content = urllib.request.urlopen(f"http://www.youtube.com/results?{query_string}")
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    if search_results:
        video_url = f"https://www.youtube.com/watch?v={search_results[0]}"
        print(f"Found video: {video_url}")
        return video_url
    else:
        print("No video found.")
        return None

def play_video(video_url):
    print(f"Playing video: {video_url}")
    webbrowser.open(video_url)

# ------------------ Google Search ------------------
def search_google(query):
    print(f"Searching Google for: {query}")
    query_string = "+".join(query.split())
    url = f"https://www.google.com/search?q={query_string}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("div", class_="tF2Cxc"):
        title = result.find("h3").text if result.find("h3") else "No Title"
        link = result.find("a")["href"] if result.find("a") else "No Link"
        snippet = result.find("span", class_="aCOpRe").text if result.find("span", class_="aCOpRe") else "No Snippet"
        results.append({"title": title, "link": link, "snippet": snippet})

    return results

def get_weather(city):
    api_key = "5474052b9877c1bdf56d0a8548a65325"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    print(weather_data)  # Debug the API response
    
    if weather_data.get("cod") != 200:
        print(f"Error: {weather_data.get('message')}")
        return None, None, None
    
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    return weather_description, temperature, humidity

def handle_command(command):
    if "weather" in command:
        city = "Chennai"  # Replace with dynamic input if needed
        weather_description, temperature, humidity = get_weather(city)
        if weather_description:
            print(f"Weather: {weather_description}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
        else:
            print("Failed to fetch weather data.")

# Example usage
command = "weather"
handle_command(command)

def display_results(results):
    if not results:
        print("No results found.")
        return

    print("\nTop Google Search Results:\n")
    for idx, result in enumerate(results[:5], start=1):
        print(f"{idx}. {result['title']}")
        print(f"   Link: {result['link']}")
        print(f"   Snippet: {result['snippet']}\n")

    print("Opening the top result in your browser...")
    webbrowser.open(results[0]['link'])


def extract_intent_and_entity(query):
    if "wikipedia" in query:
        return "search", "wikipedia"
    if "google" in query:
        return "search", "google"
    if "play" in query:
        return "play", query.replace("play", "").strip()
    if "exit" in query:
        return "exit", None
    return "ask", query

def answer_question(context, query):
    return f"I'm sorry, I don't have an answer for '{query}' right now."

import webbrowser
import urllib.parse

def search_google(query):
    print(f"Searching Google for: {query}")
    query_string = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query_string}"
    webbrowser.open(url)
    return [{"title": "Google Search", "link": url}]

def display_results(results):
    print("Opening Google Search in your browser...")

# ------------------ Main Program ------------------
if __name__ == "__main__":
    wishings()
    while True:
        query = commands()

        # Intent Detection
        intent, entity = extract_intent_and_entity(query)

        if intent == "search":
            if entity == "wikipedia":
                query = query.replace("wikipedia", "").strip()
                search_wikipedia(query)
            elif entity == "google":
                query = query.replace("search google for", "").strip()
                results = search_google(query)
                display_results(results)

        elif intent == "play":
            video_url = search_youtube(entity)
            if video_url:
                play_video(video_url)

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak("Sir, the time is: " + strTime)
            print(strTime)

        elif "open firefox" in query:
            speak("Opening Firefox, sir.")
            os.startfile("C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")

        elif "type" in query:
            speak("Please tell me what to write.")
            while True:
                typeQuery = commands()
                if typeQuery == "exit typing":
                    break
                else:
                    pyautogui.write(typeQuery)

        elif "open gmail" in query:
            speak("Opening Gmail.")
            webbrowser.open("https://www.gmail.com")
        elif 'scroll up' in query:
            pyautogui.scroll(200)
            speak('done!')
            
        elif 'scroll up2' in query:
            pyautogui.scroll(400)
            speak('done!')
                
        elif 'scroll down' in query:
            pyautogui.scroll(-200)
            speak('done!')
            
        elif 'scroll down2' in query:
            pyautogui.scroll(-400)
            speak('done!')
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif "google" in query:
                query = query.replace("search google for", "").strip()
                results = search_google(query)
                display_results(results)
              
        
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com") 
              
        elif 'open VLC' in query:
            speak('opening VLC player sir')
            os.startfile('')
            
        elif 'open cmd' in query:
           speak('opening command promt sir')
           os.startfile('')
        
        elif 'open python idle' in query:
            speak('opening python idle sir')
            os.startfile('')
            
        elif 'open calculator' in query:
            speak('opening calculator sir')
            os.startfile('')
            
        elif 'navigate ' in query:
            pyautogui.moveRel(0, -100, duration=0.25)
            speak('done!')
            
        elif 'navigate down' in query:
            pyautogui.moveRel(0, 100, duration=0.25)
            speak('done!')
            
        
        elif 'navigate right' in query:
            pyautogui.moveRel(100, 0, duration=0.25)
            speak('done!')
        
        elif 'navigate light' in query:
            pyautogui.moveRel(100, 0, duration=0.25)
            speak('done!')
            
        elif 'navigate left' in query:
            pyautogui.moveRel(-100, 0, duration=0.25)
            speak('done!')
         
        elif 'left click' in query:
            pyautogui.click()
            speak('done!')
            
        elif  'right click' in query:
            pyautogui.click(button='right')
            speak('done!')
            
        elif 'double click' in query:
            pyautogui.click()
            pyautogui.click()  
            speak('done!')
        
            
        elif 'mouse position' in query:
            speak(pyautogui.position())
                      
        elif 'type' in query:
            newt = query.replace('type','')
            pyautogui.typewrite(newt)
            speak('done!')
            
        elif 'play music' in query:
            music_dir = 'D:\\New folder (4)\\Love songs'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))        
        elif 'open github' in query:
            webbrowser.open('https://www.github.com')
            speak("opening github sir")
        elif 'open snapdeal' in query:
            webbrowser.open('https://www.snapdeal.com')
            speak("opening snapdeal sir")
        elif 'open amazon' in query:
            webbrowser.open('https://www.amazon.com')
            speak("opening amazon sir")
        elif 'open flipkart' in query:
            webbrowser.open('https://www.flipkart.com')
            speak("opening flipkart sir")

        elif "joke" in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif intent == "ask":
            context = "Your assistant is trained to provide information on various topics."
            response = answer_question(context, query)
            print(response)
            speak(response)
   
        elif "google" in query:
            query = query.replace("search google for", "").strip()
            results = search_google(query)
            display_results(results)

        elif "exit" in query:
            speak("Goodbye, Boss.")
            break    
