import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Tkinter 示例界面")
root.geometry("350x200")

# 添加标签
label = tk.Label(root, text="欢迎使用 CodeBuddy 桌面应用系统")
label.pack(pady=10)

# 添加按钮事件函数
def on_click():
    label.config(text="按钮已点击！")

# 添加按钮
button = tk.Button(root, text="点击我", command=on_click)
button.pack(pady=10)

# 循环运行窗口
root.mainloop()
