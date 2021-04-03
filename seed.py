from django.contrib.auth.models import User, Group

groups = [
    'Editor',
    'Editor chefe',
    'Chefe de redação',
    'Reporter',
    'Administração',
]
for group in groups:
    Group.objects.get_or_create(name=group)

users = [
    ('admin', 'secret', True),
    ('reporter1', 'secret', False),
    ('editor1', 'secret', False),
    ('editor-chefe1', 'secret', False),
    ('chefe-de-redacao1', 'secret', False),
]

for login, pw, su in users:
    user = User.objects.create_user(login, password=pw)
    user.is_superuser=su
    user.is_staff=True
    user.save()
