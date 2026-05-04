from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(model_name='todo', name='assigned_to'),
    ]
