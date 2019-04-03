"""Configures test environment by setting up the 'setup.cfg' file with your
    test environment paths.

    Warning:
        Before running this script, you must edit the test-setup.cfg file in
        the tests/ directory.

    Warning:
        This script must be run once before running any tests.
"""
import os
import argparse
from jinja2 import Template
try:
    from ConfigParser import ConfigParser # Python2
except ImportError:
    from configparser import ConfigParser # Python3


DEFAULT_ENV_CFG = "env.cfg"
DEFAULT_SETUP_CFG = "setup.cfg"

def get_cfg_option(section, option):
    """Returns the option value set in the config file %s""" % DEFAULT_ENV_CFG
    cfg = ConfigParser(allow_no_value=True)
    env_cfg_path = os.path.join(get_repo_path(), "tests", DEFAULT_ENV_CFG)
    if not os.path.isfile(env_cfg_path):
        raise Exception("Could not find environment configuration file: %s " % env_cfg_path)
    cfg.read(env_cfg_path)

    return cfg.get(section, option)

def get_ccs_exe(ccs_path=None):
    """Returns the full path to the ccs exe based off of the ccs_path or the
    value set in %s """ % DEFAULT_ENV_CFG
    return get_cfg_option("ccs", "ccs_exe")

def get_repo_path():
    """Returns the full path to the repo directory"""
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.abspath(repo_dir)

def get_cc13x0_serno(serno=None):
    """Returns the serial number for cc13x0 device set in %s""" % DEFAULT_ENV_CFG
    return get_cfg_option("cc13x0", "serno")



def configure_setup(ccs_path=None, cc13x0=None):
    """Configures setup.cfg file based off of the provided or env.cfg settings
        Args:
            ccs_path (str): full path to the ccs exe
            cc13x0 (str): serial number of the cc13x0 device used in your test setup
    """
    env = dict()
    env['repo_path'] = get_repo_path()
    env['ccs_exe'] = get_ccs_exe(ccs_path=ccs_path)
    env['cc13x0'] = {'serno': get_cc13x0_serno(serno=cc13x0)}

    setup_cfg = os.path.join(get_repo_path(), "tests", DEFAULT_SETUP_CFG)
    setup_cfg_j2 = setup_cfg + ".j2"

    # Render setup template to setup.cfg file
    with open(setup_cfg_j2) as f:
        Template(f.read()).stream(env=env).dump(setup_cfg)


def configure_cc13x0(cc13x0=None):
    """Configures cc13x0 resources folder for testing
        Args:
            cc13x0 (str): serial number of the cc13x0 device used in your test setup
    """
    env = dict()
    env['cc13x0'] = {'serno': get_cc13x0_serno(serno=cc13x0)}

    cc13x0_ccxml = os.path.join(get_repo_path(), "tests", "resources", "cc13x0", "cc13x0.ccxml")
    cc13x0_ccxml_j2 = cc13x0_ccxml + ".j2"

    # Render ccxml template to cc13x0 ccxml file
    with open(cc13x0_ccxml_j2) as f:
        Template(f.read()).stream(env=env).dump(cc13x0_ccxml)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ccs", help="full path to ccs exe; overrides the value set in tests/%s" % DEFAULT_ENV_CFG, type=str)
    parser.add_argument("--cc13x0", help="serial number for cc13x0 device; overrides the value set in tests/%s" % DEFAULT_ENV_CFG, type=str)

    args = parser.parse_args()

    configure_setup(ccs_path=args.ccs, cc13x0=args.cc13x0)
    configure_cc13x0(cc13x0=args.cc13x0)


if __name__ == "__main__":
    main()
