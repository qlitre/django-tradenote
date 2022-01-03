from django.db import models
from mdeditor.fields import MDTextField

# bootstrapのテーマカラー
COLOR_CHOICES = (('primary', 'primary'),
                 ('secondary', 'secondary'),
                 ('success', 'success'),
                 ('info', 'info'),
                 ('warning', 'warning'),
                 ('danger', 'danger'),
                 ('light', 'light'),
                 ('dark', 'dark'))


class Status(models.Model):
    """保有中、終了などのステータス"""
    name = models.CharField(max_length=32)
    color = models.CharField(verbose_name='テーマカラー', choices=COLOR_CHOICES, max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    """勝敗結果"""
    name = models.CharField(max_length=12)
    color = models.CharField(verbose_name='テーマカラー', choices=COLOR_CHOICES, max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """取引モデル"""
    ticker_code = models.CharField(verbose_name='銘柄コード', max_length=12)
    ticker_name = models.CharField(verbose_name='銘柄名', max_length=32)
    status = models.ForeignKey(to=Status, verbose_name='ステータス', blank=True, null=True, on_delete=models.PROTECT)
    date_entry = models.DateField(verbose_name='エントリー日', blank=True, null=True)
    date_close = models.DateField(verbose_name='手仕舞い日', blank=True, null=True)
    result = models.ForeignKey(to=Result, verbose_name='勝敗結果', blank=True, null=True, on_delete=models.PROTECT)
    reason = models.TextField(verbose_name='エントリー理由', null=True, blank=True)
    memo = MDTextField(verbose_name='メモ', default='', null=True, blank=True)
    benefit = models.BigIntegerField(verbose_name='損益', null=True, blank=True)

    def __str__(self):
        return f'#{self.pk} {self.ticker_name}'


class History(models.Model):
    """売買履歴"""
    date_trade = models.DateField(verbose_name='売買日')
    trading_category = models.CharField(verbose_name='売買区分',
                                        max_length=12,
                                        choices=(('Buy', 'Buy'),
                                                 ('Sell', 'Sell'),
                                                 ('Dividend', 'Dividend')))
    target = models.ForeignKey(to=Transaction, verbose_name='対象取引', on_delete=models.PROTECT)
    price = models.FloatField(verbose_name='単価')
    quantity = models.IntegerField(verbose_name='数量')
    commission = models.IntegerField(verbose_name='手数料', null=True, blank=True)
    amount = models.BigIntegerField(verbose_name='受渡金額')
