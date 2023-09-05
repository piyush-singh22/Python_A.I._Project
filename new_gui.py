

import tkinter as tk
import subprocess
import os
from threading import Thread
import speech_recognition as sr
from gtts import gTTS
import vlc

class ProjectRunnerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("My Python Project")
        self.root.configure(bg="#282C35")  # Set background color to dark gray
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        self.vlc_instance = vlc.Instance('--no-qt-system-tray')
        self.vlc_player = self.vlc_instance.media_player_new()
        self.project_paths = [
            "E:/Internship Project/personalAITrainer.py",
            "E:/Internship Project/ai painter.py",
            "E:/Internship Project/VolumeControl.py",
            "E:/Internship Project/fingerCounter.py",
            "E:/Internship Project/aiVirtualMouse.py"
            # Add more project paths here
        ]
        self.create_welcome_label()
        self.create_voice_button()
        self.create_buttons()
        self.note()

        # ... Rest of the methods ...


    def create_welcome_label(self):
        welcome_label = tk.Label(
            self.root,
            text="Welcome to My Python Project",
            font=("Helvetica", 20),
            bg="#282C35",
            fg="white",
        )
        welcome_label.pack(pady=(20, 0))  # Add padding at the top of the label

    def create_voice_button(self):
        # voice_icon = tk.PhotoImage(file="voice_icon.png")
        print("create command")
        voice_button = tk.Button(self.root, text="Use Voice assistant K",font=("Helvetica", 15), cursor="hand2", command=self.run_voice_assistant)
        voice_button.pack(pady=(10, 0))
        welcome_label = tk.Label(
            self.root,
            text="OR",
            font=("Helvetica", 20),
            bg="#282C35",
            fg="white",
        )
        welcome_label.pack(pady=(10, 0))
        # voice_button.place(x=150, y=50)

    def run_voice_assistant(self):
        print("run_voice_assistant")
        assistant_thread = Thread(target=self.voice_assistant_thread)
        assistant_thread.start()

    def speak(self, text):
        tts = gTTS(text=text, lang='en')  # Create a gTTS object with the given text
        tts.save('output.mp3')  # Save the generated audio as an MP3 file
        # subprocess.Popen(['start', 'output.mp3'], shell=True)  # Play the MP3 audio using the default system player

        # By using vlc with the - -no - qt - system - tray flag, the media player should run without showing its
        # interface, which would address the issue of it opening in the foreground.
        media = self.vlc_instance.media_new('output.mp3')
        self.vlc_player.set_media(media)
        self.vlc_player.play()



    def voice_assistant_thread(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            self.speak("Voice command assistant is ready. How can I help you?")
            print("Listening...")
            audio = self.recognizer.listen(source, timeout=10)

        try:
            command = r.recognize_google(audio).lower().strip()
            print("You said:", command)
            if "run project" in command:
                project_number = command.split("run project", 1)[1].strip()
                if project_number.isdigit():
                    project_index = int(project_number) - 1
                    if 0 <= project_index < len(self.project_paths):
                        project_path = self.project_paths[project_index]
                        self.speak(f"Running project {project_index + 1}")
                        self.run_project(project_path)
                else:
                    self.speak("Project not found.")
            else:
                self.speak("Sorry, I didn't understand that.")
        except Exception as e:
            print("Error:", e)
            self.speak("Sorry, I had trouble understanding you.")

    def create_buttons(self):
        for i, project_path in enumerate(self.project_paths):
            project_name = os.path.basename(project_path)
            button = tk.Button(self.root, text=f"Run project {i+1} : {project_name}", font=("Arial", 15), cursor="hand2", command=lambda path=project_path: self.run_project(path))
            button.pack(pady=(23, 4))


    def run_project(self, path):
        try:
            subprocess.Popen(["python", path])
        except Exception as e:
            print("Error:", e)
    #
    # welcome_label = tk.Label(
    #     self.root,
    #     text="OR",
    #     font=("Helvetica", 20),
    #     bg="#282C35",
    #     fg="white",
    # )
    # welcome_label.pack(pady=(10, 0))

    def note(self):
        info = tk.Label(self.root, text="* To use voice assistance tell run project and its index number for example 'run project 1' *", font=("Helvetica", 10), bg="#282C35", fg="white")
        info.pack(pady=(24,25))

if __name__ == "__main__":
    root = tk.Tk()
    # ck.set_appearance_mode("dark")
    root.geometry("620x575")    # it is in the form of width x height
    app = ProjectRunnerGUI(root)
    root.mainloop()
