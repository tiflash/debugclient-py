try:
    from ConfigParser import ConfigParser, ExtendedInterpolation # Python2
except ImportError:
    from configparser import ConfigParser, ExtendedInterpolation # Python3

def get_enabled_setups(cfgfile):
    """Returns list of names of all enabled setups in setup.cfg"""
    enabled_setups = list()

    cfg = ConfigParser(None, allow_no_value=False)
    cfg.optionxform = str
    cfg.read(cfgfile)

    for opt in cfg.options("testsetups-enabled"):
        if cfg.getboolean("testsetups-enabled", opt) is True:
            enabled_setups.append(opt)

    return enabled_setups

def get_setup_env(cfgfile, setup_name):
    """Returns a dict of setup values"""
    cfg = ConfigParser(None, interpolation=ExtendedInterpolation())
    cfg.optionxform = str
    cfg.read(cfgfile)

    tenv = dict(cfg.items("paths"))
    tenv.update(dict(cfg.items(setup_name)))

    return tenv
