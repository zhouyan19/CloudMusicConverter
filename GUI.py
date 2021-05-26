# -*- coding:utf-8 -*-

import os
import base64
import threading
from converter import Transform
from ico_data import img
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Progressbar as PB

window = tk.Tk()
window.title('Cloud Music Converter 1.2')
with open("icon.ico", "wb+") as f:
    f.write(base64.b64decode(img))
window.iconbitmap('icon.ico')
window.geometry('600x220')

def help():
    word = '打开网易云音乐电脑端，进入设置->下载设置，找到缓存目录，这个目录存放的是你播放过的歌曲的缓存文件。在本转换器中，缓存文件即为这个目录里的.uc结尾的文件。选中你想要转换的歌曲对应的.uc文件，再选择输出目录，点击转换按钮即可获得该歌曲的.mp3文件。'
    mb.showinfo('Help', word)

mebubar = tk.Menu(window)
mebubar.add_command(label="使用帮助", command=help)
window.config(menu=mebubar)

path = tk.StringVar()
path2 = tk.StringVar()
uc_file = ''
mp3_dir = ''

def selectPathUC():
    #选择文件path_接收文件地址
    global uc_file, btn
    f_path = fd.askopenfilename()
    path.set(f_path)
    uc_file = path.get()

def selectPathMP3():
    #选择文件path_接收文件地址
    global mp3_dir, btn
    g_path = fd.askdirectory()
    path2.set(g_path)
    mp3_dir = path2.get() + '/'

def Bar():
    progress.grid(row=4, column=0, sticky='W', padx=16, pady=20)
    progress.start()
    T = threading.Thread(target=convert)
    T.start()

def End():
    progress.stop()
    progress.grid_forget()

def convert():
    global uc_file, mp3_dir
    print('uc:', uc_file)
    print('mp3:', mp3_dir)
    if not (os.path.isfile(uc_file)):
        End()
        print('Not a file.')
        mb.showwarning('Warnig', '源文件不存在！')
        return
    if not (os.path.isdir(mp3_dir)):
        End()
        print('Not a directory.')
        mb.showwarning('Warnig', '输出目录不存在！')
        return
    try:
        transform = Transform(uc_file, mp3_dir)
        code = transform.do_transform()
        if (code == 1):
            End()
            mb.showwarning('Warnig', '非正确的uc文件！')
            print('Done.')
        else:
            End()
            mb.showinfo('Info', '转换成功！')
    except Exception as e:
        End()
        mb.showerror('Error', str(e))
        print('Exception:', e)
        return


# def Ready():
#     if uc_file and mp3_dir:
#         return 'active'
#     else:
#         return 'disabled'

tk.Label(window, text="缓存文件路径:").grid(row=0, column=0, sticky='W', padx=16, pady=10)
tk.Entry(window, textvariable=path, width=64).grid(row=1, column=0, padx=16)
tk.Button(window, text="选择缓存文件", command=selectPathUC).grid(row=1, column=1, padx=10)

tk.Label(window, text="MP3文件路径:").grid(row=2, column=0, sticky='W', padx=16)
tk.Entry(window, textvariable=path2, width=64).grid(row=3, column=0, padx=16)
tk.Button(window, text="选择输出目录", command=selectPathMP3).grid(row=3, column=1, padx=10)

progress = PB(window, orient=tk.HORIZONTAL, length=452, mode='indeterminate')
# progress['value'] = 50
# progress['maximum'] = 100
tk.Button(window, text="开始转换", command=Bar).grid(row=4, column=1, sticky='E', padx=10, pady=20)

window.mainloop()
