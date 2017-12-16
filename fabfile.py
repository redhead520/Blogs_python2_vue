#!/usr/bin/env python
# -*- coding: utf-8 -*-

# fabfile.py
import os, re
from datetime import datetime

# 导入Fabric API:
from fabric.api import *

# 服务器登录用户名:
env.user = 'root'
# # sudo用户为root:
# env.sudo_user = 'root'

env.hosts = ['162.219.127.17:27246']
# env.password = '0311020045'

_REMOTE_BASE_DIR = '/var/www/Blogs_python2_vue'

def push():
    with lcd(os.path.abspath('.')):
        local('git add -A')
        local('git commit -m "{} commited"'.format(str(datetime.now())))
        local('git push')

def deploy():
    # git 重新拉取最新代码
    with cd(_REMOTE_BASE_DIR):
        sudo('git pull')
        # 重启Python服务和nginx服务器:
    with settings(warn_only=True):
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        sudo('/etc/init.d/nginx reload')
