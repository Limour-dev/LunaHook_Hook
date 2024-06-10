import subprocess
from threading import Thread
from queue import Queue, Empty


class LunaTextOutputObject:
    def __init__(self,
                 handle: int,
                 pid: int,
                 addr: int,
                 ctx: int,
                 ctx2: int,
                 name: str,
                 code: str,
                 text: str):
        self.handle = handle
        self.pid = pid
        self.addr = addr
        self.ctx = ctx
        self.ctx2 = ctx2
        self.name = name
        self.code = code
        self.text = text


def enqueue_readline(out, q):
    while True:
        q.put(out.readline())


class LunaHook:
    def __init__(self, CLI_path: str):
        self.cli = subprocess.Popen(
            CLI_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-16le"
        )

        self.q = Queue()
        self.t = Thread(target=enqueue_readline, args=(self.cli.stdout, self.q), daemon=True)
        self.t.start()

        self.printline()

    def printline(self):
        while True:
            line = self.readline()
            if line:
                print(line.strip())
            else:
                break

    def exec(self, cmd: str):
        self.cli.stdin.write(cmd + '\n')
        self.cli.stdin.flush()

    def readline(self, timeout=0.1):
        try:
            line = self.q.get(timeout=timeout)
        except Empty:
            line = ''
        return line

    def attach(self, pid: int):
        self.exec(f'attach -P{pid}')
        self.printline()

    def detach(self, pid: int):
        self.exec(f'detach -P{pid}')
        self.printline()


if __name__ == '__main__':
    tmp = LunaHook(r'D:\scn\LunaTranslator\Release_Chinese\LunaHostCLI64.exe')
    tmp.attach(24636)
    tmp.detach(24636)
