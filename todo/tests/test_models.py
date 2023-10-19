from django.test import TestCase
from django.contrib.auth import get_user_model

from todo.models import Project, Tag, Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        test_user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        Task.objects.create(title="test_title", user=test_user)

    def test_task_object_name(self) -> None:
        test_task = Task.objects.get(pk=1)
        self.assertEqual(str(test_task), test_task.title)

    def test_task_title_max_length(self) -> None:
        test_task = Task.objects.get(pk=1)
        title_max_length = test_task._meta.get_field("title").max_length
        self.assertEqual(title_max_length, 255)


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        test_user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        Project.objects.create(name="test_name", user=test_user)

    def test_project_object_name(self) -> None:
        test_project = Project.objects.get(pk=1)
        self.assertEqual(str(test_project), test_project.name)

    def test_project_name_max_length(self) -> None:
        test_project = Project.objects.get(pk=1)
        name_max_length = test_project._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 255)


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        test_user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        Tag.objects.create(name="test_name", slug="test_slug", user=test_user)

    def test_tag_object_name(self) -> None:
        test_tag = Tag.objects.get(pk=1)
        self.assertEqual(str(test_tag), test_tag.name)

    def test_tag_name_max_length(self) -> None:
        test_tag = Tag.objects.get(pk=1)
        name_max_length = test_tag._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 100)

    def test_tag_slug_max_length(self) -> None:
        test_tag = Tag.objects.get(pk=1)
        slug_max_length = test_tag._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 100)
