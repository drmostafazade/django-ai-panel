from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('ai_manager', '0002_alter_aiprovider_options_alter_apikey_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='personal_context',
            field=models.TextField(blank=True, default='', help_text='Context شخصی برای این API Key'),
        ),
    ]
