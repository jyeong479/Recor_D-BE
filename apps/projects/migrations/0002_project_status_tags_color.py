from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(model_name='project', name='is_active'),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(
                choices=[('진행중', '진행중'), ('완료', '완료'), ('중단', '중단')],
                default='진행중',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='project',
            name='color',
            field=models.CharField(
                choices=[
                    ('primary', 'primary'),
                    ('accent', 'accent'),
                    ('secondary', 'secondary'),
                    ('success', 'success'),
                    ('warning', 'warning'),
                    ('destructive', 'destructive'),
                ],
                default='primary',
                max_length=20,
            ),
        ),
    ]
