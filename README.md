# django-tradenote

## 概要
djangoとMDB(Material Design for Bootstrap v5 & v4)の株取引ノートアプリです。

## 画面イメージ

### トップページ

![image](https://user-images.githubusercontent.com/77523162/147900039-43291dea-d4bd-4f37-92c3-b76defcf53ba.png)

### 取引登録、編集ページ
マークダウンに対応しています。

![image](https://user-images.githubusercontent.com/77523162/147900056-34b37dda-f4c2-47d3-85b2-4836d70a31ed.png)

![image](https://user-images.githubusercontent.com/77523162/147900062-47e44e85-5df8-414e-85c5-b336aceb55a7.png)

### 売買履歴の追加
モーダルで取引詳細ページから追加できます。

![image](https://user-images.githubusercontent.com/77523162/147900068-c00c36b1-d392-4f0b-b6f8-40f907c54fd3.png)

### ダッシュボードページ

![image](https://user-images.githubusercontent.com/77523162/147900074-0f88c1ef-dfe0-48c9-a62f-e77a2e028da5.png)

## つかいかた

適当なディレクトリを作りgit cloneしてください。

```
git clone https://github.com/qlitre/django-tradenote
```

次に仮想環境を作成し、ライブラリをインストールしてください。

```
python -m venv myvenv
myvenv\scripts\activate
pip install -r requirements.txt
```

migrateをします。

```
python manage.py migrate
```

次に初期データの投入です。

```
python manage.py loaddata initial.json
```

runserverして株取引ノートをお楽しみください。

```
python manage.py runserver
```

## チュートリアル
ブログにまとめました。
https://qlitre-weblog.com/django-tradenote
