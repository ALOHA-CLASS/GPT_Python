import os
import uuid
import qrcode
import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk

# DB 연결 설정
def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='python',
            password='123456',
            database='python'
        )
        cursor = conn.cursor()

        # 테이블이 없으면 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qr_code (
                no INT AUTO_INCREMENT PRIMARY KEY,
                id CHAR(36) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                value TEXT NOT NULL,
                path VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        return conn, cursor
    except mysql.connector.Error as err:
        messagebox.showerror("DB 연결 오류", str(err))
        return None, None

# QR 코드 생성 함수
def generate_qr_code(name, value, path):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{now}_{name}.png"
    full_path = os.path.join(path, filename)
    qr = qrcode.make(value)
    qr.save(full_path)
    return filename, full_path

# QR 코드 정보 DB 저장 함수
def save_qr_info(name, value, path):
    conn = get_connection()
    cursor = conn.cursor()
    qr_id = str(uuid.uuid4())
    now = datetime.now()
    cursor.execute("""
        INSERT INTO qr_code (id, name, value, path, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (qr_id, name, value, path, now, now))
    conn.commit()
    conn.close()

# 메인 GUI 클래스
class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR 코드 생성기")
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="QR 코드 이름").grid(row=0, column=0)
        tk.Label(frame, text="QR 코드 값").grid(row=1, column=0)
        tk.Label(frame, text="저장 경로").grid(row=2, column=0)

        self.name_entry = tk.Entry(frame)
        self.value_entry = tk.Entry(frame)
        self.path_entry = tk.Entry(frame, width=40)

        self.name_entry.grid(row=0, column=1)
        self.value_entry.grid(row=1, column=1)
        self.path_entry.grid(row=2, column=1)

        tk.Button(frame, text="경로 선택", command=self.choose_path).grid(row=2, column=2)
        tk.Button(frame, text="QR 코드 생성", command=self.create_qr).grid(row=3, column=1, pady=5)

        self.tree = ttk.Treeview(self.root, columns=("name", "value", "path"), show="headings")
        self.tree.heading("name", text="이름")
        self.tree.heading("value", text="값")
        self.tree.heading("path", text="경로")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree.bind("<Double-1>", self.edit_qr)

    def choose_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def create_qr(self):
        name = self.name_entry.get()
        value = self.value_entry.get()
        path = self.path_entry.get()
        if not (name and value and path):
            messagebox.showwarning("입력 오류", "모든 항목을 입력하세요.")
            return
        filename, full_path = generate_qr_code(name, value, path)
        save_qr_info(name, value, full_path)
        messagebox.showinfo("성공", f"QR 코드 생성 완료\n{filename}")
        self.refresh_list()

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, value, path FROM qr_code")
        for (id, name, value, path) in cursor:
            self.tree.insert("", tk.END, iid=id, values=(name, value, path))
        conn.close()

    def edit_qr(self, event):
        item_id = self.tree.selection()[0]
        new_name = simpledialog.askstring("이름 변경", "새 이름 입력")
        if new_name:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE qr_code SET name=%s, updated_at=%s WHERE id=%s", (new_name, datetime.now(), item_id))
            conn.commit()
            conn.close()
            self.refresh_list()
        delete = messagebox.askyesno("삭제", "이 항목을 삭제하시겠습니까?")
        if delete:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT path FROM qr_code WHERE id=%s", (item_id,))
            result = cursor.fetchone()
            if result:
                try:
                    os.remove(result[0])
                except FileNotFoundError:
                    pass
            cursor.execute("DELETE FROM qr_code WHERE id=%s", (item_id,))
            conn.commit()
            conn.close()
            self.refresh_list()

if __name__ == '__main__':
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
