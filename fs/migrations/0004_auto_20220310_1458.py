# Generated by Django 3.2.8 on 2022-03-10 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fs', '0003_alter_contribuable_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribuable',
            name='door_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='geo_situation',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='identity',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='last_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='latitude',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='longitude',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='quarter',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='tel',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
