# Generated by Django 5.1.5 on 2025-01-22 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0003_alter_servico_mes_alter_servico_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='mes',
            field=models.CharField(choices=[('January', 'Jan'), ('February', 'Feb'), ('March', 'Mar'), ('April', 'Apr'), ('May', 'May'), ('June', 'Jun'), ('July', 'Jul'), ('August', 'Aug'), ('September', 'Sep'), ('October', 'Oct'), ('November', 'Nov'), ('December', 'Dec')], max_length=10),
        ),
    ]
