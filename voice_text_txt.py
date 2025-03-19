import speech_recognition as sr
import time
from datetime import datetime

def recognize_speech_from_mic():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the specified filename and path
    filename = "trans_capture.txt"
    filepath = r"C:\Users\user\OneDrive\Desktop\BKS\project\trans_capture.txt"
    
    print("Speech-to-Text Converter with Auto-Save")
    print("---------------------------------------")
    print(f"Saving transcriptions to: {filepath}")
    print("Say something to convert to text. Press Ctrl+C to exit.")
    
    try:
        while True:
            # Use the default microphone as the audio source
            with sr.Microphone() as source:
                print("\nListening...")
                
                # Adjust for ambient noise and listen
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                
                print("Processing...")
                
                try:
                    # Use Google's speech recognition
                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    
                    # Save transcription to file
                    with open(filepath, "a") as file:
                        # Add timestamp to each entry
                        entry_time = datetime.now().strftime("%H:%M:%S")
                        file.write(f"[{entry_time}] {text}\n")
                        print(f"Text saved to {filename}")
                    
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand what you said.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\nExiting program.")
        print(f"All transcriptions saved to {filepath}")

if __name__ == "__main__":
    recognize_speech_from_mic()