# Generated by Django 5.1.5 on 2025-01-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicerequest',
            old_name='submitted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='servicerequest',
            old_name='customer',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='resolved_at',
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
