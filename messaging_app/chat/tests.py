from django.test import TestCase
from .models import User, Conversation, Message

class ModelsTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='test', password='pass')
        self.assertEqual(user.username, 'test')
