# Generated by Django 4.2.1 on 2024-04-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0011_alter_category_options_alter_women_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpLoadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads_model')),
            ],
        ),
    ]
