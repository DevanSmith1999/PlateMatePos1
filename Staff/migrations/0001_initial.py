# Generated by Django 4.2.6 on 2024-04-04 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FOH', 'FOH'), ('BOH', 'BOH')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent_position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subpositions', to='Staff.position')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=4, unique=True)),
                ('Date_of_birth', models.CharField(max_length=100, null=True)),
                ('positions', models.ManyToManyField(related_name='staff', to='Staff.position')),
                ('subposition', models.ManyToManyField(related_name='staff', to='Staff.subposition')),
            ],
        ),
    ]
