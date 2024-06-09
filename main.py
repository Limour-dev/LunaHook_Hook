# mamba create -n uiautomation conda-forge::uiautomation

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkf
from tkinter import messagebox
import uiautomation as auto

import mods.m03_windows as windows
from mods.m05_attachprocess import getAttachProcess
from mods.m06_clearT import clearT, get_all_files_in_directory

import os, json
from io import TextIOWrapper
import importlib

_cfg_json = {
    'ddb_char': 2,
    'ddb_content': 2,
    'allHooks': [],
    'ddb_char_Item': 0,
    'ddb_content_Item': 0,
    'ddb_plugin': 0,
    'label_log': r'D:\datasets\tmp\1.txt'
}

if os.path.exists('config.json'):
    with open(r'config.json', 'r', encoding='utf-8') as f:
        _cfg_json.update(json.load(f))


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
    # ===== 日志记录 =====
    log = False
    log_file: TextIOWrapper
    log_add_size: int = 0
    # ===== 插件选择 =====
    plugin: importlib.import_module
    GetClipboardText = auto.GetClipboardText


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
    if _list:
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
    # ===== 日志记录 =====
    label_log: tk.Label
    button_log: tk.Button
    button_log_control: tk.Button
    # ===== 人名后处理 =====
    button_char_find: tk.Button
    button_char_map: tk.Button
    # ===== 插件选择 =====
    ddb_plugin: ttk.Combobox


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.2 " + ("管理员" if windows.IsUserAnAdmin() else "非管理员"))  # 窗口名
Windows.root.geometry('640x320+10+10')  # axb为窗口大小，+10 +10 定义窗口弹出时的默认展示位置

Windows.root.attributes("-topmost", True)  # 设置窗口在最上层

# ===== 选择进程 =====
Windows.label_AttachProcessPID = tk.Label(Windows.root, text=f'等待选择窗口')
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


Windows.button_AttachProcess = tk.Button(Windows.root, text='选择窗口', command=button_AttachProcess)
Windows.button_AttachProcess.grid(row=0, column=0)

# ===== 人物 =====
Windows.ddb_char = ddb_list(_cfg_json['ddb_char'], Cfg.encoding_list)
Windows.ddb_char.grid(row=3, column=0)

Windows.ddb_char_Item = ddb_list(_cfg_json['ddb_char_Item'], _cfg_json['allHooks'])
Windows.ddb_char_Item.grid(row=3, column=1, columnspan=2)
# ===== 内容 =====
Windows.ddb_content = ddb_list(_cfg_json['ddb_content'], Cfg.encoding_list)
Windows.ddb_content.grid(row=4, column=0)

Windows.ddb_content_Item = ddb_list(_cfg_json['ddb_content_Item'], _cfg_json['allHooks'])
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
    Windows.label_cb_d.config(text=Cfg.var_d[:35])


def get_n():
    tmp = Cfg.ListItem[Windows.ddb_char_Item.get()].Name
    if Cfg.var_n != tmp:
        Cfg.var_n = tmp
        Windows.root.after(10, _cb_n)


def get_d():
    tmp = Cfg.ListItem[Windows.ddb_content_Item.get()].Name
    if Cfg.var_d != tmp:
        Windows.root.after(5, get_n)
        Cfg.var_d = tmp
        Windows.root.after(9, log_process)
        Windows.root.after(10, _cb_d)


# ===== 时钟循环 =====
def clock_loop():
    get_d()
    Windows.root.after(50, clock_loop)


# ===== 日志记录 =====
Windows.label_log = tk.Label(Windows.root, text=_cfg_json['label_log'])
Windows.label_log.grid(row=100, column=1, columnspan=4)


def button_log():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _askd_path = tkf.asksaveasfilename(
        title='Log 路径',
        initialdir=_dir,
        initialfile=_file
    )
    if not _askd_path:
        return
    _cfg_json['label_log'] = os.path.abspath(_askd_path)
    Windows.label_log.config(text=_cfg_json['label_log'])


Windows.button_log = tk.Button(
    Windows.root,
    text='选择 Log 路径',
    command=button_log
)
Windows.button_log.grid(row=100, column=0)


def button_log_control():
    if not Cfg.log:
        Windows.button_log_control.config(text='暂停记录')
        Cfg.log_file = open(_cfg_json['label_log'], 'a', encoding='utf-8')
    else:
        Windows.button_log_control.config(text='继续记录')
        Cfg.log_file.close()
    Cfg.log = not Cfg.log


Windows.button_log_control = tk.Button(
    Windows.root,
    text='开始记录',
    command=button_log_control
)
Windows.button_log_control.grid(row=101, column=5)


def log_flush():
    try:
        if (not Cfg.log) or not Cfg.var_d:
            return
        if Cfg.log_add_size > 0:
            Cfg.log_file.flush()
            Cfg.log_add_size = 0
    finally:
        Windows.root.after(2000, log_flush)


Windows.root.after(2000, log_flush)


def log_process():
    line = Cfg.plugin.log_process(clearT, Cfg, Windows)
    print('log_process', line)
    if (not Cfg.log) or not Cfg.var_d:
        return
    if line:
        Cfg.log_add_size += Cfg.log_file.write(line + '\n')


# ===== 插件选择 =====
plugins_path = [x[:-3] for x in os.listdir('Plugins') if x.endswith('.py')]
Windows.ddb_plugin = ddb_list(_cfg_json['ddb_plugin'], plugins_path)
Windows.ddb_plugin.grid(row=101, column=0)
Cfg.plugin = importlib.import_module('.' + Windows.ddb_plugin.get(), 'Plugins')


@Windows.root.register
def ddb_plugin_update():
    _plugin = Windows.ddb_plugin.get()
    Cfg.plugin = importlib.import_module('.' + _plugin, 'Plugins')
    print(Cfg.plugin)


Windows.ddb_plugin.bind('<<ComboboxSelected>>', ddb_plugin_update)


# ===== 人名后处理 =====
def button_char_find():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _a = get_all_files_in_directory(_dir)
    _n = {}
    for _path in _a:
        with open(_path, 'r', encoding='utf-8') as _f:
            for _line in _f:
                if '：' in _line:
                    _idx = _line.index('：')
                    n = _line[:_idx]
                    if n in _n:
                        pass
                    else:
                        _n[n] = n
                        print(_line)
    with open('name_map.json', 'w', encoding='utf-8') as _f:
        json.dump(_n, _f, ensure_ascii=False, indent=4)


Windows.button_char_find = tk.Button(
    Windows.root,
    text='生成人名映射表',
    command=button_char_find
)
Windows.button_char_find.grid(row=101, column=1)


def button_char_map():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _a = get_all_files_in_directory(_dir)
    with open('name_map.json', 'r', encoding='utf-8') as _f:
        _n: dict = json.load(_f)
    for _path in _a:
        with open(_path, 'r', encoding='utf-8') as _f:
            _lines = _f.readlines()
        with open(_path + '.map.txt', 'w', encoding='utf-8') as _f:
            for _line in _lines:
                if '：' in _line:
                    _idx = _line.index('：')
                    n = _line[:_idx]
                    n = _n.get(n, n)
                    _f.write(n + '：' + _line[_idx + 1:])
                else:
                    _f.write(_line)


Windows.button_char_map = tk.Button(
    Windows.root,
    text='应用人名映射表',
    command=button_char_map
)
Windows.button_char_map.grid(row=101, column=2)


# ===== 进入消息循环 =====
def on_closing():
    if Cfg.log:
        button_log_control()
    if messagebox.askokcancel("保存", "保存当前状态?"):
        _cfg_json['ddb_char'] = Windows.ddb_char.current()
        _cfg_json['ddb_content'] = Windows.ddb_content.current()
        _cfg_json['allHooks'] = list(Cfg.ListItem.keys())
        _cfg_json['ddb_char_Item'] = Windows.ddb_char_Item.current()
        _cfg_json['ddb_content_Item'] = Windows.ddb_content_Item.current()
        _cfg_json['ddb_plugin'] = Windows.ddb_plugin.current()
        # ===== 持久化设置 =====
        with open(r'config.json', 'w', encoding='utf-8') as f:
            json.dump(_cfg_json, f, ensure_ascii=False, indent=4)
    Windows.root.destroy()


Windows.root.protocol("WM_DELETE_WINDOW", on_closing)
Windows.root.mainloop()