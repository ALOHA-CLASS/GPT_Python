import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime, timedelta
import threading
import time
import os
import pygame
import mysql.connector

# DB 설정
DB_CONFIG = {
    'host': 'localhost',
    'user': 'python',
    'password': '123456',
    'database': 'python'
}

DEFAULT_SOUND_PATH = "c:/alarm/기본.mp3"
SOUND_DIR = "c:/alarm/"

class AlarmManager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarm (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                time DATETIME,
                sound_path TEXT
            )
        ''')
        self.conn.commit()

    def add_alarm(self, name, time, sound_path):
        self.cursor.execute('INSERT INTO alarm (name, time, sound_path) VALUES (%s, %s, %s)', (name, time, sound_path))
        self.conn.commit()

    def get_alarms(self):
        self.cursor.execute('SELECT * FROM alarm')
        return self.cursor.fetchall()

    def delete_alarm(self, alarm_id):
        self.cursor.execute('DELETE FROM alarm WHERE id = %s', (alarm_id,))
        self.conn.commit()

    def update_alarm(self, alarm_id, name, time, sound_path):
        self.cursor.execute('UPDATE alarm SET name=%s, time=%s, sound_path=%s WHERE id=%s', (name, time, sound_path, alarm_id))
        self.conn.commit()

class AlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("알람 프로그램")
        self.manager = AlarmManager()
        pygame.mixer.init()
        self.selected_alarm = None

        self._build_dashboard()
        self._refresh_alarm_list()
        self._start_alarm_checker()

    def _build_dashboard(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "이름", "시간"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("이름", text="이름")
        self.tree.heading("시간", text="시간")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind('<Double-1>', self._open_edit_alarm)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="알람 등록", command=self._open_add_alarm).pack(side="left", padx=5)

    def _refresh_alarm_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for alarm in self.manager.get_alarms():
            self.tree.insert("", "end", values=(alarm[0], alarm[1], alarm[2]))

    def _open_add_alarm(self):
        AlarmEditWindow(self.root, self.manager, refresh_callback=self._refresh_alarm_list)

    def _open_edit_alarm(self, event):
        selected_item = self.tree.selection()[0]
        alarm_id = self.tree.item(selected_item)['values'][0]
        AlarmEditWindow(self.root, self.manager, alarm_id=alarm_id, refresh_callback=self._refresh_alarm_list)

    def _start_alarm_checker(self):
        def check_alarms():
            while True:
                alarms = self.manager.get_alarms()
                now = datetime.now()
                for alarm in alarms:
                    alarm_id, name, alarm_time, sound_path = alarm
                    if now >= alarm_time and now < alarm_time + timedelta(seconds=5):
                        self._trigger_alarm(name, sound_path)
                time.sleep(1)

        threading.Thread(target=check_alarms, daemon=True).start()

    def _trigger_alarm(self, name, sound_path):
        def play_sound():
            pygame.mixer.music.load(sound_path or DEFAULT_SOUND_PATH)
            pygame.mixer.music.play(loops=-1)

        def stop_alarm():
            pygame.mixer.music.stop()
            alert.destroy()

        alert = tk.Toplevel(self.root)
        alert.title("알람 알림")
        tk.Label(alert, text=f"알람: {name}", font=("Arial", 14)).pack(pady=10)
        tk.Button(alert, text="알람 끄기", command=stop_alarm).pack(pady=10)
        play_sound()

class AlarmEditWindow:
    def __init__(self, parent, manager, alarm_id=None, refresh_callback=None):
        self.manager = manager
        self.alarm_id = alarm_id
        self.refresh_callback = refresh_callback
        self.top = tk.Toplevel(parent)
        self.top.title("알람 수정" if alarm_id else "알람 등록")

        tk.Label(self.top, text="이름:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.top)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.top, text="시간 (YYYY-MM-DD HH:MM:SS):").grid(row=1, column=0)
        self.time_entry = tk.Entry(self.top)
        self.time_entry.grid(row=1, column=1)

        tk.Label(self.top, text="소리:").grid(row=2, column=0)
        self.sound_path = tk.StringVar(value=DEFAULT_SOUND_PATH)
        tk.Entry(self.top, textvariable=self.sound_path).grid(row=2, column=1)
        tk.Button(self.top, text="소리 선택", command=self._choose_sound).grid(row=2, column=2)

        action_btn = tk.Button(self.top, text="수정" if alarm_id else "등록", command=self._save_alarm)
        action_btn.grid(row=3, columnspan=3, pady=10)

        if alarm_id:
            self._load_alarm()

    def _choose_sound(self):
        path = filedialog.askopenfilename(initialdir=SOUND_DIR, filetypes=[("MP3 파일", "*.mp3")])
        if path:
            self.sound_path.set(path)

    def _load_alarm(self):
        alarm = [a for a in self.manager.get_alarms() if a[0] == self.alarm_id][0]
        self.name_entry.insert(0, alarm[1])
        self.time_entry.insert(0, alarm[2].strftime("%Y-%m-%d %H:%M:%S"))
        self.sound_path.set(alarm[3])

    def _save_alarm(self):
        name = self.name_entry.get()
        time_str = self.time_entry.get()
        sound_path = self.sound_path.get()
        try:
            alarm_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("오류", "시간 형식이 잘못되었습니다.")
            return

        if self.alarm_id:
            self.manager.update_alarm(self.alarm_id, name, alarm_time, sound_path)
        else:
            self.manager.add_alarm(name, alarm_time, sound_path)

        if self.refresh_callback:
            self.refresh_callback()
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
