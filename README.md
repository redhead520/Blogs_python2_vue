###### 基于廖雪峰python2教程的实战项目
# 162.219.127.17:88
####项目结构

```
py2-webapp/   <-- 根目录
|
+- backup/               <-- 备份目录
|
+- conf/                 <-- 配置文件
|
+- dist/                 <-- 打包目录
|
+- www/                  <-- Web目录，存放.py文件
|  |
|  +- static/            <-- 存放静态文件
|  |
|  +- templates/         <-- 存放模板文件
|
+- LICENSE               <-- 代码LICENSE
```

#### 本地自动化部署
    要用Fabric部署，需要在本机（是开发机器，不是Linux服务器）安装Fabric：
    ```
    $ easy_install fabric
    ```
    编辑fabric文件：fabfile.py
    ```
    $ fab build
    $ fab run
    ```

#### 服务器配置 Nginx/

- Nginx：高性能Web服务器+负责反向代理；
- gunicorn：高性能WSGI服务器；
- gevent：把Python同步代码变成异步协程的库；
- Supervisor：监控服务进程的工具；
- MySQL：数据库服务。
```
$ sudo apt-get install nginx gunicorn python-gevent supervisor mysql-server
$ sudo apt-get install python-jinja2 python-mysql.connector
```
- 数据库初始化脚本
```
mysql -u root -p < schema.sql
```
- 配置Supervisor: sudo vim /etc/supervisor/conf.d/awesome.conf
    ```
    [program:awesome]
    command     = /usr/bin/gunicorn --bind 127.0.0.1:9000 --workers 1 --worker-class gevent wsgiapp:application
    directory   = /srv/awesome/www
    user        = www-data
    startsecs   = 3

    redirect_stderr         = true
    stdout_logfile_maxbytes = 50MB
    stdout_logfile_backups  = 10
    stdout_logfile          = /srv/awesome/log/app.log
    ```

    supervisor 命令：
    ```
    $ sudo supervisorctl reload
    $ sudo supervisorctl start awesome
    $ sudo supervisorctl status
    ```
- Nginx 配置 vim /etc/nginx/sites-enabled/awesome
    ```
    server {
        listen      80; # 监听80端口

        root       /srv/awesome/www;
        access_log /srv/awesome/log/access_log;
        error_log  /srv/awesome/log/error_log;

        # server_name awesome.liaoxuefeng.com; # 配置域名

        # 处理静态文件/favicon.ico:
        location /favicon.ico {
            root /srv/awesome/www;
        }

        # 处理静态资源:
        location ~ ^\/static\/.*$ {
            root /srv/awesome/www;
        }

        # 动态请求转发到9000端口(gunicorn):
        location / {
            proxy_pass       http://127.0.0.1:9000;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

    ```