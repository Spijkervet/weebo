import unittest
import os
import json
from app import create_app, db

class AlarmTestCase(unittest.TestCase):
    """This class represents the alarm test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.alarm = {'name': 'Flight to Los Angeles'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_alarm_creation(self):
        """Test API can create an alarm (POST request)"""
        res = self.client().post('/alarms/', data=self.alarm)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Flight to Los Angeles', str(res.data))

    def test_api_can_get_all_alarms(self):
        """Test API can get an alarm (GET request)."""
        res = self.client().post('/alarms/', data=self.alarm)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/alarms/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Flight to Los Angeles', str(res.data))

    def test_api_can_get_alarm_by_id(self):
        """Test API can get a single alarm by using it's id."""
        rv = self.client().post('/alarms/', data=self.alarm)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/alarms/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Flight to Los Angeles', str(result.data))

    def test_alarm_can_be_edited(self):
        """Test API can edit an existing alarm. (PUT request)"""
        rv = self.client().post(
            '/alarms/',
            data={'name': 'Flight to Amsterdam'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/alarms/1',
            data={
                "name": "It's a great flight."
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/alarms/1')
        self.assertIn('Flight to Amsterdam', str(results.data))

    def test_alarm_deletion(self):
        """Test API can delete an existing alarm. (DELETE request)."""
        rv = self.client().post(
            '/alarms/',
            data={'name': 'Flight to Amsterdam'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/alarms/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/alarms/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
