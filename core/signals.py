from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Article

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "core":  # chỉ chạy khi migrate app core
        # Tạo group
        reader_group, _ = Group.objects.get_or_create(name="Reader")
        reporter_group, _ = Group.objects.get_or_create(name="Reporter")

        # Lấy quyền của Article
        content_type = ContentType.objects.get_for_model(Article)
        add_article = Permission.objects.get(codename="add_article", content_type=content_type)
        change_article = Permission.objects.get(codename="change_article", content_type=content_type)
        delete_article = Permission.objects.get(codename="delete_article", content_type=content_type)
        view_article = Permission.objects.get(codename="view_article", content_type=content_type)

        # Gán quyền cho Reporter (CRUD + view)
        reporter_group.permissions.set([add_article, change_article, delete_article, view_article])

        # Gán quyền cho Reader (chỉ view)
        reader_group.permissions.set([view_article])
