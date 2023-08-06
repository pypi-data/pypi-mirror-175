"""

    """

import subprocess

from .util import read_json , get_user_repo_from_url
from .models import Conf
from .github_release import download_latest_release


cnf = Conf()

def make_venv(fp = cnf.def_fn) :
    js = read_json(fp)

    rp_url = js[cnf.repo_url]
    usrp = get_user_repo_from_url(rp_url)

    pyv = js[cnf.python_version]

    subprocess.run(['pyenv' , 'install' , '--skip-existing' , pyv])
    subprocess.run(['pyenv' , 'virtualenv-delete' , '-f' , usrp.user_und_repo])
    subprocess.run(['pyenv' , 'virtualenv' , pyv , usrp.user_und_repo])

    print(usrp.user_und_repo)

def ret_dirn(fp = cnf.def_fn) :
    js = read_json(fp)
    rp_url = js[cnf.repo_url]
    dirp = download_latest_release(rp_url)
    print(dirp)

def ret_module_2_run_name(fp = cnf.def_fn) :
    js = read_json(fp)
    print(js[cnf.module_2_run])

def rm_venv(fp = cnf.def_fn) :
    js = read_json(fp)

    rp_url = js[cnf.repo_url]
    usrp = get_user_repo_from_url(rp_url)

    rmv = js[cnf.rm_venv]
    if rmv is True :
        cmd = ['pyenv' , 'virtualenv-delete' , '-f' , usrp.user_und_repo]
        subprocess.run(cmd)
        print(f'\n LOG: {usrp.user_und_repo} venv has been deleted')
    else :
        print(f'\n LOG: {usrp.user_und_repo} venv has NOT been deleted')

def dl_main_bash() :
    rp_url = 'https://github.com/imahdimir/auto-run-bash'
    dirp = download_latest_release(rp_url)
    print(dirp)
