def startsWithAny(s: str, keys):
    for x in keys:
        if s.startswith(x):
            return x
    else:
        return False


def indexWithAny(s: str, keys):
    for x in keys:
        if x in s:
            idx = s.index(x)
            return x, s[:idx], s[idx:]
    else:
        return False


def endsWithAny(s: str, keys):
    for x in keys:
        if s.endswith(x):
            return x
    else:
        return False


def simpleSplit(_s: str, _sp, _st=0, _shift=True):
    _idx = _s.index(_sp, _st)
    if _shift:
        return _s[:_idx], _s[_idx + len(_sp):]
    else:
        return _s[:_idx], _s[_idx:]


brackets = {'「': '」', '『': '』', '（': '）', '“': '”'}  # , '【': '】'
brackets_r = {v: k for k, v in brackets.items()}

cache = []
cache_tmp = ''
cache_var_n = ''


def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.var_d
    if var_d.endswith(r'\@'):
        var_d = var_d[:-2]
    global cache, cache_tmp, cache_var_n
    var_d = var_d.strip()
    var_n: str = Cfg.var_n
    var_n = clearT(var_n).replace('???', '?')

    if cache:
        cache.append(var_d)
        if var_d.endswith(cache_tmp):
            sp = cache_var_n + '：' + clearT(' '.join(cache))
            cache = []
            return sp
        else:
            return ''

    tmp = startsWithAny(var_d, brackets)
    if tmp:
        if var_d.endswith(brackets[tmp]):
            return var_n + '：' + clearT(var_d)
        else:
            cache.append(var_d)
            cache_tmp = brackets[tmp]
            cache_var_n = var_n
            return ''
    else:
        return '旁白：' + clearT(var_d)
