"""
Neoreg_Gui

Author: 青山(qingshan@88.com)
License: MIT license
Source: https://github.com/iqingshan/Neoreg_Gui
"""

import signal
import os
import tkinter as tk
from tkinter import ttk,messagebox,scrolledtext
from datetime import datetime
import subprocess
import threading

__version__ = "1.0.0"
banner = r"""

          "$$$$$$''  'M$  '$$$@m
        :$$$$$$$$$$$$$$''$$$$'
       '$'    'JZI'$$&  $$$$'
                 '$$$  '$$$$
                 $$$$  J$$$$'
                m$$$$  $$$$,
                $$$$@  '$$$$_          Neo-reGeorg-Gui
             '1t$$$$' '$$$$<
          '$$$$$$$$$$'  $$$$          version {}
               '@$$$$'  $$$$'       
                '$$$$  '$$$@
             'z$$$$$$  @$$$
                r$$$   $$|
                '$$v c$$
               '$$v $$v$$$$$$$$$#
               $$x$$$$$$$$$twelve$$$@$'
             @$$$@L '    '<@$$$$$$$$`
           $$                 '$$$


    [ Github ] https://github.com/iqingshan/Neo_Gui
""".format(__version__)

class gui():

    def __init__(self):
        self.process = None
    def on_focus_in(self,entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
    def on_focus_out(self,entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.delete(0, tk.END)
    # 添加一个示例函数来向终端输出信息
    def print_to_terminal(self,message, status='Error', color=2):
        colors = ['green','blue','red']
        terminal_output.configure(state=tk.NORMAL)
        terminal_output.tag_configure(colors[color], foreground=colors[color])
        terminal_output.insert(tk.END, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        terminal_output.insert(tk.END, "["+status+"] ")
        terminal_output.tag_add(colors[color], "end-1c linestart", "end-1c lineend")
        terminal_output.insert(tk.END, message + "\r\n")
        terminal_output.tag_add(colors[color], "end-2c linestart", "end-2c lineend")
        terminal_output.see(tk.END)  # 自动滚动到底部

    # 执行长时间执行的脚本不等待完成逐行获取输出
    def run_script(self,p,path,url,key):
        self.process = subprocess.Popen(f"{p} {path} -u {url} -k {key}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = self.process.stdout.readline()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                print(output.strip())
                self.print_to_terminal(output.decode(),'info',1)

    # 关闭上方函数的执行命令
    def stop_script(self):
        if self.process is not None:
            self.print_to_terminal("正在关闭代理...",'info',1)
            self.process.terminate()
            self.process.wait()
            self.print_to_terminal("关闭代理成功！",'success',0)
            self.process = None
        else:
            self.print_to_terminal("没有代理正在运行！",'info',1)

    # 连接
    def Connect(self):
        p = p_var.get()
        path = path_var.get()
        url = entry_var.get()
        key = key_var.get()
        if p == "" or path == "" or url == "" or key == "" or url == "请输入URL" or key == "请输入Key":
            # messagebox.showinfo("提示", "请输入完整信息！")
            self.print_to_terminal("请输入URL，Key！")
            return 0
        self.print_to_terminal("启动Neoreg！",'info',1)
        if self.process is not None:
            self.print_to_terminal("已经启动中！",'info',1)
        else:
            a1 = threading.Thread(target=self.run_script, args=(p,path,url,key))
            a1.start()
            self.print_to_terminal("启动成功！",'success',0)

    def on_closing(self):
        if self.process is not None:
            # 杀死子进程
            os.kill(self.process.pid, signal.SIGTERM)
        # 杀死当前进程
        os.kill(os.getpid(), signal.SIGTERM)
        root.destroy()

# 实例化gui
gui = gui()


# GUI 开始
root = tk.Tk()
root.title("Neoreg_Gui")
root.option_add("*tearOff", False) # This is always a good idea

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

# Create a style
style = ttk.Style(root)

def is_time_between_8am_and_6pm():
    # 获取当前时间
    now = datetime.now()
    # 获取当前小时数（24小时制）
    current_hour = now.hour

    # 判断当前时间是否在8点到18点（即晚上6点）之间
    if 8 <= current_hour < 18:
        return True
    else:
        return False
# 主题判断
if is_time_between_8am_and_6pm():
    # Import the tcl file
    root.tk.call("source", "forest-light.tcl")
    # Set the theme with the theme_use method
    style.theme_use("forest-light")
else:
    # Import the tcl file
    root.tk.call("source", "forest-dark.tcl")
    # Set the theme with the theme_use method
    style.theme_use("forest-dark")

# Create lists for the Comboboxes
option_menu_list = ["", "OptionMenu", "Option 1", "Option 2"]
combo_list = ["Combobox", "Editable item 1", "Editable item 2"]
readonly_combo_list = ["Readonly combobox", "Item 1", "Item 2"]

# Create control variables
a = tk.BooleanVar()
b = tk.BooleanVar(value=True)
c = tk.BooleanVar()
d = tk.IntVar(value=2)
e = tk.StringVar(value=option_menu_list[1])
f = tk.BooleanVar()
g = tk.DoubleVar(value=75.0)
h = tk.BooleanVar()


# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

# 创建一个StringVar变量
p_var = tk.StringVar()
# Entry
p_entry = ttk.Entry(widgets_frame, textvariable=p_var)
p_placeholder = "Python3"


p_entry.insert(0, p_placeholder)
p_entry.bind('<FocusIn>', lambda event: gui.on_focus_in(p_entry, p_placeholder))
p_entry.bind('<FocusOut>', lambda event: gui.on_focus_out(p_entry, p_placeholder))
p_entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")

# 创建一个StringVar变量
path_var = tk.StringVar()
# Entry
path_entry = ttk.Entry(widgets_frame, textvariable=path_var)
path_placeholder = "neoreg.py"

path_entry.insert(0, path_placeholder)
path_entry.bind('<FocusIn>', lambda event: gui.on_focus_in(path_entry, path_placeholder))
path_entry.bind('<FocusOut>', lambda event: gui.on_focus_out(path_entry, path_placeholder))
path_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")


# 创建一个StringVar变量
entry_var = tk.StringVar()
# Entry
entry = ttk.Entry(widgets_frame,textvariable=entry_var)
placeholder = "请输入URL"


entry.insert(0, placeholder)
entry.bind('<FocusIn>', lambda event: gui.on_focus_in(entry, placeholder))
entry.bind('<FocusOut>', lambda event: gui.on_focus_out(entry, placeholder))
entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")

# 创建一个StringVar变量
key_var = tk.StringVar()
# KEY
key_entry = ttk.Entry(widgets_frame, textvariable=key_var)
key_placeholder = "请输入Key"


key_entry.insert(0, key_placeholder)
key_entry.bind('<FocusIn>', lambda event: gui.on_focus_in(key_entry, key_placeholder))
key_entry.bind('<FocusOut>', lambda event: gui.on_focus_out(key_entry, key_placeholder))
key_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")


# 连接
button = ttk.Button(widgets_frame, text="连接", style="Accent.TButton", command=gui.Connect)
button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

def show_alert():
    messagebox.showinfo("Success", "生成成功！")

# 生成
button = ttk.Button(widgets_frame, text="关闭", style="Accent.TButton",command=gui.stop_script)
button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")


# Switch
# switch = ttk.Checkbutton(widgets_frame, text="切换主题", style="Switch",command=theme_switch)
# switch.grid(row=10,column=0, padx=5, pady=10, sticky="SW")

# Panedwindow
paned = ttk.PanedWindow(root)
paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)


pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=10)
pane_1.pack(side="right", fill="y")

treeFrame = ttk.LabelFrame(pane_1,text="输出", padding=(5, 5))  # 添加边框宽度和样式
treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

# 终端输出框
terminal_output = scrolledtext.ScrolledText(treeFrame, undo=True, wrap=tk.WORD)
terminal_output.pack(expand=True, fill="both", padx=5, pady=5)
gui.print_to_terminal(banner,'Logo',0)

# 窗口大小
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))



root.protocol("WM_DELETE_WINDOW", gui.on_closing)

# 运行
root.mainloop()