from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from todo.models import Project, Tag
from todo.forms import TaskForm


class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        for project_id in range(1, 11):
            Project.objects.create(
                name=f"project_name_{project_id}",
                user=test_user,
            )

        for tag_id in range(6):
            Tag.objects.create(
                name=f"tag_name_{tag_id}",
                user=test_user,
            )

    def test_task_form_displays_corresponding_projects_and_tags(self) -> None:
        with patch("todo.forms.get_current_user") as current_user_mock:
            test_user = get_user_model().objects.get(pk=1)
            self.client.force_login(test_user)
            current_user_mock.return_value = test_user

            test_form = TaskForm()
            user_projects = Project.objects.filter(user=test_user)
            user_tags = Tag.objects.filter(user=test_user)

            self.assertEqual(
                list(test_form.fields["project"].queryset), list(user_projects)
            )
            self.assertEqual(
                list(test_form.fields["tags"].queryset), list(user_tags)
            )
