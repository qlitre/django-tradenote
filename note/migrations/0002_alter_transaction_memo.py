# Generated by Django 3.2.10 on 2022-01-02 02:02

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='memo',
            field=mdeditor.fields.MDTextField(blank=True, default='', null=True, verbose_name='メモ'),
        ),
    ]
