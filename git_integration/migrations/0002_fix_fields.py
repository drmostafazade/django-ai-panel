from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('git_integration', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'Repositories'},
        ),
    ]
