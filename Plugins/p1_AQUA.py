def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.GetEditText()[::2]
    var_n = Cfg.var_n if var_d.startswith('「') else '旁白'
    if var_d.startswith('（') and var_d.endswith('）'):
        var_n = Cfg.var_n
    return clearT(var_n) + '：' + clearT(var_d)