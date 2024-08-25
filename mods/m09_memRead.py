from pymem import Pymem


def str2ce(_s: str, _encode):
    _hex = _s.encode(_encode).hex(sep=' ')
    return _hex


class MemRead:
    def __init__(self, _game: Pymem, _address: str, _encoding: str, _len: int = 50):
        self._game = _game
        self._address = int(_address, 16)
        self._encoding = _encoding
        self._len = _len

    def __call__(self):
        tmp = self._game.read_bytes(self._address, self._len)
        tmp = tmp.decode(self._encoding, errors='ignore')
        try:
            _idx = tmp.index('\x00')
            tmp = tmp[:_idx]
        except ValueError as e:
            print(tmp)
        tmp = tmp.rstrip('\x00')
        return tmp

