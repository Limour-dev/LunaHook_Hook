def log_process(clearT, Cfg, Windows):
    var_d: str = Cfg.GetClipboardText()[::2]
    var_n = Cfg.var_n if var_d.startswith('「') else '旁白'
    return clearT(var_n) + '：' + clearT(var_d)