from django.test import TestCase, Client
from django.contrib.auth.models import User
from deposit.views import *
from banksampah.models import News



# Create your tests here.
class HomeTest(TestCase): 
    def setUp(self):
        # runs before every test function
        self.dummy_deposit = {
            'data': '{"description": "test", "mass": 5.5, "type": "PLASTIK"}'
        }
        self.dummy_news = {
             'data': '{"title": "test", "description": "test"}'
        }
        self.credentials = {
            'username': 'testimoney11',
            'password': 'investasibodong1'
        }
        self.user = User.objects.create_superuser(
            username= self.credentials['username'],
            email = '',
            password= self.credentials['password']
        )
        self.user.save()

        user = User.objects.create_user(username='test', password='investasibodong')
        userAdmin = User.objects.create_superuser('testAdmin', '', "senjatamakantuan")

    
    def test_home(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        
    def test_news_json(self):
        c = Client()
        response = c.get("/news/json/")
        self.assertEqual(response.status_code, 200) 

    def test_news(self):
        c = Client()
        c.login(username="test", password="investasibodong")
        response = c.get("/news/")
        self.assertEqual(response.status_code, 200) 
    
    def test_news_read_more(self):
        News.objects.create(title="jamet", description="khatulistiwa")
        c = Client()
        c.login(username="test", password="investasibodong")
        response = c.get("/news/read/1/")
        self.assertEqual(response.status_code, 200) 

    def test_submit_logged_in(self):
        ''' Test submitting new deposit'''
        c = Client()
        c.login(**self.credentials)
        c.post('/login/', self.credentials)
        c.get('/news/')
        
        response = c.post('/news/add', self.dummy_news)
        self.assertEqual(response.status_code, 301) # should be oK or redirect

    def test_news_logged_in_read(self):
        c = Client()
        c.login(**self.credentials)
        c.post('/login/', self.credentials)
        c.get('/news/')
        
        response = c.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_view_home_logged_in(self):
        c = Client()
        c.login(**self.credentials)
        c.get('/')
        
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        c = Client()
        c.post('/register/', self.credentials)

        response = c.get('/register/')
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        c = Client()
        c.login(**self.credentials)
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        c= Client()
        response = c.post('/logout/', username='dog', password='123')
        self.assertEqual(response.status_code, 302)

    def test_add_news(self):
        c = Client()
        c.login(**self.credentials)
        c.get('/news/')

        response = c.post('/news/add/', self.dummy_news)
        
        self.assertEqual(response.status_code, 200)

    def test_get_add_news(self):
        c = Client()
        c.login(**self.credentials)
        response = c.get('/news/add/')
        
        self.assertEqual(response.status_code, 200)
        

    def test_delete_news(self):
        c = Client()
        c.login(**self.credentials)
        c.get('/news/')
        c.post('/news/add/', self.dummy_news)

        response = c.post('/news/delete/1/')
        
        self.assertEqual(response.status_code, 200)

    def test_wrong_login(self):
        c = Client()
        response = c.login(username='a', password='bbawdaw')
        self.assertEqual(response, False)
    
    
    def test_login2(self):
        ''' test login process (before utilizing logged-in features)'''
        c = Client()
        is_logged_in = c.login(**self.credentials)
        self.assertTrue(is_logged_in)