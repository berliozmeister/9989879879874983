'''
Created on 15.06.2012

@author: berlioz
'''
import web
import os
import urllib
import posixpath
import networkx as nx
import utils   
import matplotlib.pyplot as plt
__author__ = '\n'.join(['Mikhail Bernovskiy',
                        'Stas Fomin'])

if os.name == 'nt':
    import random as rnd
else:
    import random as rnd
pass

urls = (
    '/(.*)', 'index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

if not os.path.exists('generated'):
    os.mkdir('generated')
    

def RGG(n, beta, mean_degree):
    G = nx.empty_graph(n)
    degreeArray = utils.degreeDistribution(beta, n, mean_degree)
    utils.randPairings(G, degreeArray)
    txtName = "generated/adj-%s-%s-%s-.txt" % (str(n), str(beta), str(mean_degree))
    nx.write_adjlist(G, txtName)
    utils.drawDegreeHistogram(G)
    if n < 1000:
        utils.drawGraph(G)
    pngname = "generated/graph-%s-%s-%s-.png" % (str(n), str(beta), str(mean_degree))
    plt.savefig(pngname)
    



class index:
    def GET(self, wtf):
        inp = web.input(mean='10', power='1.7', size='10000')
        RGG(int(inp.size), float(inp.power), int(inp.mean))
        return render.index(mean=inp.mean, power=inp.power, size=inp.size)

class StaticMiddleware:
    """WSGI middleware for serving static files."""
    def __init__(self, app, prefix='/generated/',
                 root_path=r'/generated/'):
        self.app = app
        self.prefix = prefix
        self.root_path = root_path

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        path = self.normpath(path)

        if path.startswith(self.prefix):
            environ["PATH_INFO"] = os.path.join(self.root_path,
                                                web.lstrips(path, self.prefix))
            return web.httpserver.StaticApp(environ, start_response)
        else:
            return self.app(environ, start_response)

    def normpath(self, path):
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith("/"):
            path2 += "/"
        return path2


if __name__ == "__main__":
    wsgifunc = app.wsgifunc()
    wsgifunc = StaticMiddleware(wsgifunc)
    wsgifunc = web.httpserver.LogMiddleware(wsgifunc)
    server = web.httpserver.WSGIServer(("0.0.0.0", 8080), wsgifunc)
    print "http://%s:%d/" % ("0.0.0.0", 8080)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()