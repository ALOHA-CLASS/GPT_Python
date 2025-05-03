import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from gtts import gTTS  # Google Text-to-Speech 모듈
import os

# 텍스트를 음성으로 변환하고 mp3로 저장하는 함수
def convert_text_to_speech():
    print("[DEBUG] 버튼 클릭됨: 음성 변환 시작")

    # 텍스트 입력 위젯에서 내용을 가져옴 ("1.0"은 첫 줄 첫 문자, tk.END는 끝까지)
    text = text_input.get("1.0", tk.END).strip()
    print(f"[DEBUG] 입력 텍스트: '{text}'")

    # 입력이 비어있으면 경고 메시지 출력 후 종료
    if not text:
        print("[DEBUG] 입력된 텍스트 없음")
        messagebox.showwarning("경고", "텍스트를 입력해주세요.")
        return

    try:
        # 현재 날짜와 시간을 "YYYYMMDD_HHMMSS" 형식으로 문자열로 생성
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"[DEBUG] 현재 시간 문자열: {now}")

        # 입력 텍스트 중 첫 마침표 전까지 최대 10글자를 잘라서 파일 이름 프리뷰로 사용
        preview_text = text.split(".")[0][:10]  # 예: "안녕하세요 파이썬"
        print(f"[DEBUG] 파일 이름용 미리보기 텍스트: {preview_text}")

        # 최종 파일 이름 생성
        filename = f"{now}_{preview_text}.mp3"
        print(f"[DEBUG] 최종 파일 이름: {filename}")

        # gTTS 객체를 생성 (언어는 한국어로 지정)
        tts = gTTS(text=text, lang='ko')
        print("[DEBUG] gTTS 객체 생성 완료")

        # mp3 파일로 저장
        tts.save(filename)
        print(f"[DEBUG] 파일 저장 완료: {filename}")

        # 사용자에게 저장 완료 메시지 표시
        messagebox.showinfo("완료", f"음성 파일이 저장되었습니다:\n{filename}")

    except Exception as e:
        # 예외 발생 시 오류 메시지 출력
        print(f"[ERROR] 예외 발생: {e}")
        messagebox.showerror("오류", f"음성 변환 중 오류 발생: {e}")

# 메인 윈도우 생성
root = tk.Tk()
root.title("텍스트 음성 변환기")  # 윈도우 제목 설정
root.geometry("400x300")  # 윈도우 크기 설정

# 안내 텍스트 라벨 생성 및 배치
label = tk.Label(root, text="텍스트를 입력하세요:")
label.pack(pady=10)

# 여러 줄 텍스트 입력 위젯 생성 (높이 5행, 너비 40열)
text_input = tk.Text(root, height=5, width=40)
text_input.pack(padx=10, pady=5)

# 변환 버튼 생성 및 클릭 시 convert_text_to_speech 함수 실행
convert_button = tk.Button(root, text="음성 변환", command=convert_text_to_speech)
convert_button.pack(pady=20)

# GUI 루프 실행 (윈도우 창을 유지함)
print("[DEBUG] GUI 실행 시작")
root.mainloop()
