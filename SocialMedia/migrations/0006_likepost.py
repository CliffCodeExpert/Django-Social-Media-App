# Generated by Django 4.2.5 on 2023-10-04 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMedia', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]
