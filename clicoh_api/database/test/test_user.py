from rest_framework.test import APITestCase,APIClient
from rest_framework import status 


from database.models import User
from authentication.serializers import *

from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self):

        self.register_url =  reverse('auth_register') 
        self.login_url    =  reverse('auth_login')        
        self.data = {'email':"test@gmail.com",'password':"testpassword"}

        return super().setUp() 

    def tearDown(self):
        return super().tearDown()  


class RegistrationTest(TestSetUp):

    def test_register_failed(self):

        res = self.client.post(self.register_url)        
        self.assertEqual(res.status_code,400)

    def test_register_success(self): 

        res = self.client.post(self.register_url,self.data,format='json') 
        self.assertEqual(res.data['email'],self.data['email'])        
        self.assertEqual(res.status_code,201)


    def test_login_success(self):

        res_register = self.client.post(self.register_url,self.data,format='json')
        res_login    = self.client.post(self.login_url,self.data,format='json')
        self.assertEqual(res_login.status_code,200)


    def test_api_jwt(self):

        res_register = self.client.post(self.register_url,self.data,format='json')
        res_login    = self.client.post(self.login_url,self.data,format='json')
        
        self.assertEqual(res_login.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in res_login.data)
        token = res_login.data['token']

        # verification_url = reverse('token_verify')
        # resp = self.client.post(verification_url, {'token': token}, format='json')
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)

        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = client.get('/products/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

       
     
