from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from todo.models import Project, Tag, Task


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        test_user_1 = get_user_model().objects.create_user(
            username="test_user_1", password="test_password"
        )

        test_user_2 = get_user_model().objects.create_user(
            username="test_user_2", password="test_password"
        )

        for project_id in range(1, 11):
            Project.objects.create(
                name=f"project_name_{project_id}",
                user=test_user_1 if project_id % 2 else test_user_2,
            )

        for task_id in range(1, 21):
            Task.objects.create(
                title=f"task_name_{task_id}",
                user=test_user_1 if task_id % 2 else test_user_2,
            )

        for tag_id in range(6):
            Tag.objects.create(
                name=f"tag_name_{tag_id}",
                user=test_user_1 if tag_id % 2 else test_user_2,
            )

    def test_task_list_accessible_by_name(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        url = reverse("todo:task-list")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_task_list_uses_correct_template(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        url = reverse("todo:task-list")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/task_list.html")

    def test_task_list_if_not_logged_in(self) -> None:
        url = reverse("todo:task-list")
        resp = self.client.get(url)

        self.assertNotEqual(resp.status_code, 200)

    def test_task_list_displays_corresponding_tasks(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)

        url = reverse("todo:task-list")
        resp = self.client.get(url)
        user_tasks = Task.objects.filter(user=test_user)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/task_list.html")
        self.assertEqual(list(resp.context["task_list"]), list(user_tasks))

    def test_task_list_displays_corresponding_tags(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)

        url = reverse("todo:task-list")
        resp = self.client.get(url)
        user_tags = Tag.objects.filter(user=test_user)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/task_list.html")
        self.assertEqual(list(resp.context["common_tags"]), list(user_tags))

    def test_project_list_accessible_by_name(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        url = reverse("todo:project-list")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_project_list_uses_correct_template(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        url = reverse("todo:project-list")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/project_list.html")

    def test_project_list_if_not_logged_in(self) -> None:
        url = reverse("todo:project-list")
        resp = self.client.get(url)

        self.assertNotEqual(resp.status_code, 200)

    def test_project_list_displays_corresponding_projects(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)

        url = reverse("todo:project-list")
        resp = self.client.get(url)
        user_projects = Project.objects.filter(user=test_user)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/project_list.html")
        self.assertEqual(
            list(resp.context["project_list"]), list(user_projects)
        )

    def test_project_detail_accessible_by_name(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        url = reverse("todo:project-detail", kwargs={"pk": 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_project_detail_uses_correct_template(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        url = reverse("todo:project-detail", kwargs={"pk": 1})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/project_detail.html")

    def test_project_detail_displays_corresponding_tasks(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)

        url = reverse("todo:project-detail", kwargs={"pk": 1})
        resp = self.client.get(url)
        project_tasks = Task.objects.filter(project_id=1)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "todo/project_detail.html")
        self.assertEqual(list(resp.context["task_list"]), list(project_tasks))

    def test_task_status_toggles_from_false_to_true(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)

        test_task = Task.objects.create(title="test_task", user=test_user)
        self.client.post(
            reverse("todo:task-toggle-completed", kwargs={"pk": test_task.pk})
        )

        test_task.refresh_from_db()
        self.assertEqual(test_task.completed, True)

    def test_task_status_toggles_from_true_to_false(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)

        test_task = Task.objects.create(title="test_task", user=test_user)
        test_task.completed = True
        test_task.save()
        self.client.post(
            reverse("todo:task-toggle-completed", kwargs={"pk": test_task.pk})
        )

        test_task.refresh_from_db()
        self.assertEqual(test_task.completed, False)

    def test_task_detail_forbidden_when_not_owner(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_task = Task.objects.get(pk=2)
        resp = self.client.get(
            reverse("todo:task-detail", kwargs={"pk": test_task.pk})
        )

        self.assertEqual(resp.status_code, 403)

    def test_task_update_forbidden_when_not_owner(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_task = Task.objects.get(pk=2)
        resp = self.client.get(
            reverse("todo:task-update", kwargs={"pk": test_task.pk})
        )

        self.assertEqual(resp.status_code, 403)

    def test_task_delete_forbidden_when_not_owner(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_task = Task.objects.get(pk=2)
        resp = self.client.get(
            reverse("todo:task-delete", kwargs={"pk": test_task.pk})
        )

        self.assertEqual(resp.status_code, 403)

    def test_project_detail_forbidden_when_not_owner(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_project = Project.objects.get(pk=2)
        resp = self.client.get(
            reverse("todo:project-detail", kwargs={"pk": test_project.pk})
        )

        self.assertEqual(resp.status_code, 403)

    def test_project_update_forbidden_when_not_owner(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_project = Project.objects.get(pk=2)
        resp = self.client.get(
            reverse("todo:project-update", kwargs={"pk": test_project.pk})
        )

        self.assertEqual(resp.status_code, 403)

    def test_project_delete_forbidden_when_not_owner(self) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_project = Project.objects.get(pk=2)
        resp = self.client.get(
            reverse("todo:project-delete", kwargs={"pk": test_project.pk})
        )

        self.assertEqual(resp.status_code, 403)

    def test_task_toggle_completed_status_forbidden_when_not_owner(
        self,
    ) -> None:
        self.client.login(username="test_user_1", password="test_password")

        test_task = Task.objects.get(pk=2)
        resp = self.client.post(
            reverse("todo:task-toggle-completed", kwargs={"pk": test_task.pk})
        )

        self.assertEqual(resp.status_code, 403)
