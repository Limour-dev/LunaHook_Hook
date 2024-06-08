import threading
import time
import tkinter
import os

try:
    import m03_windows as windows
except ModuleNotFoundError as e:
    import mods.m03_windows as windows


def getpidexe(pid):
    hwnd1 = windows.AutoHandle(
        windows.OpenProcess(windows.PROCESS_ALL_ACCESS, False, (pid))
    )
    if hwnd1 == 0:
        hwnd1 = windows.OpenProcess(
            windows.PROCESS_QUERY_LIMITED_INFORMATION, False, (pid)
        )
    if hwnd1 == 0:
        name_ = None
    else:
        name_ = windows.GetProcessFileName(hwnd1)
    return name_


def getprocesslist():
    pids = windows.EnumProcesses()
    return pids


def ListProcess(filt=True):
    ret = []
    pids = getprocesslist()
    for pid in pids:
        if os.getpid() == pid:
            continue
        try:
            name_ = getpidexe(pid)
            if name_ is None:
                continue
            name = name_.lower()
            if filt:
                if (
                        ":\\windows\\" in name
                        or "\\microsoft\\" in name
                        or "\\windowsapps\\" in name
                ):
                    continue
            ret.append([pid, name_])
        except:
            pass
    kv = {}
    for pid, exe in ret:
        if exe in kv:
            kv[exe]["pid"].append(pid)
        else:
            kv[exe] = {"pid": [pid]}
    # for exe in kv:
    #         if len(kv[exe]['pid'])>1:
    #                 mems=[getprocessmem(_) for _ in kv[exe]['pid']]
    #                 _i=argsort(mems)
    #                 kv[exe]['pid']=[kv[exe]['pid'][_i[-1]]]
    xxx = []
    for exe in kv:
        xxx.append([kv[exe]["pid"], exe])
    return xxx


def getPidByPath(_path, _pid=None):
    _lps = ListProcess(False)
    _pids = None
    for pids, _exe in _lps:
        if _exe == _path:
            _pids = pids
            break
    return _pids if _pids else [_pid]


def mouseselectwindow(callback):
    def _loop():
        while True:
            keystate = windows.GetKeyState(
                windows.VK_LBUTTON
            )  # 必须使用GetKeyState, GetAsyncKeyState或SetWindowHookEx都无法检测到高权限应用上的点击事件。
            if keystate < 0:
                break
            time.sleep(0.01)
        try:
            pos = windows.GetCursorPos()
            hwnd = windows.GetAncestor(windows.WindowFromPoint(pos))
            pid = windows.GetWindowThreadProcessId(hwnd)
            callback(pid, hwnd)
        except:
            pass

    threading.Thread(target=_loop).start()


class AttachProcessDialog:
    selectedp: tuple

    def __init__(self, _callback):
        self._callback = _callback

    def selectwindowcallback(self, pid, hwnd):
        if pid == os.getpid():
            return
        name = getpidexe(pid)
        _pids = getPidByPath(name, pid)
        self.selectedp = (_pids, name, hwnd)
        self._callback(self.selectedp)


def getAttachProcess(_top=None):
    if _top is None:
        root = tkinter.Tk()
    else:
        root = tkinter.Toplevel(_top)
    # ===== 初始化窗口 =====
    root.title("LunaHook_log AttachProcessDialog " + "管理员" if windows.IsUserAnAdmin() else "非管理员")  # 窗口名
    root.geometry('480x120+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
    # ===== 展现获取的信息 =====
    t_pid = tkinter.Label(root, text='进程号: ')
    t_pid.grid(row=1, sticky=tkinter.W)
    t_hwnd = tkinter.Label(root, text='窗口名: ')
    t_hwnd.grid(row=2, sticky=tkinter.W)
    t_name = tkinter.Label(root, text='程序名: ')
    t_name.grid(row=3, sticky=tkinter.W)

    # ===== 唯一的功能 =====
    def btn_01_cb(selectedp):
        t_pid.config(text=f'进程号: {selectedp[0]}')
        t_hwnd.config(text=f'窗口名: {windows.GetWindowText(selectedp[2])}')
        t_name.config(text=f'程序名: {selectedp[1]}')

    retn = AttachProcessDialog(btn_01_cb)

    def btn_01():
        mouseselectwindow(retn.selectwindowcallback)

    button = tkinter.Button(root, command=btn_01, text='点击此按钮后点击游戏窗口')
    button.grid(row=0, sticky=tkinter.W)
    # ===== 进入消息循环 =====
    if _top is None:
        root.mainloop()
    else:
        _top.wait_window(root)
    # ===== 返回选择的进程 =====
    return retn.selectedp


if __name__ == '__main__':
    print(getAttachProcess())
