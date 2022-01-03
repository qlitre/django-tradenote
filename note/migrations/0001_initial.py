# Generated by Django 3.2.10 on 2021-12-28 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12)),
                ('color', models.CharField(blank=True, choices=[('primary', 'primary'), ('secondary', 'secondary'), ('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('danger', 'danger'), ('light', 'light'), ('dark', 'dark')], max_length=32, null=True, verbose_name='テーマカラー')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('color', models.CharField(blank=True, choices=[('primary', 'primary'), ('secondary', 'secondary'), ('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('danger', 'danger'), ('light', 'light'), ('dark', 'dark')], max_length=32, null=True, verbose_name='テーマカラー')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker_code', models.CharField(max_length=12, verbose_name='銘柄コード')),
                ('ticker_name', models.CharField(max_length=32, verbose_name='銘柄名')),
                ('date_entry', models.DateField(blank=True, null=True, verbose_name='エントリー日')),
                ('date_close', models.DateField(blank=True, null=True, verbose_name='手仕舞い日')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='エントリー理由')),
                ('memo', models.TextField(blank=True, default='', null=True, verbose_name='メモ')),
                ('benefit', models.BigIntegerField(blank=True, null=True, verbose_name='損益')),
                ('result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='note.result', verbose_name='勝敗結果')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='note.status', verbose_name='ステータス')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_trade', models.DateField(verbose_name='売買日')),
                ('trading_category', models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell'), ('Dividend', 'Dividend')], max_length=12, verbose_name='売買区分')),
                ('price', models.FloatField(verbose_name='単価')),
                ('quantity', models.IntegerField(verbose_name='数量')),
                ('commission', models.IntegerField(blank=True, null=True, verbose_name='手数料')),
                ('amount', models.BigIntegerField(verbose_name='受渡金額')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='note.transaction', verbose_name='対象取引')),
            ],
        ),
    ]