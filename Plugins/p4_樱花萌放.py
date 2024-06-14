oldLine = ''


def log_process(clearT, Cfg, Windows):
    global oldLine
    var_d: str = Cfg.GetEditText()
    if var_d == '空':
        return ''
    if not var_d.endswith('」'):
        var_n = '旁白'
    else:
        if var_d.startswith('「'):
            tmp: str = Cfg.oldText
            idx_r = tmp.rindex(var_d) - 2
            idx_l = tmp.rindex('\r\n', 0, idx_r)
            var_n = tmp[idx_l+2:idx_r]
        else:
            idx = var_d.index('「')
            var_n = var_d[:idx]
            var_d = var_d[idx:]
    var_d = var_d.replace('\n', '').replace('\r', '')
    if not var_d.startswith('「') and oldLine and var_d != oldLine and oldLine.endswith(var_d):
        return ''
    oldLine = var_d
    return clearT(var_n) + '：' + clearT(var_d)
