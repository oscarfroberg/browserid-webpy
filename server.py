import web
import urllib
import json

urls = ('/', 'index')

app = web.application(urls, globals())
render = web.template.render('templates/', base='base')

class FalseStorage(web.storage):
    def __nonzero__(self): return False

def browserid():
    # get user cookies:
    c = web.cookies()
    # if we find a browserid cookie:
    if c.get('browserid_assertion'):
        out = urllib.urlencode(dict(audience=web.ctx.host, 
            assertion=c.browserid_assertion))
        # send it to browserid.org to verify it:
        o = json.loads(urllib.urlopen('https://verifier.login.persona.org/verify', out).read())
        if o['status'] == 'failure':
            return FalseStorage(o)
        else:
            # if successful return the info:
            return web.storage(o)
    else:
        return web.storage()

def auth():
    # get authorization info from browserid:
    bid = browserid()
    # print the info for debugging:
    print "This is what browserid returns: ", bid
    # if we get a response, relay the information:
    if bid:
        response = "authorized as %s" % (bid['email'])
        return response
    else:
        response = "unauthorized!"
        return response

# render the main page
class index:
    def GET(self):
        # authenticate user:
        userstatus = auth()
        # render the main page with authentication info:
        return render.index(userstatus)

if __name__ == '__main__':
    app.run()
