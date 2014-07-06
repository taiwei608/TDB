import cgi
import urllib

from google.appengine.ext import ndb

import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """\
<html>
  <body>
    <form action="/add?%s" method="post">
      <div><input name="URL"></input></div>
      <div><input type="submit" value="Add URL"></div>
    </form>
    <hr>
  </body>
</html>
"""
    
class URLEntry(ndb.Model):
    """Models an individual URL entry."""
    createTime = ndb.DateTimeProperty(auto_now_add=True)
    URL=ndb.TextProperty()
    tags=ndb.StringProperty(repeated=True)
    group=ndb.StringProperty()
    visitTimes=ndb.IntegerProperty()
    parent=ndb.StringProperty()
    userDefineGroup=ndb.StringProperty(repeated=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Write the submission form and the footer of the page
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        
class URLList(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        ruls_query = URLEntry.query()
        urls = ruls_query.fetch()
        for url in urls:
            if url.URL:
                self.response.write('<b>%s</b>:%s<br>' % (url.URL, url.createTime))
        self.response.write('</body></html>')
        
class URLAdd(webapp2.RequestHandler):
    def post(self):
        url = URLEntry()
        url.URL = self.request.get('URL')
        url.put()
        self.redirect('/')
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/list', URLList),
    ('/add', URLAdd)
], debug=True)