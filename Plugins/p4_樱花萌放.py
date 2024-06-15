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


def getPrevLine(Cfg, var_d):
    tmp: str = Cfg.oldText
    idx_r = tmp.rindex(var_d) - 2
    idx_l = tmp.rindex('\r\n', 0, idx_r)
    var_n = tmp[idx_l + 2:idx_r]
    return var_n


def log_process(clearT, Cfg, Windows):
    global oldLine
    var_d: str = Cfg.GetEditText()
    if var_d == '空':
        return ''
    tmp = endsWithAny(var_d, brackets_r.keys())
    if not tmp:
        var_n = '旁白'
        if '「' in var_d and '」' not in var_d:
            return ''
        if '『' in var_d and '』' not in var_d:
            return ''
    else:
        if var_d.startswith(brackets_r[tmp]):
            var_n = getPrevLine(Cfg, var_d)
        else:
            if brackets_r[tmp] in var_d:
                idx = var_d.index(brackets_r[tmp])
            else:
                var_d += (getPrevLine(Cfg, var_d) + '\r\n')
                idx = var_d.index(brackets_r[tmp])
            if idx > 5:
                var_n = '旁白'
            elif idx == 0:
                var_n = getPrevLine(Cfg, var_d)
            else:
                var_n = var_d[:idx]
                var_d = var_d[idx:]

    var_d = var_d.replace('\n', '').replace('\r', '')
    if not var_d.startswith('「') and oldLine and var_d != oldLine and oldLine.endswith(var_d):
        return ''
    oldLine = var_d
    return clearT(var_n) + '：' + clearT(var_d)
