from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_delete_role'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserInfo',
        ),
    ]
