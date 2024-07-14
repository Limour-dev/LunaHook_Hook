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

cache = []
cache_tmp = ''
cache_var_n = ''


def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.var_d
    var_d = var_d.strip()

    tmp = startsWithAny(var_d, brackets.keys())
    if tmp != '（' and var_d.endswith('）') and '（' in var_d:
        _var_d = var_d[:var_d.rindex('（')].rstrip()
    else:
        _var_d = var_d

    global cache, cache_tmp, cache_var_n
    if cache_tmp:
        if _var_d.endswith(brackets[cache_tmp]):
            var_n = cache_var_n
            cache.append(var_d)
            cache_tmp = ''
            var_d = ' '.join(cache)
            cache = []
            line = clearT(var_n) + '：' + clearT(var_d)
        else:
            if tmp and _var_d.endswith(brackets[tmp]):
                line = clearT(cache_var_n) + '：' + clearT(' '.join(cache)) + '\n'
                cache = []
                cache_tmp = ''
                var_n = Cfg.var_n
                line += clearT(var_n) + '：' + clearT(var_d)
            else:
                cache.append(var_d)
                print('cache', cache_var_n, cache)
                return ''

    else:
        if tmp and _var_d.endswith(brackets[tmp]):
            var_n = Cfg.var_n
        else:
            if tmp and (brackets[tmp] not in _var_d):
                cache_var_n = Cfg.var_n
                cache.append(var_d)
                cache_tmp = tmp
                print('cache', cache_var_n, cache)
                return ''

            var_n = '旁白'

        line = clearT(var_n) + '：' + clearT(var_d)

    return line
