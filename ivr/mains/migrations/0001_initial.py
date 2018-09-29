# Generated by Django 2.1.1 on 2018-09-29 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'auth',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=50)),
                ('isRead', models.CharField(default='0', max_length=20)),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=500)),
                ('time', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'notification',
            },
        ),
        migrations.CreateModel(
            name='Phonelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('star', models.CharField(default='0', max_length=20)),
                ('createTime', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'phonelist',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('callTime', models.CharField(max_length=50)),
                ('callLength', models.CharField(max_length=50)),
                ('digits', models.CharField(max_length=100)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mains.Phonelist')),
            ],
            options={
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='Template_store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', models.CharField(max_length=100)),
                ('pos', models.CharField(max_length=100)),
                ('digit', models.CharField(max_length=20)),
                ('cid', models.CharField(max_length=100)),
                ('flag', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'template_store',
            },
        ),
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'templates',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('pwd', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('regTime', models.CharField(max_length=20)),
                ('auth', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mains.Auth')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='templates',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mains.User'),
        ),
        migrations.AddField(
            model_name='template_store',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mains.Templates'),
        ),
        migrations.AddField(
            model_name='phonelist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mains.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mains.User'),
        ),
    ]
