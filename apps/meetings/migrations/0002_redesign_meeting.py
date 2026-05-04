import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(name='MeetingNote'),
        migrations.RemoveField(model_name='meeting', name='participants'),
        migrations.RemoveField(model_name='meeting', name='location'),
        migrations.RemoveField(model_name='meeting', name='held_at'),
        migrations.AlterField(
            model_name='meeting',
            name='project',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='meetings', to='projects.project',
            ),
        ),
        migrations.AddField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.date.today),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='duration',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='meeting',
            name='participants',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='meeting',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='tags',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='meeting',
            name='transcript',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='ai_summary',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='key_points',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='meeting',
            name='action_items',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='meeting',
            name='is_summarized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='meeting',
            name='summarized_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
