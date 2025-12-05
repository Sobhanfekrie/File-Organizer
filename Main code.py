import os
import shutil
import ctypes
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu, Frame

# --- بارگذاری DLL (C Extension) ---
# file_helper.dll باید در همین پوشه باشه
# DLL فعلا فقط نمونه است و عملیاتی انجام نمیده
try:
    file_helper = ctypes.CDLL("./file_helper.dll")
except:
    file_helper = None

# --- متد مرتب‌سازی ---
def organize_files(folder, method):
    if not os.path.exists(folder):
        result_label.config(text="❌ فولدر پیدا نشد / Folder not found")
        return
    
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    # مرتب‌سازی بر اساس روش انتخاب شده
    if method == "پسوند / Extension":
        files.sort(key=lambda x: os.path.splitext(x)[1])
    elif method == "تاریخ ایجاد / Creation":
        files.sort(key=lambda x: os.path.getctime(os.path.join(folder, x)))
    elif method == "تاریخ تغییر / Modified":
        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    elif method == "حجم / Size":
        files.sort(key=lambda x: os.path.getsize(os.path.join(folder, x)))

    # ساخت فولدرها و انتقال فایل‌ها
    for f in files:
        ext = os.path.splitext(f)[1][1:] if os.path.splitext(f)[1] else "NoExtension"
        dest_folder = os.path.join(folder, ext)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(os.path.join(folder, f), os.path.join(dest_folder, f))
    
    result_label.config(text="✅ مرتب‌سازی انجام شد / Done!")

# --- رابط کاربری Tkinter ---
root = Tk()
root.title("File Organizer - سبحان فکری")

# اندازه پنجره
root.geometry("500x300")
root.resizable(False, False)

# عنوان
Label(root, text="File Organizer / سازماندهی فایل‌ها", font=("Arial", 14, "bold")).pack(pady=10)

# انتخاب فولدر
folder_path = StringVar()
def browse_folder():
    path = filedialog.askdirectory()
    if path:
        folder_path.set(path)

Button(root, text="انتخاب فولدر / Select Folder", command=browse_folder).pack(pady=5)
Label(root, textvariable=folder_path).pack(pady=5)

# انتخاب روش مرتب‌سازی
sort_method = StringVar(value="پسوند / Extension")
options = ["پسوند / Extension", "تاریخ ایجاد / Creation", "تاریخ تغییر / Modified", "حجم / Size"]
OptionMenu(root, sort_method, *options).pack(pady=10)

# دکمه اجرا
Button(root, text="شروع مرتب‌سازی / Start Organize", command=lambda: organize_files(folder_path.get(), sort_method.get())).pack(pady=10)

# نتیجه
result_label = Label(root, text="", fg="green")
result_label.pack(pady=5)

# نوشته پایین
Label(root, text="ساخته شده توسط سبحان فکری / Made by Sobhan Fekrie", font=("Arial", 10, "italic")).pack(side="bottom", pady=10)

root.mainloop()
