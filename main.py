# mamba create -n uiautomation conda-forge::uiautomation

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkf
from tkinter import messagebox

try:
    import uiautomation as auto
except ModuleNotFoundError:
    print('uiautomation 缺失，GUI后端失效')


    class auto:
        ControlFromHandle = None
        ListControl = None
        EditControl = None
        GetClipboardText = None

import mods.m03_windows as windows
from mods.m05_attachprocess import getAttachProcess
from mods.m06_clearT import clearT, get_all_files_in_directory
from mods.m07_LunaHostCLI import LunaHook

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
    'backendType': 2,
    'label_log': r'D:\datasets\tmp\1.txt',
    'label_cli_path': r'D:\scn\LunaTranslator\Release_Chinese\LunaHostCLI64.exe',
    'entry_delay': 5
}

if os.path.exists('config.json'):
    with open(r'config.json', 'r', encoding='utf-8') as f:
        _cfg_json.update(json.load(f))


def GetEditText():
    if Cfg.backendType.get() == 1:
        tmp = _GetEditText(Cfg.EditControl.NativeWindowHandle)
        prefix = '\r\n' + Cfg.var_d[:10]
        try:
            retn = tmp[tmp.rindex(prefix) + 2:]
        except ValueError:
            if tmp.startswith('\r\n'):
                retn = tmp[tmp.rindex('\r\n') + 2:]
            else:
                if len(Cfg.oldText) < len(tmp):
                    retn = tmp[len(Cfg.oldText):].strip()
                    if len(retn) < len(Cfg.var_d):
                        retn = Cfg.var_d
                else:
                    retn = Cfg.var_d
        Cfg.oldText = tmp
        return retn
    else:
        return Cfg.var_d


class Cfg:
    selectedp: tuple = tuple()
    control: auto.ControlFromHandle
    ListControl: auto.ListControl
    ListItem: dict
    EditControl: auto.EditControl
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
    # ===== 获取长文 =====
    GetClipboardText = auto.GetClipboardText
    oldText = ''
    GetEditText = GetEditText
    # ===== 后端选择 =====
    backendType: tk.IntVar
    lunaHook: LunaHook
    entry_delay: tk.IntVar


def _GetEditText(handle: int) -> str:
    """
    Get text of a native Win32 Edit.
    handle: int, the handle of a native window.
    Return str.
    """
    textLen = auto.SendMessage(handle, 0x000E, 0, 0) + 1  # WM_GETTEXTLENGTH
    arrayType = auto.ctypes.c_wchar * textLen
    values = arrayType()
    auto.SendMessage(handle, 0x000D, textLen, auto.ctypes.addressof(values))  # WM_GETTEXT
    return values.value


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
    button_char_fix: tk.Button
    # ===== 插件选择 =====
    ddb_plugin: ttk.Combobox
    # ===== 后端选择 =====
    rb_backend_gui: tk.Radiobutton
    rb_backend_cli: tk.Radiobutton
    entry_delay: tk.Entry
    # ===== CLI路径 =====
    label_cli_path: tk.Label
    button_cli_path: tk


# ===== 初始化窗口 =====
Windows.root.title("LunaHook_log v0.2 " + ("管理员" if windows.IsUserAnAdmin() else "非管理员"))  # 窗口名
Windows.root.geometry('720x320+10+10')  # axb为窗口大小，+10 +10 定义窗口弹出时的默认展示位置

Windows.root.attributes("-topmost", True)  # 设置窗口在最上层

# ===== 后端选择 =====
Cfg.backendType = tk.IntVar(Windows.root, value=_cfg_json['backendType'])
Windows.rb_backend_gui = tk.Radiobutton(Windows.root, text="GUI", variable=Cfg.backendType, value=1)
Windows.rb_backend_cli = tk.Radiobutton(Windows.root, text="CLI", variable=Cfg.backendType, value=2)
Windows.rb_backend_gui.grid(row=102, column=0)
Windows.rb_backend_cli.grid(row=102, column=1)

# ===== CLI路径 =====
Windows.label_cli_path = tk.Label(Windows.root, text=_cfg_json['label_cli_path'])
Windows.label_cli_path.grid(row=103, column=1, columnspan=4)


def button_cli_path():
    _dir, _file = os.path.split(_cfg_json['label_cli_path'])
    _askd_path = tkf.askopenfilename(
        title='LunaHostCLI.exe 路径',
        initialdir=_dir,
        initialfile=_file,
        filetypes=(('可执行文件', '.exe'),)
    )
    if not _askd_path:
        return
    _cfg_json['label_cli_path'] = _askd_path
    Windows.label_cli_path.config(text=_askd_path)


Windows.button_cli_path = tk.Button(
    Windows.root,
    text='选择 LunaHostCLI 路径',
    command=button_cli_path
)
Windows.button_cli_path.grid(row=103, column=0)

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

    if Cfg.backendType.get() == 1:
        Cfg.control = auto.ControlFromHandle(Cfg.selectedp[2])
        Cfg.ListControl = Cfg.control.ListControl()

        button_ListItem()

        Cfg.EditControl = Cfg.control.EditControl(foundIndex=2)

        Windows.root.after(500, clock_loop_gui)
    else:
        Cfg.lunaHook = LunaHook(_cfg_json['label_cli_path'])
        for pid in Cfg.selectedp[0]:
            Cfg.lunaHook.attach(pid)
        Windows.root.after(500, clock_loop_cli)


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
    if Cfg.backendType.get() == 1:
        Cfg.ListItem = allControls(Cfg.ListControl)
        print(Cfg.ListItem)
        _cfg_json['allHooks'] = list(Cfg.ListItem.keys())
    else:
        _cfg_json['allHooks'] = list(Cfg.lunaHook.allHooks.keys())
    _updateDdbHooks(Windows.ddb_char_Item, _cfg_json['allHooks'])
    _updateDdbHooks(Windows.ddb_content_Item, _cfg_json['allHooks'])


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


def get_n_gui():
    tmp = Cfg.ListItem[Windows.ddb_char_Item.get()].Name
    if Cfg.var_n != tmp:
        Cfg.var_n = tmp
        Windows.root.after(10, _cb_n)


def get_d_gui():
    tmp = Cfg.ListItem[Windows.ddb_content_Item.get()].Name
    if Cfg.var_d != tmp:
        Windows.root.after(_cfg_json['entry_delay'] * 3, get_n_gui)
        Cfg.var_d = tmp
        Windows.root.after(_cfg_json['entry_delay'] * 3 + 5, log_process)
        Windows.root.after(10, _cb_d)


# ===== 时钟循环 =====
Cfg.entry_delay = tk.IntVar(Windows.root, value=_cfg_json['entry_delay'])
Windows.entry_delay = tk.Entry(Windows.root, textvariable=Cfg.entry_delay)
Windows.entry_delay.grid(row=102, column=2)


def entry_delay(a, b, c):
    _cfg_json['entry_delay'] = Cfg.entry_delay.get()
    print('entry_delay', _cfg_json['entry_delay'], c)


Cfg.entry_delay.trace('w', entry_delay)


def clock_loop_gui():
    try:
        get_d_gui()
    finally:
        Windows.root.after(_cfg_json['entry_delay'], clock_loop_gui)


clock_loop_hook_cache = {}


def clock_loop_cli_hook_cache():
    global clock_loop_hook_cache
    while True:
        hook, tmp = Cfg.lunaHook.onData(block=False)
        if not hook:
            break
        print(hook, tmp)
        clock_loop_hook_cache[hook] = clock_loop_hook_cache.get(hook, '') + tmp


def clock_loop_cli_b():
    global clock_loop_hook_cache
    try:
        clock_loop_cli_hook_cache()
        for hook, tmp in clock_loop_hook_cache.items():
            if hook == Windows.ddb_content_Item.get():
                Cfg.var_d = tmp
                Windows.root.after(10, _cb_d)
                Windows.root.after(_cfg_json['entry_delay'], log_process)
            elif hook == Windows.ddb_char_Item.get():
                Cfg.var_n = tmp
                Windows.root.after(10, _cb_n)
    finally:
        clock_loop_hook_cache = {}
        Windows.root.after(_cfg_json['entry_delay'], clock_loop_cli)


def clock_loop_cli():
    clock_loop_cli_hook_cache()
    if clock_loop_hook_cache:
        Windows.root.after(_cfg_json['entry_delay'], clock_loop_cli_b)
    else:
        Windows.root.after(_cfg_json['entry_delay'], clock_loop_cli)


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

log_process_oldLine = ''


def log_process():
    line = Cfg.plugin.log_process(clearT, Cfg, Windows)
    print('log_process', line)
    if (not Cfg.log) or not Cfg.var_d:
        return
    if line:
        global log_process_oldLine
        if log_process_oldLine != line:
            Cfg.log_add_size += Cfg.log_file.write(line + '\n')
            log_process_oldLine = line


# ===== 插件选择 =====
plugins_path = [x[:-3] for x in os.listdir('Plugins') if x.endswith('.py')]
Windows.ddb_plugin = ddb_list(_cfg_json['ddb_plugin'], plugins_path)
Windows.ddb_plugin.grid(row=101, column=0)
Cfg.plugin = importlib.import_module('.' + Windows.ddb_plugin.get(), 'Plugins')


@Windows.root.register
def ddb_plugin_update():
    _plugin = Windows.ddb_plugin.get()
    if Cfg.plugin.__name__.endswith(_plugin):
        Cfg.plugin = importlib.reload(Cfg.plugin)
        print('reload', Cfg.plugin)
    else:
        Cfg.plugin = importlib.import_module('.' + _plugin, 'Plugins')
        print('import_module', Cfg.plugin)


Windows.ddb_plugin.bind('<<ComboboxSelected>>', ddb_plugin_update)


# ===== 人名后处理 =====
def button_char_find():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _a = get_all_files_in_directory(_dir, '.txt')
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
    with open(os.path.join(_dir, 'name_map.json'), 'w', encoding='utf-8') as _f:
        json.dump(_n, _f, ensure_ascii=False, indent=4)


Windows.button_char_find = tk.Button(
    Windows.root,
    text='生成人名映射表',
    command=button_char_find
)
Windows.button_char_find.grid(row=101, column=1)


def button_char_map():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _a = get_all_files_in_directory(_dir, '.txt')
    with open(os.path.join(_dir, 'name_map.json'), 'r', encoding='utf-8') as _f:
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


def simpleSplit(_s: str, _sp, _st=0, _shift=True):
    _idx = _s.find(_sp, _st)
    if _idx < 0:
        return '', _s
    if _shift:
        return _s[:_idx], _s[_idx + len(_sp):]
    else:
        return _s[:_idx], _s[_idx:]


def button_char_fix():
    _dir, _file = os.path.split(_cfg_json['label_log'])
    _a = get_all_files_in_directory(_dir, '.txt')
    for _path in _a:
        with open(_path, 'r', encoding='utf-8') as _f:
            _lines = _f.readlines()
        _n = set()
        for _line in _lines:
            n, d = simpleSplit(_line, '：')
            if n and n != '旁白':
                _n.add(n)
        _res_lines = []
        _cache = ''
        import re
        _re_rep = re.compile(r'^(.+?)\1+$')
        for _line in _lines:
            if _cache:
                n, d = simpleSplit(_cache, '：')
                _pre_n, _pre_d = simpleSplit(_line, '：')
                if _pre_n == '旁白':
                    _pre_d: str = _pre_d.strip()
                    if _pre_d in _n:
                        _res_lines.append(_pre_d + '：' + d)
                        _cache = ''
                        continue
                    _tmp = _re_rep.findall(_pre_d)
                    if len(_tmp) == 1:
                        _pre_d = _tmp[0]
                        if _pre_d in _n:
                            _res_lines.append(_pre_d + '：' + d)
                            _cache = ''
                            continue
                _res_lines.append('<sp>' + _cache)
                _cache = ''

            n, d = simpleSplit(_line, '：')
            if not n:
                if _res_lines:
                    _pre_n, _pre_d = simpleSplit(_res_lines[-1], '：')
                    if _pre_n == '旁白':
                        _pre_d: str = _pre_d.strip()
                        if _pre_d in _n:
                            _res_lines[-1] = _pre_d + '：' + d
                            continue
                        _tmp = _re_rep.findall(_pre_d)
                        if len(_tmp) == 1:
                            _pre_d = _tmp[0]
                            if _pre_d in _n:
                                _res_lines[-1] = _pre_d + '：' + d
                                continue
                _cache = _line
                continue
            _res_lines.append(_line)
        else:
            if _cache:
                _res_lines.append('<sp>' + _cache)
        try:
            with open(_path, 'w', encoding='utf-8') as _f:
                _f.writelines(_res_lines)
        except Exception as e:
            with open(_path, 'w', encoding='utf-8') as _f:
                _f.writelines(_lines)
            raise e

        print(_path, 'done')


Windows.button_char_fix = tk.Button(
    Windows.root,
    text='错行修复',
    command=button_char_fix
)
Windows.button_char_fix.grid(row=101, column=3)


# ===== 进入消息循环 =====
def on_closing():
    if Cfg.log:
        button_log_control()
    if messagebox.askokcancel("保存", "保存当前状态?"):
        _cfg_json['ddb_char'] = Windows.ddb_char.current()
        _cfg_json['ddb_content'] = Windows.ddb_content.current()
        _cfg_json['ddb_char_Item'] = Windows.ddb_char_Item.current()
        _cfg_json['ddb_content_Item'] = Windows.ddb_content_Item.current()
        _cfg_json['ddb_plugin'] = Windows.ddb_plugin.current()
        _cfg_json['backendType'] = Cfg.backendType.get()
        # ===== 持久化设置 =====
        with open(r'config.json', 'w', encoding='utf-8') as f:
            json.dump(_cfg_json, f, ensure_ascii=False, indent=4)

    if Cfg.backendType.get() == 2 and Cfg.selectedp:
        for pid in Cfg.selectedp[0]:
            Cfg.lunaHook.detach(pid)

    Windows.root.destroy()


Windows.root.protocol("WM_DELETE_WINDOW", on_closing)
Windows.root.mainloop()
