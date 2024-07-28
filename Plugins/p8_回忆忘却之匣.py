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
    global cache, cache_tmp, cache_var_n
    var_d = var_d.strip()
    if var_d.startswith('【'):
        var_n, var_d = simpleSplit(var_d, '】')
        var_d = var_d.strip()
        var_n = clearT(var_n[1:]).replace('???', '?')
        if cache:
            sp = cache_var_n + '<sp>：' + clearT(' '.join(cache)) + '\n' # 标记一下，后期手动处理
            cache = []
        else:
            sp = ''

        tmp = startsWithAny(var_d, brackets)
        if tmp:
            if var_d.endswith(brackets[tmp]):
                return sp + var_n + '：' + clearT(var_d)
            else:
                cache.append(var_d)
                cache_tmp = brackets[tmp]
                cache_var_n = var_n
                return sp.rstrip()
        else:
            return sp + var_n + '<sp>：' + clearT(var_d)  # 标记一下，后期手动处理
    else:
        if cache:
            cache.append(var_d)
            if var_d.endswith(cache_tmp):
                sp = cache_var_n + '：' + clearT(' '.join(cache))
                cache = []
                return sp
            else:
                return ''
        else:
            return '旁白：' + clearT(var_d)
