import server
import unittest
import json
from pymongo import MongoClient

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
      self.app = server.app.test_client()
      # Run app in testing mode to retrieve exceptions and stack traces
      server.app.config['TESTING'] = True

      # Inject test database into application
      mongo = MongoClient('localhost', 27017)
      db = mongo.test_database
      server.app.db = db

      # Drop collection (significantly faster than dropping entire db)
      db.drop_collection('myobjects')

    # User tests
    def test_posting_username_and_password(self):
        response = self.app.post('/users/',
                                data=json.dumps(dict(
                                    username="Kazu",
                                    password="test"
                                )),
                                content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert "Kazu" in responseJSON["username"]
        assert "test" in responseJSON["password"]

    # MyObject tests
    def test_posting_myobject(self):
      response = self.app.post('/myobject/',
        data=json.dumps(dict(
          name="A object"
        )),
        content_type='application/json')

      responseJSON = json.loads(response.data.decode())

      self.assertEqual(response.status_code, 200)
      assert 'application/json' in response.content_type
      assert 'A object' in responseJSON["name"]


    def test_getting_object(self):
      response = self.app.post('/myobject/',
        data=json.dumps(dict(
          name="Another object"
        )),
        content_type = 'application/json')

      postResponseJSON = json.loads(response.data.decode())
      postedObjectID = postResponseJSON["_id"]

      response = self.app.get('/myobject/'+postedObjectID)
      responseJSON = json.loads(response.data.decode())

      self.assertEqual(response.status_code, 200)
      assert 'Another object' in responseJSON["name"]

    def test_getting_non_existent_object(self):
      response = self.app.get('/myobject/55f0cbb4236f44b7f0e3cb23')
      self.assertEqual(response.status_code, 404)


# Note: implement test for put method
    def test_putting_object(self):
        response = self.app.post('/myobject/',
            data=json.dumps(dict(
                name="Another object"
            )),
            content_type = 'application/json')

        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["_id"]

        response = self.app.put('/myobject/'+postedObjectID,
            data=json.dumps(dict(name="Another colored object")),
            content_type='application/json')
        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'Another colored object' in responseJSON["name"]

    def test_putting_non_existent_object(self):
      response = self.app.get('/myobject/55f0cbb4236f44b7f0e3cb23')
      self.assertEqual(response.status_code, 404)


    def test_deleting_object(self):
      response = self.app.post('/myobject/',
        data=json.dumps(dict(
          name="Another object"
        )),
        content_type='application/json')

      postResponseJSON = json.loads(response.data.decode())
      postedObjectID = postResponseJSON["_id"]

      response = self.app.delete('/myobject/'+postedObjectID)
      responseJSON = json.loads(response.data.decode())

      self.assertEqual(response.status_code, 200)
      assert postedObjectID in responseJSON["objectIdentifier"]

      responseGet = self.app.get(('/myobject/'+postedObjectID))
      self.assertEqual(responseGet.status_code, 404)
    #   assert 'Another object' not in responseJSON["name"]
    #
    # def test_deleting_non_existent_object(self):
    #   response = self.app.get('/myobject/55f0cbb4236f44b7f0e3cb23')
    #   self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
    # test_posting_myobject()
