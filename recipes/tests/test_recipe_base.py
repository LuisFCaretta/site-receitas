from django.test import TestCase
from recipes.models import Recipe, Category, User


class RecipeMixin:
    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name="User",
        last_name="Created",
        username="username",
        password="User12345",
        email="user@user.com",
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title="Recipe title",
        description="Recipe decription",
        slug="recipe-title",
        preparation_time="10",
        preparation_time_unit="Minutos",
        servings="5",
        servings_unit="Pessoas",
        preparation_steps="preparation steps are here",
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {"author_data": {
                "username": f"user-{i}"}, "slug": f"slug-{i}"}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name="User",
        last_name="Created",
        username="username",
        password="User12345",
        email="user@user.com",
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title="Recipe title",
        description="Recipe decription",
        slug="recipe-title",
        preparation_time="10",
        preparation_time_unit="Minutos",
        servings="5",
        servings_unit="Pessoas",
        preparation_steps="preparation steps are here",
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
