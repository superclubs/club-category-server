# Django
from django.db import migrations, models


# Main Section
class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_user_icons_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='religion',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Religion'),
        ),
    ]
