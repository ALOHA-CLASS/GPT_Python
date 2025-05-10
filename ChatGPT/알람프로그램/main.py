import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
import threading
import time
import pygame
import mysql.connector
from plyer import notification

# ===================== DB SETUP =====================
def connect_db():
    # MySQL DB에 연결하고 alarm 테이블 생성 (status 추가)
    conn = mysql.connector.connect(
        host='localhost', user='python', password='123456', database='python'
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alarm (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            time DATETIME,
            sound_path TEXT,
            status VARCHAR(10) DEFAULT 'on'  -- 알람 상태 (on/off)
        )
    ''')
    conn.commit()
    return conn

# ===================== ALARM PLAYER =====================
def play_alarm(sound_path):
    # 알람 소리를 반복 재생 (stop_event가 설정될 때까지)
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    while not stop_event.is_set():
        pygame.mixer.music.play()
        time.sleep(pygame.mixer.Sound(sound_path).get_length())

def notify_user(title, msg):
    # 윈도우 알림을 띄움
    notification.notify(
        title=title,
        message=msg,
        timeout=5
    )

# ===================== MAIN APP =====================
class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("알람 대시보드")
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill='both', expand=True)

        self.add_button = ttk.Button(self.frame, text="알람 등록", command=self.open_add_alarm_window)
        self.add_button.pack(pady=5)

        # 알람 리스트 출력용 TreeView 구성
        self.tree = ttk.Treeview(self.frame, columns=('Name', 'Time', 'Sound', 'Status'), show='headings')
        self.tree.heading('Name', text='알람 이름')
        self.tree.heading('Time', text='알람 시간')
        self.tree.heading('Sound', text='알람 소리')
        self.tree.heading('Status', text='상태')
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<Double-1>', self.open_edit_alarm_window)

        self.load_alarms()
        self.check_alarms()

    def load_alarms(self):
        # DB에서 알람 목록을 불러와 TreeView에 표시
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT id, name, time, sound_path, status FROM alarm")
        for id, name, time_, sound, status in self.cursor.fetchall():
            self.tree.insert('', 'end', iid=id, values=(name, time_, os.path.basename(sound), status))

    def open_add_alarm_window(self):
        AlarmEditor(self.root, self.conn, self.load_alarms)

    def open_edit_alarm_window(self, event):
        selected = self.tree.focus()
        if selected:
            alarm_id = int(selected)
            AlarmEditor(self.root, self.conn, self.load_alarms, alarm_id)

    def check_alarms(self):
        # 주기적으로 현재 시각과 알람 시간 비교하여 실행 조건 체크
        def run():
            while True:
                self.cursor.execute("SELECT id, name, time, sound_path FROM alarm WHERE status='on'")
                for alarm_id, name, alarm_time, sound in self.cursor.fetchall():
                    now = datetime.now()
                    # 알람 시간이 지났고 아직 울리지 않은 알람이면 실행
                    if now >= alarm_time and not active_alarms.get(alarm_id):
                        active_alarms[alarm_id] = True
                        threading.Thread(target=self.trigger_alarm, args=(alarm_id, name, alarm_time, sound)).start()
                time.sleep(10)
        threading.Thread(target=run, daemon=True).start()

    def trigger_alarm(self, alarm_id, name, alarm_time, sound):
        # 알람 실행: 알림 표시 및 소리 재생
        notify_user("알람", f"{name} - {alarm_time.strftime('%Y-%m-%d %H:%M:%S')}")
        global stop_event
        stop_event = threading.Event()
        threading.Thread(target=play_alarm, args=(sound,), daemon=True).start()

        # 알람 종료용 팝업 윈도우
        stop_window = tk.Toplevel(self.root)
        stop_window.title("알람 울림")
        ttk.Label(stop_window, text=f"알람: {name}").pack(pady=10)
        ttk.Label(stop_window, text=f"시간: {alarm_time}").pack(pady=5)
        stop_btn = ttk.Button(stop_window, text="알람 끄기", command=lambda: self.stop_alarm(stop_window, alarm_id))
        stop_btn.pack(pady=20)

    def stop_alarm(self, window, alarm_id):
        # 알람 정지 처리: 소리 중지 + DB 상태 변경
        stop_event.set()
        pygame.mixer.music.stop()
        window.destroy()

        # 알람 상태를 'off'로 업데이트
        self.cursor.execute("UPDATE alarm SET status='off' WHERE id=%s", (alarm_id,))
        self.conn.commit()
        self.load_alarms()

# ===================== ALARM EDITOR =====================
class AlarmEditor:
    def __init__(self, root, conn, refresh_callback, alarm_id=None):
        self.conn = conn
        self.cursor = conn.cursor()
        self.refresh_callback = refresh_callback
        self.alarm_id = alarm_id

        self.top = tk.Toplevel(root)
        self.top.title("알람 수정" if alarm_id else "알람 등록")

        # 알람 이름 입력
        ttk.Label(self.top, text="알람 이름").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.top)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # 날짜 선택
        ttk.Label(self.top, text="알람 날짜").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.top, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # 시간 입력 (시:분)
        ttk.Label(self.top, text="시간 (HH:MM)").grid(row=2, column=0, padx=5, pady=5)
        self.time_entry = ttk.Entry(self.top)
        self.time_entry.insert(0, "08:00")  # 기본값 설정
        self.time_entry.grid(row=2, column=1, padx=5, pady=5)

        # 알람 소리 선택
        ttk.Label(self.top, text="알람 소리").grid(row=3, column=0, padx=5, pady=5)
        self.sound_combo = ttk.Combobox(self.top, values=self.load_sounds())
        self.sound_combo.set("기본.mp3")
        self.sound_combo.grid(row=3, column=1, padx=5, pady=5)

        # 저장 버튼
        save_btn = ttk.Button(self.top, text="저장", command=self.save_alarm)
        save_btn.grid(row=4, column=0, pady=10)

        # 수정 시 삭제 버튼도 표시
        if alarm_id:
            delete_btn = ttk.Button(self.top, text="삭제", command=self.delete_alarm)
            delete_btn.grid(row=4, column=1, pady=10)

        if alarm_id:
            self.load_alarm_data()

    def load_sounds(self):
        # 알람 사운드 폴더에서 mp3 파일 목록 가져오기
        sound_dir = "c:/alarm"
        return [f for f in os.listdir(sound_dir) if f.endswith(".mp3")]

    def load_alarm_data(self):
        # DB에서 알람 정보 로드하여 폼에 설정
        self.cursor.execute("SELECT name, time, sound_path FROM alarm WHERE id=%s", (self.alarm_id,))
        name, time_, sound = self.cursor.fetchone()
        self.name_entry.insert(0, name)
        self.date_entry.set_date(time_)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, time_.strftime("%H:%M"))
        self.sound_combo.set(os.path.basename(sound))

    def save_alarm(self):
        # 폼에서 입력한 데이터를 저장하거나 업데이트
        name = self.name_entry.get()
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")
        time_str = self.time_entry.get()
        datetime_str = f"{date_str} {time_str}:00"
        sound = os.path.join("c:/alarm", self.sound_combo.get())

        if self.alarm_id:
            self.cursor.execute(
                "UPDATE alarm SET name=%s, time=%s, sound_path=%s, status='on' WHERE id=%s",
                (name, datetime_str, sound, self.alarm_id)
            )
        else:
            self.cursor.execute(
                "INSERT INTO alarm (name, time, sound_path, status) VALUES (%s, %s, %s, 'on')",
                (name, datetime_str, sound)
            )
        self.conn.commit()
        self.refresh_callback()
        self.top.destroy()

    def delete_alarm(self):
        # 알람 삭제 확인 후 DB에서 제거
        if messagebox.askyesno("삭제 확인", "이 알람을 삭제하시겠습니까?"):
            self.cursor.execute("DELETE FROM alarm WHERE id=%s", (self.alarm_id,))
            self.conn.commit()
            self.refresh_callback()
            self.top.destroy()

# ===================== MAIN =====================
if __name__ == "__main__":
    active_alarms = {}  # 현재 실행 중인 알람 목록
    stop_event = threading.Event()  # 알람 중지 이벤트
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
