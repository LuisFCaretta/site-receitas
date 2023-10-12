from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Type your first name here.'),
        ('last_name', 'Type your last name here.'),
        ('username', 'Type your username here.'),
        ('email', 'Type your e-mail here.'),
        ('password', 'Type your password here.'),
        ('password2', 'Repeat your password.'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos.'
         ' Letras, números e @/./+/-/_ apenas.'),
        ('email', 'The e-mail must be valid.'),
        ('password', 'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters.'),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirm password'),
    ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, label)


class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'user@email.com',
            'password': 'User1234',
            'password2': 'User1234'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty.'),
        ('first_name', 'Write your first name.'),
        ('last_name', 'Write your last name.'),
        ('email', 'E-mail is required.'),
        ('password', 'Password must not be empty.'),
        ('password2', 'Please, repeat your password.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
