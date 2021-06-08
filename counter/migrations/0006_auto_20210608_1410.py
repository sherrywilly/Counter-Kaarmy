# Generated by Django 3.2.3 on 2021-06-08 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0005_auto_20210608_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_status',
            field=models.CharField(choices=[('0', 'Open'), ('1', 'Closed')], default='0', max_length=30),
        ),
    ]