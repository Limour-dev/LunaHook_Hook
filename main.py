# mamba create -n uiautomation conda-forge::uiautomation

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkf
import uiautomation as auto

import mods.m03_windows as windows
from mods.m05_attachprocess import getAttachProcess

_cfg_json = {
    'ddb_char': 2,
    'ddb_content': 2,
    'allHooks': [],
    'ddb_char_Item': 0,
    'ddb_content_Item': 0,
    'label_log': r'D:\datasets\tmp\1.txt'
}


class Cfg:
    selectedp: tuple
    control: auto.ControlFromHandle
    ListControl: auto.ListControl
    ListItem: dict
    encoding_list = [
        'shift_jis',
        'gbk',
        'utf-8',
        'utf-16-le',
        'utf-32-le',
        'big5',
    ]
    var_n: str = '旁白'
    var_d: str = '内容'


def allControls(control, _if=None, _pc=None):
    if _if is None:
        def _if(x):
            return x.ControlTypeName == 'ListItemControl'
    if _pc is None:
        def _pc(x):
            return x.TextControl(foundIndex=2)

    retn = {}
    for c, d in auto.WalkControl(control, False, 1):
        if _if(c):
            retn[c.Name] = _pc(c)
    return retn


def ddb_list(_current=0, _list=None):
    _ddb = ttk.Combobox(Windows.root)
    _ddb['value'] = _list
    _ddb.current(_current)
    return _ddb


class Windows:
    root = tk.Tk()
    # ===== 选择进程 =====
    button_AttachProcess: tk.Button
    label_AttachProcessPID: tk.Label
    # ===== 枚举列表 =====
    button_ListItem: tk.Button
    # ===== 人物 =====
    ddb_char: ttk.Combobox
    ddb_char_Item: ttk.Combobox
    # ===== 内容 =====
    ddb_content: ttk.Combobox
    ddb_content_Item: ttk.Combobox
    # ===== 捕获输出 =====
    label_cb_n: tk.Label
    label_cb_d: tk.Label


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.2 " + ("管理员" if windows.IsUserAnAdmin() else "非管理员"))  # 窗口名
Windows.root.geometry('640x320+10+10')  # axb为窗口大小，+10 +10 定义窗口弹出时的默认展示位置

Windows.root.attributes("-topmost", True)  # 设置窗口在最上层

# ===== 选择进程 =====
Windows.label_AttachProcessPID = tk.Label(Windows.root, text=f'等待选择进程')
Windows.label_AttachProcessPID.grid(row=0, columnspan=2, column=1)


# ===== 注入进程 =====
def button_AttachProcess():
    Windows.root.attributes("-topmost", False)  # 设置窗口在最上层
    Cfg.selectedp = getAttachProcess(Windows.root)
    print('button_AttachProcess', Cfg.selectedp)
    Windows.label_AttachProcessPID.config(text=f'进程号:  {Cfg.selectedp[0]}; 窗口号:  {Cfg.selectedp[2]}')
    Windows.root.attributes("-topmost", True)  # 设置窗口在最上层

    Cfg.control = auto.ControlFromHandle(Cfg.selectedp[2])
    Cfg.ListControl = Cfg.control.ListControl()

    button_ListItem()

    Windows.root.after(500, clock_loop)


Windows.button_AttachProcess = tk.Button(Windows.root, text='注入进程', command=button_AttachProcess)
Windows.button_AttachProcess.grid(row=0, column=0)

# ===== 人物 =====
Windows.ddb_char = ddb_list(_cfg_json['ddb_char'], Cfg.encoding_list)
Windows.ddb_char.grid(row=3, column=0)

Windows.ddb_char_Item = ttk.Combobox()
Windows.ddb_char_Item.grid(row=3, column=1, columnspan=2)
# ===== 内容 =====
Windows.ddb_content = ddb_list(_cfg_json['ddb_content'], Cfg.encoding_list)
Windows.ddb_content.grid(row=4, column=0)

Windows.ddb_content_Item = ttk.Combobox()
Windows.ddb_content_Item.grid(row=4, column=1, columnspan=2)


# ===== 枚举列表 =====
def _updateDdbHooks(_ddb, _hooks, _current=0):
    _ddb['value'] = _hooks
    if not 0 <= _ddb.current() < len(_hooks):
        _ddb.current(min(_current, len(_hooks) - 1))


def button_ListItem():
    Cfg.ListItem = allControls(Cfg.ListControl)
    print(Cfg.ListItem)
    _hooks = list(Cfg.ListItem.keys())
    _updateDdbHooks(Windows.ddb_char_Item, _hooks)
    _updateDdbHooks(Windows.ddb_content_Item, _hooks)


Windows.button_ListItem = tk.Button(
    Windows.root,
    text='枚举列表',
    command=button_ListItem
)
Windows.button_ListItem.grid(row=3, column=3)

# ===== 捕获输出 =====
Windows.label_cb_n = tk.Label(Windows.root, text='旁白')
Windows.label_cb_n.grid(row=97, columnspan=4, sticky=tk.W)
Windows.label_cb_d = tk.Label(Windows.root, text=f'内容')
Windows.label_cb_d.grid(row=98, columnspan=4, sticky=tk.W)


def _cb_n():
    Windows.label_cb_n.config(text=Cfg.var_n[:10])


def _cb_d():
    Windows.label_cb_d.config(text=Cfg.var_d[:50])


def get_n():
    tmp = Cfg.ListItem[Windows.ddb_char_Item.get()].Name
    if Cfg.var_n != tmp:
        Cfg.var_n = tmp
        Windows.root.after(10, _cb_n)


def get_d():
    tmp = Cfg.ListItem[Windows.ddb_content_Item.get()].Name
    if Cfg.var_d != tmp:
        Cfg.var_d = tmp
        Windows.root.after(10, _cb_d)


# ===== 时钟循环 =====
def clock_loop():
    get_n()
    get_d()
    Windows.root.after(50, clock_loop)


# ===== 进入消息循环 =====
def on_closing():
    Windows.root.destroy()


Windows.root.protocol("WM_DELETE_WINDOW", on_closing)
Windows.root.mainloop()
