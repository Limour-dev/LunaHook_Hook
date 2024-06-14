oldLine = ''

brackets = {'「': '」', '（': '）', '『': '』', '【': '】'}

brackets_r = {v: k for k, v in brackets.items()}


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


def log_process(clearT, Cfg, Windows):
    global oldLine
    var_d: str = Cfg.GetEditText()
    if var_d == '空':
        return ''
    tmp = endsWithAny(var_d, brackets_r.keys())
    if not tmp:
        var_n = '旁白'
    else:
        if var_d.startswith(brackets_r[tmp]):
            tmp: str = Cfg.oldText
            idx_r = tmp.rindex(var_d) - 2
            idx_l = tmp.rindex('\r\n', 0, idx_r)
            var_n = tmp[idx_l + 2:idx_r]
        else:
            idx = var_d.index(brackets_r[tmp])
            if idx > 5:
                var_n = '旁白'
            else:
                var_n = var_d[:idx]
                var_d = var_d[idx:]
    var_d = var_d.replace('\n', '').replace('\r', '')
    if not var_d.startswith('「') and oldLine and var_d != oldLine and oldLine.endswith(var_d):
        return ''
    oldLine = var_d
    return clearT(var_n) + '：' + clearT(var_d)
