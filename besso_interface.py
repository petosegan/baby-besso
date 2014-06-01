import cgi, urllib
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import besso_online
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_CONVO_NAME = 'default_convo'

def convo_key(convo_name=DEFAULT_CONVO_NAME):
    """Constructs a Datastore key for a Convo entity with convo_name."""
    return ndb.Key('Convo', convo_name)

class Dialeme(ndb.Model):
    """Models an individual query and response."""
    question = ndb.StringProperty(indexed=False)
    response = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        convo_name = self.request.get('convo_name',
                                          DEFAULT_CONVO_NAME)
                                          
        dialeme_query = Dialeme.query(
            ancestor=convo_key(convo_name)).order(-Dialeme.date)
        dialemes = dialeme_query.fetch(8)
        dialemes.reverse()
        
        template_values = {
            'dialemes': dialemes,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        

class convo_handler(webapp2.RequestHandler):
    def post(self):
        last_prompt = cgi.escape(self.request.get('content'))
        this_response = besso_online.online(last_prompt)
        
        convo_name = self.request.get('convo_name',
                                          DEFAULT_CONVO_NAME)
                                          
        dialeme = Dialeme(parent=convo_key(convo_name))
        dialeme.question = last_prompt
        dialeme.response = this_response
        dialeme.put()
        
        query_params = {'convo_name': convo_name}
        self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/convo', convo_handler),
], debug=True)