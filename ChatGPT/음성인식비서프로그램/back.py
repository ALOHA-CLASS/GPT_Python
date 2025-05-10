# pip install SpeechRecognition pyttsx3 pyaudio
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# 음성 엔진 초기화
engine = pyttsx3.init()

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("말씀하세요...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language='ko-KR')
            print("사용자:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("무슨 말인지 잘 모르겠어요.")
            return ""
        except sr.RequestError:
            speak("서버에 연결할 수 없습니다.")
            return ""

def run_assistant():
    speak("무엇을 도와드릴까요?")
    while True:
        command = listen()

        if '시간' in command:
            now = datetime.datetime.now().strftime("%H시 %M분입니다.")
            speak(now)

        elif '검색' in command:
            speak("무엇을 검색할까요?")
            query = listen()
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"{query}에 대한 검색 결과입니다.")

        elif '메모' in command:
            speak("메모 내용을 말씀해주세요.")
            memo = listen()
            with open("memo.txt", "a", encoding="utf-8") as f:
                f.write(memo + "\n")
            speak("메모가 저장되었습니다.")

        elif '종료' in command or '그만' in command:
            speak("프로그램을 종료합니다.")
            break

        else:
            speak("죄송해요. 그 명령은 이해하지 못했어요.")

# 프로그램 실행
if __name__ == "__main__":
    run_assistant()
