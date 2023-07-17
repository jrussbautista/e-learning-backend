import factory
from faker import Factory
from users.factories import UserFactory
from .models import Category, Course


faker = Factory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
