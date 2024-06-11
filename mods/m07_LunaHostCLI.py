import subprocess
from threading import Thread
from queue import Queue, Empty


def enqueue_readline(out, q):
    while True:
        q.put(out.readline())


class LunaHook:
    allHooks = {}
    lastHook = ''

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

    def readline(self, timeout=0.1, block=True):
        try:
            line = self.q.get(block=block, timeout=timeout)
        except Empty:
            line = ''
        return line

    def attach(self, pid: int):
        self.exec(f'attach -P{pid}')
        self.printline()

    def detach(self, pid: int):
        self.exec(f'detach -P{pid}')
        self.printline()

    def onData(self, block=True, timeout=None):
        line: str = self.readline(timeout, block)
        if not line:
            return '', ''
        line = line.rstrip()
        if line.startswith('['):
            idx = line.index(']')
            hook, text = line[1:idx], line[idx + 1:]
            self.allHooks[hook] = text
            self.lastHook = hook
        else:
            self.allHooks[self.lastHook] += line
        return self.lastHook, self.allHooks[self.lastHook]


if __name__ == '__main__':
    tmp = LunaHook(r'D:\scn\LunaTranslator\Release_Chinese\LunaHostCLI64.exe')
    tmp.attach(2744)
    print(tmp.onData())
    tmp.detach(2744)
