def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.var_d
    var_d = var_d.strip()
    var_n = '旁白'
    if var_d.endswith('」') and '「' in var_d:
        idx = var_d.index('「')
        var_n = var_d[:idx]
        if var_n:
            var_d = var_d[idx:]
        else:
            var_n = '旁白'
    return clearT(var_n) + '：' + clearT(var_d)
