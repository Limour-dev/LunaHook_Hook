def startsWithAny(s: str, keys):
    for x in keys:
        if s.startswith(x):
            return x
    else:
        return False


def endsWithAny(s: str, keys):
    for x in keys:
        if s.endswith(x):
            return x
    else:
        return False


brackets = {'「': '」', '（': '）', '『': '』', '【': '】', '“': '”'}

oldLine = ''


def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.var_d
    var_d = var_d.strip()
    tmp = startsWithAny(var_d, brackets.keys())
    if tmp and var_d.endswith(brackets[tmp]):
        var_n = Cfg.var_n
    else:
        var_n = '旁白'
    line = clearT(var_n) + '：' + clearT(var_d)
    global oldLine
    if oldLine != line:
        oldLine = line
    else:
        return ''
    return line
