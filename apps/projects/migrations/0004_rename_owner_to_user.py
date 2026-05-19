from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_update_status_and_color_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='owner',
            new_name='user',
        ),
    ]
