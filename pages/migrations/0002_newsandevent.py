# Generated by Django 3.0 on 2020-11-06 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsAndEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, null=True)),
                ('summary', models.TextField(blank=True)),
                ('posted_as', models.TextField(choices=[('News', 'News'), ('Events', 'Events')], null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
