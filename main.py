#!/usr/bin/env python
import os
import jinja2
import webapp2
import json

from google.appengine.api import urlfetch


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        f = open("people.json", "r")
        podatki = f.read()
        ljudje = json.loads(podatki)
        params = {"seznam": ljudje}
        return self.render_template("hello.html", params=params)

class VremeHandler(BaseHandler):
    def get(self):
        zeljeno_mesto = self.request.get("mesto")
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + zeljeno_mesto + "&units=metric&appid=bc404a534664f0682a9e960d80ad241f" # noter smo dodali & units=metric
        stran = urlfetch.fetch(url).content
        vreme = json.loads(stran)
        params = {"vreme":vreme}
        return self.render_template("vreme.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vreme', VremeHandler),
], debug=True)
