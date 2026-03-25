import unittest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

class DjangoViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup run once for all tests in the class
        super().setUpClass()
        User.objects.all().delete()  # Clear existing users
        cls.client = Client()
        cls.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        cls.signup_url = reverse('signup')
        cls.login_url = reverse('login')
        cls.home_url = reverse('home')
        cls.logout_url = reverse('logout')

    def test_signup_success(self):
        # Test successful signup
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_password_mismatch(self):
        # Test signup with mismatched passwords
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password1',
            'password2': 'password2'
        })
        self.assertEqual(response.status_code, 200)  # Renders the same page again
        self.assertIn("Your password and confrom password are not Same!!", response.content.decode())

    def test_login_success(self):
        # Test successful login
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'pass': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertIn(self.home_url, response.url)

    def test_login_failure(self):
        # Test login with incorrect credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'pass': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Username or Password is incorrect!!!", response.content.decode())

    def test_home_page_authenticated(self):
        # Test accessing the home page while authenticated
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("home.html", [t.name for t in response.templates])

    def test_home_page_unauthenticated(self):
        # Test accessing the home page without authentication
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200) 

    def test_logout(self):
        # Test logout functionality
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn(self.login_url, response.url)

if __name__ == "__main__":
    unittest.main()

