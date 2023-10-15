from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("first_name", "Type your first name here."),
            ("last_name", "Type your last name here."),
            ("username", "Type your username here."),
            ("email", "Type your e-mail here."),
            ("password", "Type your password here."),
            ("password2", "Repeat your password."),
        ]
    )
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            (
                "username",
                (
                    "Username must have letters,"
                    " numbers or one of those @.+-_ "
                    "The length should be between 4 and 150 characters."
                ),
            ),
            ("email", "The e-mail must be valid."),
            (
                "password",
                "Password must have at least one uppercase letter,"
                "one lowercase letter and one number."
                "The length should be at least 8 characters.",
            ),
        ]
    )
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand(
        [
            ("first_name", "First name"),
            ("last_name", "Last name"),
            ("username", "Username"),
            ("email", "E-mail"),
            ("password", "Password"),
            ("password2", "Confirm password"),
        ]
    )
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, label)


class AuthorRegisterFormIntegrationTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "user",
            "first_name": "First",
            "last_name": "Last",
            "email": "user@email.com",
            "password": "User1234",
            "password2": "User1234",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand(
        [
            ("username", "This field must not be empty."),
            ("first_name", "Write your first name."),
            ("last_name", "Write your last name."),
            ("email", "E-mail is required."),
            ("password", "Password must not be empty."),
            ("password2", "Please, repeat your password."),
        ]
    )
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data["username"] = "Ze"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Username must have at least 4 characters."
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))

    def test_username_field_max_length_should_be_150(self):
        self.form_data["username"] = "Z" * 151
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Username must have less than 150 characters."
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))

    def test_password_field_have_lower_upper_case_letter_and_number(self):
        self.form_data["password"] = "abc123"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = ("Password must have at least one uppercase letter,"
               " one lowercase letter and one number."
               " The length should be at least 8 characters.")
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("password"))

        self.form_data["password"] = "A@77bc123"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.context["form"].errors.get("password"))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data["password"] = "@abcDe123"
        self.form_data["password2"] = "@abcD123"

        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Password and confirm password must be equal."
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("password"))

        self.form_data["password"] = "@abcDe123"
        self.form_data["password2"] = "@abcDe123"

        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode("utf-8"))

    def test_send_get_request_to_registration_view_returns_404(self):
        url = reverse("authors:register_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse("authors:register_create")
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "User e-mail is already in use."
        self.assertIn(msg, response.context["form"].errors.get("email"))
        self.assertIn(msg, response.content.decode("utf-8"))

    def test_author_created_can_login(self):
        url = reverse("authors:register_create")
        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc12345678',
            'password2': '@Bc12345678',
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc12345678'
        )
        self.assertTrue(is_authenticated)
