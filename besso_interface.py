import cgi, urllib
import os
import random, string
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import besso_online
import jinja2
from gaesessions import get_current_session


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
    session_id = ndb.StringProperty(indexed=False)

class MainPage(webapp2.RequestHandler):
    def get(self):
    
        session = get_current_session()
        if session.get('session_id') is None:
            random.seed()
            lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(30)]
            this_sid = "".join(lst)
            session.set_quick('session_id', this_sid)
            session.save()
        this_convo_name = session.sid

        convo_name = self.request.get('convo_name',
                                          this_convo_name)
                                          
        dialeme_query = Dialeme.query(
            ancestor=convo_key(convo_name)).order(-Dialeme.date)
        dialemes = dialeme_query.fetch(8)
        dialemes.reverse()
        
        template_values = {
            'dialemes': dialemes,
            'sessionid': session.sid.encode('ascii','ignore'),
            'convo_name': convo_name,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        

class convo_handler(webapp2.RequestHandler):
    def post(self):
    
        session = get_current_session()
        this_convo_name = session.sid
        
        last_prompt = cgi.escape(self.request.get('content'))
        this_response = besso_online.online(last_prompt)
        
        convo_name = self.request.get('convo_name',
                                          this_convo_name)
                                          
        dialeme = Dialeme(parent=convo_key(convo_name))
        dialeme.question = last_prompt
        dialeme.response = this_response
        dialeme.session_id = convo_name
        dialeme.put()
        
        query_params = {'convo_name': convo_name}
        self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/convo/', convo_handler),
], debug=True)