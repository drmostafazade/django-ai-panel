from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('git_integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubtoken',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='repository',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='repository',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='repository',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='repository',
            name='html_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
