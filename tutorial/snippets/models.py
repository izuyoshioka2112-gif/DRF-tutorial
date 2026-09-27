from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

# 手動Pygmentsライブラリ
# 一つの言語情報は(表示名, エイリアスのタプル, ファイル拡張子, MIMEタイプ) のタプル→item[1] は「エイリアス」部分(('python', 'py')みたいなやつ)
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])
# Create your models here.


# モデルインスタンス
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    # 以下のコードは先ほど設定したPygmentsライブラリ。タプルから選ぶような形になる
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)
    # 内部に保存する値, 管理画面など表に使う値２つがあるからget_all_stylesは２つのタプル


class Meta:
    ordering = ["created"]
    # Snippetクラスのヤツ。データを取得したら、昇順（古い順）に並び替える役割
