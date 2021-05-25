# Generated by Django 3.2.3 on 2021-05-25 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('0', 'Online'), ('1', 'Leave'), ('3', 'Resigned')], default='1', max_length=10),
        ),
    ]