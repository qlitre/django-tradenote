from django.views import generic
from .models import Transaction, History
from .forms import TransactionSearchForm, HistoryCreateForm, TransactionCreateForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django_pandas.io import read_frame
import pandas as pd
import numpy as np


class TransactionList(generic.ListView):
    model = Transaction
    template_name = 'note/index.html'
    ordering = ('status', '-date_close')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TransactionSearchForm
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = TransactionSearchForm(self.request.GET or None)
        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 銘柄コード、銘柄名、エントリー理由、メモが対象
                for word in key_word.split():
                    queryset = queryset.filter(
                        Q(ticker_code__icontains=word) |
                        Q(ticker_name__icontains=word) |
                        Q(reason__icontains=word) |
                        Q(memo__icontains=word)
                    )

        return queryset


class TransactionDetail(generic.DetailView):
    model = Transaction
    template_name = 'note/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['breadcrumbs_list'] = [
            {'name': f'#{pk} {self.object.ticker_name}',
             'url': ''}
        ]
        context['history_create_form'] = HistoryCreateForm

        return context


class HistoryCreate(generic.CreateView):
    """
    売買履歴作成ビュー
    取引詳細ページのフォームからpkを受け取り、モデル保存処理をする
    """
    model = History
    form_class = HistoryCreateForm

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        transaction = get_object_or_404(Transaction, pk=pk)
        price = float(self.request.POST.get('price'))
        quantity = int(self.request.POST.get('quantity'))
        commission = self.request.POST.get('commission')
        commission = int(commission) if commission else 0
        category = self.request.POST.get('trading_category')

        amount = price * quantity
        if category == 'Buy':
            amount += commission
        else:
            amount -= commission

        history = form.save(commit=False)
        history.target = transaction
        history.amount = amount
        history.commission = commission
        history.save()

        return redirect('note:detail', pk=pk)


class HistoryDelete(generic.DeleteView):
    """売買履歴削除ビュー"""
    model = History

    def get_success_url(self):
        target_pk = self.object.target.pk
        return reverse_lazy('note:detail', kwargs={'pk': target_pk})


class TransactionCreate(generic.CreateView):
    model = Transaction
    template_name = 'note/transaction_create.html'
    form_class = TransactionCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs_list'] = [{'name': 'Transaction Create',
                                        'url': ''}]

        return context

    def get_success_url(self):
        return reverse_lazy('note:transaction_list')


class TransactionUpdate(generic.UpdateView):
    model = Transaction
    template_name = 'note/transaction_create.html'
    form_class = TransactionCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        referer = self.request.environ.get('HTTP_REFERER')
        # detailページから来た場合
        if 'detail' in referer:
            context['breadcrumbs_list'] = [
                {'name': f'#{pk} {self.object.ticker_name}',
                 'url': f'/detail/{pk}/'},
                {'name': 'Transaction Update',
                 'url': ''}
            ]
        # トップページから来た場合
        else:
            context['breadcrumbs_list'] = [
                {'name': 'Transaction Update',
                 'url': ''}
            ]

        benefit = 0
        for history in History.objects.filter(target=pk):
            if history.trading_category == 'Buy':
                benefit -= history.amount
            else:
                benefit += history.amount

        context['benefit'] = benefit

        return context

    def get_success_url(self):
        view_name = 'note:detail'
        pk = self.object.pk

        return reverse_lazy(view_name, kwargs={'pk': pk})


class DashBoard(generic.TemplateView):
    model = Transaction
    template_name = 'note/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs_list'] = [{'name': 'Dashboard',
                                        'url': ''}]

        # Closeしているもののみを評価　※Closeはidが2
        queryset = Transaction.objects.filter(status=2)

        if not queryset:
            return context

        df = read_frame(queryset, fieldnames=['date_close', 'result', 'status', 'benefit'])

        # ===通算損益の計算=== #
        total_benefit = df['benefit'].sum()
        context['total_benefit'] = total_benefit

        # ===勝率の計算=== #
        total_trade_count = len(df)
        win_count = len(df[df['result'] == 'Win'])
        win_ratio = round(win_count / total_trade_count, 2) if win_count else 0
        lose_ratio = 1 - win_ratio
        context['win_ratio'] = win_ratio
        context['lose_ratio'] = lose_ratio

        # ===平均利益・平均損失の計算 === #

        # {'Lose': {'benefit': 値}, 'Win': {'benefit': 値}}という辞書になる
        dic = pd.pivot_table(df, values='benefit', columns='result', aggfunc=np.sum).to_dict()
        if dic.get('Win'):
            total_profit = dic.get('Win')['benefit']
            avg_profit = int(round(total_profit / win_count, 0))
        else:
            avg_profit = 0

        if dic.get('Lose'):
            lose_count = total_trade_count - win_count
            total_loss = dic.get('Lose')['benefit']
            avg_loss = int(round(total_loss / lose_count, 0))
        else:
            avg_loss = 0

        context['avg_profit'] = avg_profit
        context['avg_loss'] = avg_loss

        # === リスクリワード比率の計算 === #

        risk_reward_ratio = None
        if not avg_profit:
            risk_reward_ratio = 0
        elif avg_profit and avg_loss:
            risk_reward_ratio = round(avg_profit / abs(avg_loss), 2)
        context['risk_reward_ratio'] = risk_reward_ratio

        # === 月間の損益推移グラフの素材計算 === #

        df['date_close'] = pd.to_datetime(df['date_close'])
        df['month'] = df['date_close'].dt.strftime('%y-%m')

        df_pivot = pd.pivot_table(df, index='month', values='benefit', aggfunc=np.sum)
        context['month_list'] = [month for month in df_pivot.index.values]
        context['benefit_list'] = [val[0] for val in df_pivot.values]

        return context
