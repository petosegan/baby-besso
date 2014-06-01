import cgi
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import besso_online

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/convo" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Talk to Besso"></div>
    </form>
  </body>
</html>
"""

class Dialeme(ndb.Model):
    """Models an individual query and response."""
    question = ndb.StringProperty(indexed=False)
    response = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class Guestbook(webapp2.RequestHandler):
    def post(self):
        last_prompt = cgi.escape(self.request.get('content'))
        this_response = besso_online.online(last_prompt)
    
        self.response.write('<html><body>Besso Says:<pre>')
        self.response.write(this_response)
        self.response.write('</pre></body></html>')
        self.response.write(MAIN_PAGE_HTML)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/convo', Guestbook),
], debug=True)