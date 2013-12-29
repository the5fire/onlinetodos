#coding:utf-8

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

from fabric.api import task, roles, cd
from fabric.state import env

from essay.tasks import build
from essay.tasks import deploy
from essay.tasks import virtualenv, supervisor, package, git

env.GIT_SERVER = 'https://github.com/'  # ssh地址只需要填：'github.com'
env.PROJECT = 'onlinetodos'
env.PROJECT_OWNER = 'the5fire'
env.DEFAULT_BRANCH = 'master'


######
# deploy settings:
env.PROCESS_COUNT = 2  #部署时启动的进程数目
env.roledefs = {
    'online': ['the5firetodo@the5fire.com']  # 打包服务器配置
}

env.VIRTUALENV_PREFIX = '/home/the5firetodo/'
env.SUPERVISOR_CONF_TEMPLATE = os.path.join(PROJECT_ROOT, 'conf', 'supervisord.conf')

PROJECT_NUM = 310
env.VENV_PORT_PREFIX_MAP = {
    'a': '%d0' % PROJECT_NUM,
    'b': '%d1' % PROJECT_NUM,
    'c': '%d2' % PROJECT_NUM,
    'd': '%d3' % PROJECT_NUM,
    'e': '%d4' % PROJECT_NUM,
    'f': '%d5' % PROJECT_NUM,
    'g': '%d6' % PROJECT_NUM,
    'h': '%d7' % PROJECT_NUM,
    'i': '%d8' % PROJECT_NUM,
}


@task(default=True)
@roles('online')
def git_deploy(venv_dir, profile):
    virtualenv.ensure(venv_dir)

    with virtualenv.activate(venv_dir):
        supervisor.ensure(project=env.PROJECT, profile=profile)
        package.install_from_git(env.PROJECT)
        supervisor.shutdown()
        supervisor.start()


HOST_PATH = '/home/the5firetodo/a/src/onlinetodos/'

@task(default=True)
@roles('online')
def re_deploy(venv_dir, br="master"):
    with cd(HOST_PATH):
        git.checkout(br)
    supervisor.reload(venv_dir)
