from google.appengine.ext import ndb
import webapp2
import json
import logging

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Marina content here')

class Boat(ndb.Model):
	name = ndb.StringProperty(required = True)
	type = ndb.StringProperty(required = True)
	length = ndb.IntegerProperty(required = True)
	at_sea = ndb.BooleanProperty(required = True)

class BoatHandler(webapp2.RequestHandler):
	def post(self):
		boat_data = json.loads(self.request.body)
		new_boat = Boat(name = boat_data['name'],
						type = boat_data['type'],
						length = boat_data['length'],
						at_sea = True)
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))

	def get(self, id = None):
		if id:
			boat = ndb.Key(urlsafe = id).get()
			if boat:
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boat/' + id
				self.response.write(json.dumps(boat_dict))
		else:
			all_boats = Boat.query().fetch(1000)
			boats = []
			for boat in all_boats:
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boat/' + boat.key.urlsafe()
				boats.append(boat_dict)
			self.response.write(json.dumps(boats))

	def delete(self, id = None):
		if id:
			boat = ndb.Key(urlsafe = id).get()
			boat.key.delete()
		else:
			boats = Boat.query().fetch(1000)
			for boat in boats:
				boat.key.delete()

	def patch(self, id = None):
		if id:
			boat = ndb.Key(urlsafe = id).get()
			if boat:
				boat_data = json.loads(self.request.body)
				if 'name' in boat_data:
					boat.name = boat_data['name']
				if 'type' in boat_data:
					boat.type = boat_data['type']
				if 'length' in boat_data:
					boat.length = boat_data['length']
				boat.put()
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boat/' + boat.key.urlsafe()
				self.response.write(json.dumps(boat_dict))

class Slip(ndb.Model):
	number = ndb.IntegerProperty(required = True)
	current_boat = ndb.IntegerProperty()
	arrival_date = ndb.StringProperty()

class SlipHandler(webapp2.RequestHandler):
	def post(self):
		slip_data = json.loads(self.request.body)
		new_slip = Slip(number = slip_data['number'],
						current_boat = None,
						arrival_date = None)
		new_slip.put()
		slip_dict = new_slip.to_dict()
		slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
		self.response.write(json.dumps(slip_dict))

	def get(self, id = None):
		if id:
			slip = ndb.Key(urlsafe = id).get()
			if slip:
				slip_dict = slip.to_dict()
				slip_dict['self'] = '/slip/' + id
				self.response.write(json.dumps(slip_dict))
		else:
			all_slips = Slip.query().fetch(1000)
			slips = []
			for slip in all_slips:
				slip_dict = slip.to_dict()
				slip_dict['self'] = '/slip/' + slip.key.urlsafe()
				slips.append(slip_dict)
			self.response.write(json.dumps(slips))

	def delete(self, id = None):
		if id:
			slip = ndb.Key(urlsafe = id).get()
			slip.key.delete()
		else:
			slips = Slip.query().fetch(1000)
			for slip in slips:
				slip.key.delete()

	def patch(self, id = None):
		if id:
			slip = ndb.Key(urlsafe = id).get()
			if slip:
				slip_data = json.loads(self.request.body)
				if 'number' in slip_data:
					slip.number = slip_data['number']
				slip.put()
				slip_dict = slip.to_dict()
				slip_dict['self'] = '/slip/' + slip.key.urlsafe()
				self.response.write(json.dumps(slip_dict))

class DockHandler(webapp2.RequestHandler):
	def put(self, id = None):
		if id:
			self.response.write(id)

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/boat', BoatHandler),
	('/boat/(.*)', BoatHandler),
	('/slip', SlipHandler),
	('/slip/boat/(.*)', DockHandler),
	('/slip/(.*)', SlipHandler)
], debug=True)
