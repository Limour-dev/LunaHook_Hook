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


brackets = {'「': '」', '『': '』', '（': '）', '【': '】', '“': '”'}
brackets_r = {v: k for k, v in brackets.items()}

cache = []
cache_tmp = ''
cache_var_n = ''

sysT = {'快速保存。', '文本自动推进。', '快进。', '打开设置界面。',
        '打开历史界面。', '打开读取界面。', '打开保存界面。',
        '快速读取。', '快速保存。'}


def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.var_d
    if var_d.strip() in sysT:
        return ''
    tmp = endsWithAny(var_d, brackets_r.keys())
    tmp2 = ''
    if tmp == '）' and '（' in var_d:
        _var_d = var_d[:var_d.rindex('（')].rstrip()
        tmp2 = endsWithAny(_var_d, brackets_r.keys())
        if tmp2:
            tmp = tmp2
            tmp2 = var_d[var_d.rindex('（'):]
            var_d = _var_d
        else:
            tmp2 = ''

    global cache, cache_tmp, cache_var_n
    if not tmp:
        if cache:
            cache.append(var_d)
            return ''
        tmp = indexWithAny(var_d, brackets.keys())
        if not tmp or brackets[tmp[0]] in var_d:
            return '旁白：' + clearT(var_d)
        else:
            cache_var_n = tmp[1]
            cache_tmp = tmp[0]
            cache.append(tmp[2])
            return ''
    else:
        if cache:
            var_n = cache_var_n
            cache.append(var_d)
            var_d = ' '.join(cache)
            cache = []
            return clearT(var_n) + ('：' if brackets_r[tmp] == cache_tmp else '<sp>：') + clearT(var_d + tmp2)

        elif brackets_r[tmp] in var_d:
            idx = var_d.index(brackets_r[tmp])
            var_n = var_d[:idx]
            var_d = var_d[idx:]
            return clearT(var_n) + '：' + clearT(var_d + tmp2)
        else:
            return '旁白<sp>：' + clearT(var_d + tmp2)  # 标记一下，后期手动处理
