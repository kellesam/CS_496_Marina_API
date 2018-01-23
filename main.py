from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty(required=True)
	length = ndb.IntegerProperty(required=True)
	at_sea = ndb.BooleanProperty(required=True)

class Slip(ndb.Model):
	number = ndb.IntegerProperty(required=True)
#	current_boat = ndb.IntegerProperty()
#	arrival_date = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Marina content here')

class BoatHandler(webapp2.RequestHandler):
	def post(self):
		parent_key = ndb.Key(Boat, "parent_boat")
		boat_data = json.loads(self.request.body)
		new_boat = Boat(name = boat_data['name'],
						type = boat_data['type'],
						length = boat_data['length'],
						at_sea = True,
						parent = parent_key)
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))

	def get(self, id=None):
		if id:
			boat = ndb.Key(urlsafe=id).get()
			boat_dict = boat.to_dict()
			boat_dict['self'] = '/boat/' + id
			self.response.write(json.dumps(boat_dict))
		else:
			all_boats = Boat.query().fetch(20)
			boats = []
			for boat in all_boats:
				boats.append(boat.to_dict())
			self.response.write(json.dumps(boats))

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler),
    ('/boat/(.*)', BoatHandler)
], debug=True)
