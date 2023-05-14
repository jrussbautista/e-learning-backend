import factory
from faker import Factory
from users.factories import UserFactory
from .models import Subject, Course


faker = Factory.create()


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    title = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))
    author = factory.SubFactory(UserFactory)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=1))
    description = factory.LazyAttribute(lambda _: faker.paragraph(nb_sentences=5))
    subject = factory.SubFactory(SubjectFactory)
    author = factory.SubFactory(UserFactory)
