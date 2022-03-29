from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post

# Create your tests here.
class BlogTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'meermustan',
            email = 'meer.mustan786@gmail.com',
            password = 'secret'
            
        )

        self.post = Post.objects.create(
            title = 'this is title',
            body = 'this is body',
            author = self.user
        )

    def test_string_representation(self):
        post = Post(title='this is title')
        self.assertEqual(str(post),post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}','this is title')
        self.assertEqual(f'{self.post.body}','this is body')
        self.assertEqual(f'{self.post.author}','meermustan')
    
    def test_post_list_view(self):
       response = self.client.get(reverse('home'))
       self.assertEqual(response.status_code, 200)
       self.assertContains(response, 'body')
       self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'title')
        self.assertTemplateUsed(response, 'post_detail.html')


    def test_post_create_view(self):
        response = self.client.get(reverse('post_new'),{
            'title':'this is new title',
            'body':'this is new body',
            'author':self.user
        })
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'title')
        self.assertContains(response,'body')

    # def test_post_update_view(self): # new
    #     response = self.client.post(reverse('post_edit', args='1'), {
    #         'title': 'Updated title',
    #         'body': 'Updated text',
    #     })
    #     self.assertEqual(response.status_code, 302)

    # def test_post_delete_view(self): # new
    #     response = self.client.post(reverse('post_delete', args='1'))
    #     self.assertEqual(response.status_code, 302)

            