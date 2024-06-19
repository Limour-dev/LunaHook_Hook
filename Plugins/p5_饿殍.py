def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.GetEditText()
    var_n = '旁白'
    if var_d.startswith('['):
        if ']' in var_d:
            var_n = var_d[var_d.rindex(']')+1:]
            var_d = var_d[:-len(var_n)]
        else:
            pass

    return clearT(var_n) + '：' + clearT(var_d)