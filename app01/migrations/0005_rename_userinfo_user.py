from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_rename_user_userinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserInfo',
            new_name='User',
        ),
    ]
