from task_manager.models import Tag


def generate_tags(self, stdout):
    """Создание тегов"""
    stdout.write('\n1. Создание тегов...')
    Tag.objects.all().delete()

    tag_names = ['bug', 'feature', 'urgent', 'test', 'deploy', 'security', 'documentation']
    tags = []
    for name in tag_names:
        tag = Tag(name=name)
        tag.save()
        tags.append(tag)
        stdout.write(f'   Создан тег: {name}')

    return tags