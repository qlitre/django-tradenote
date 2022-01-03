from django.contrib import admin
from .models import Result, Transaction, History, Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('ticker_code', 'ticker_name', 'memo')
    list_display = ['ticker_code', 'ticker_name', 'date_entry', 'date_close', 'benefit']


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['target', 'date_trade', 'trading_category', 'price', 'amount']


admin.site.register(Status, StatusAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(History, HistoryAdmin)
