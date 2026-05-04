from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(model_name='schedule', name='participants'),
        migrations.AddField(
            model_name='schedule',
            name='type',
            field=models.CharField(
                choices=[
                    ('meeting', '회의'),
                    ('deadline', '마감일'),
                    ('presentation', '발표'),
                    ('other', '기타'),
                ],
                default='other',
                max_length=20,
            ),
        ),
    ]
