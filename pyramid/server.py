from wsgiref.simple_server import  make_server
from pyramid.config import Configurator
from pyramid.response import Response
import pyramid.httpexceptions as exc
import os

from pyramid.wsgi import wsgiapp

MWT = "<div class='top'>Middleware TOP</div>"
MWB = "<div class='botton'>Middleware BOTTOM</div>"

def index_html(environ, start_response):
    file = open('./index.html', 'r')
    data = file.read()
    file.close()
    return Response(data)

def aboutme_html(environ, start_response):
    file = open('./about/aboutme.html', 'r')
    data = file.read()
    file.close()
    return Response(data)

class MyMiddleWare(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response)[0].decode()

        if response.find('<body>') >-1:
            header,body = response.split('<body>')
            bodycontent,htmlend = body.split('</body>')
            bodycontent = '<body>'+ MWT + bodycontent + MWB+'</body>'
            return [header.encode() + bodycontent.encode() + htmlend.encode()]
        else:
            return [MWT + response.encode() + MWB]

def app(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/':
        filePath='.'+path
        print('index')
        if path == '/about/aboutme.html':
            filePath = './about/aboutme.html'
        print('about')
    else:
        filePath = './index.html'
    fd = open(filePath,'rb')
    fileContent = fd.read()
    fd.close()

    start_response('200', [('Content-Type', 'text/html')])
    return [fileContent.encode()]

if __name__ == '__main__':
    config = Configurator()

    config.add_route('root', '/')
    config.add_route('index_html', '/index.html')
    config.add_route('aboutme_html', '/about/aboutme.html')

    config.add_view(index_html, route_name='root')
    config.add_view(index_html, route_name='index_html')
    config.add_view(aboutme_html, route_name='aboutme_html')

    app = config.make_wsgi_app()
    myApp = MyMiddleWare(app)


    server = make_server('0.0.0.0', 8000, myApp)
    server.serve_forever()
