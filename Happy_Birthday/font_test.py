import tkinter as tk
from tkinter import font as tkFont
import os

# Initialize the Tkinter root window
root = tk.Tk()  # 创建根窗口

# 使用字体名称加载字体
try:
    pixel_font = tkFont.Font(family="Silkscreen", size=12)  # 确保字体已安装到系统
    print("Font loaded successfully!")
except Exception as e:
    print(f"Failed to load font: {e}")

# 示例文本
label = tk.Label(root, text="When is your birthday?", font=pixel_font, fg="white", bg="black")
label.pack(pady=20)

# 保持窗口运行
root.mainloop()