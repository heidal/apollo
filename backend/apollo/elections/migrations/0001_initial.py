# Generated by Django 3.0.3 on 2020-03-18 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('votes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('answers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Question')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
