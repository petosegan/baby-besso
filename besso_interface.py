import cgi, urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import besso_online

MAIN_PAGE_HTML = """\
    <form action="/convo" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Talk to Besso"></div>
    </form>
  </body>
</html>
"""

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
        
        for leme in dialemes:
            self.response.write(cgi.escape(leme.question))
            self.response.write('<blockquote>%s</blockquote>' %
                                cgi.escape(leme.response))
                                
        self.response.write('<hr>')
        self.response.write(MAIN_PAGE_HTML)


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