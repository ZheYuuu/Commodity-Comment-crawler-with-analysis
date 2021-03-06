# Generated by Django 2.0.4 on 2019-03-26 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JDCommentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodityId', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField()),
                ('picNum', models.IntegerField()),
                ('videoNum', models.IntegerField()),
                ('replyNum', models.IntegerField()),
                ('isTop', models.IntegerField()),
                ('creationTime', models.DateTimeField()),
                ('userLevelName', models.CharField(max_length=50)),
                ('score', models.IntegerField()),
                ('usefulVoteCount', models.IntegerField()),
            ],
            options={
                'db_table': 'jd_comment_detail',
            },
        ),
        migrations.CreateModel(
            name='JDCommentSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodityId', models.CharField(max_length=255, unique=True)),
                ('hotCommentTagStatistics', models.TextField()),
                ('goodRate', models.FloatField()),
                ('commentCountStr', models.CharField(max_length=255)),
                ('poorCountStr', models.CharField(max_length=255)),
                ('generalCountStr', models.CharField(max_length=255)),
                ('goodCountStr', models.CharField(max_length=255)),
                ('videoCountStr', models.CharField(max_length=255)),
                ('afterCountStr', models.CharField(max_length=255)),
                ('imageListCount', models.IntegerField()),
            ],
            options={
                'db_table': 'jd_comment_summary',
            },
        ),
        migrations.CreateModel(
            name='JDCommodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('brand', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('searchKey', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('uniqueId', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'jd_commodity',
            },
        ),
    ]
