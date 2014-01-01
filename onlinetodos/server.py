#!/usr/bin/env python
#coding:utf-8
from __future__ import absolute_import

import json
import os

import web
from jinja2 import Environment, FileSystemLoader

from onlinetodos.models import Todos

RUN_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(RUN_PATH, 'templates')

loader = FileSystemLoader(TEMPLATE_PATH)
lookup = Environment(loader=loader)

urls = (
    '/', 'index',  #返回首页
    '/todo', 'todo',  #  处理POST请求
    '/todo/(\d*)', 'todo',  # 处理前端todo的请求,对指定记录进行操作
    '/todos/', 'todos',  # 处理前端todo的请求，返回所有数据
    '/login', 'login',
    '/logout', 'logout',
)

class login:
    def GET(self):
        t = lookup.get_template('login.html')
        return t.render()

    def POST(self):
        username, passwd = web.input().get("username"), web.input().get("passwd")
        if username and username == passwd:
            session.login = True
            return web.Found('/')
        # error info
        return self.render(temp_name, {"error": "用户名或密码错误！"})


class logout:
    def GET(self):
        session.login = False
        t = lookup.get_template('login.html')
        return t.render()


# 首页
class index:
    def GET(self):
        if not session.login:
            return web.Found('/login')
        t = lookup.get_template('index.html')
        return t.render()

class todo:
    def GET(self, todo_id=None):
        result = None
        todo = Todos.get_by_id(id=todo_id)
        result = {
            "id": todo.id,
            "title": todo.title,
            "order": todo._order,
            "done": todo.done == 1,
        }
        return json.dumps(result)

    def POST(self):
        data = web.data()
        todo = json.loads(data)
        # 转换成_order, order是数据库关键字, sqlite3报错
        todo['_order'] = todo.pop('order')
        Todos.create(**todo)

    def PUT(self, todo_id=None):
        data = web.data()
        todo = json.loads(data)
        todo['_order'] = todo.pop('order')
        Todos.update(**todo)

    def DELETE(self, todo_id=None):
        Todos.delete(id=todo_id)


class todos:
    def GET(self):
        todos = []
        itertodos = Todos.get_all()
        for todo in itertodos:
            todos.append({
                "id": todo.id,
                "title": todo.title,
                "order": todo._order,
                "done": todo.done == 1,
            })
        return json.dumps(todos)

app = web.application(urls, globals())
from web.httpserver import StaticMiddleware
application = app.wsgifunc(StaticMiddleware)

if web.config.get('_session') is None:
    session = web.session.Session(
        app,
        web.session.DiskStore('sessions'),
        initializer={'login': False}
    )
    web.config._session = session
else:
    session = web.config._session


def main():
    app.run()

if __name__ == "__main__":
    main()
