import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Функции ---
def load_history():
    """Загружает историю из файла JSON."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в файл JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password():
    """Генерирует пароль на основе выбранных параметров."""
    try:
        length = int(length_slider.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректная длина пароля.")
        return

    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}.")
        return

    chars = ""
    if use_upper.get():
        chars += string.ascii_uppercase
    if use_lower.get():
        chars += string.ascii_lowercase
    if use_digits.get():
        chars += string.digits
    if use_symbols.get():
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
        return

    password = ''.join(random.choices(chars, k=length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    # Добавление в историю
    history.append({"password": password, "length": length})
    save_history(history)
    update_history_tree()

def update_history_tree():
    """Обновляет виджет Treeview с историей."""
    for i in history_tree.get_children():
        history_tree.delete(i)
    for item in history:
        history_tree.insert("", "end", values=(item["password"], item["length"]))

def copy_to_clipboard():
    """Копирует пароль в буфер обмена."""
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

# --- Инициализация ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("600x500")
root.resizable(False, False)

# Загрузка истории при старте
history = load_history()

# --- Интерфейс ---
# Длина пароля
tk.Label(root, text="Длина пароля:").place(x=20, y=20)
length_slider = tk.Scale(root, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL, length=200)
length_slider.set(12)
length_slider.place(x=120, y=20)
tk.Label(root, text=f"(от {MIN_LENGTH} до {MAX_LENGTH})").place(x=330, y=23)

# Чекбоксы символов
use_upper = tk.BooleanVar(value=True)
use_lower = tk.BooleanVar(value=True)
use_digits = tk.BooleanVar(value=True)
use_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="A-Z (Верхний регистр)", variable=use_upper).place(x=20, y=60)
tk.Checkbutton(root, text="a-z (Нижний регистр)", variable=use_lower).place(x=20, y=90)
tk.Checkbutton(root, text="0-9 (Цифры)", variable=use_digits).place(x=20, y=120)
tk.Checkbutton(root, text="!@#$% (Спецсимволы)", variable=use_symbols).place(x=20, y=150)

# Кнопка генерации и поле результата
tk.Button(root, text="Сгенерировать", command=generate_password).place(x=20, y=190)
password_entry = tk.Entry(root, width=45)
password_entry.place(x=120, y=195)
tk.Button(root, text="Копировать", command=copy_to_clipboard).place(x=450, y=193)

# История паролей
history_frame = tk.LabelFrame(root, text="История", padx=5, pady=5)
history_frame.place(x=20, y=240, width=540, height=220)

history_tree = ttk.Treeview(history_frame, columns=("Пароль", "Длина"), show="headings")
history_tree.heading("Пароль", text="Пароль")
history_tree.heading("Длина", text="Длина")
history_tree.column("Пароль", width=400)
history_tree.column("Длина", width=100)
history_tree.pack(fill="both", expand=True)

# Обновляем историю при запуске окна
update_history_tree()

root.mainloop()
