import os
import unittest
import tempfile

import phonebank

class PhonebankTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, phonebank.app.config['DATABASE'] = tempfile.mkstemp()
        phonebank.app.testing = True
        self.app = phonebank.app.test_client()
        with phonebank.app.app_context():
            phonebank.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(phonebank.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Nothing here yet' in rv.data

    def test_add_contact(self):
        rv = self.app.post('/', data=dict(
            name='Jane P. Voter',
            phone_number='555-555-5555',
            address='123 Main St',
            notes='Existence unknown.'
        ), follow_redirects=True)

        assert b'Jane P. Voter' in rv.data
        assert b'5555' in rv.data

    def test_invalid_phone(self):
         rv = self.app.post('/', data=dict(
            name='Jane P. Voter',
            phone_number='555-555-garbage',
            address='123 Main St',
            notes='Existence unknown.'
        ), follow_redirects=True)

         assert b'Phone number must contain ten digits' in rv.data

if __name__ == '__main__':
    unittest.main()
