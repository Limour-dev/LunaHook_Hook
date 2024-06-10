def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.GetEditText()
    if len(var_d) % 2 == 0 and var_d[::2] == var_d[1::2]:
        var_d = var_d[::2]
    var_n = Cfg.var_n if var_d.startswith('「') else '旁白'
    if var_d.startswith('（') and var_d.endswith('）'):
        var_n = Cfg.var_n
    return clearT(var_n) + '：' + clearT(var_d)