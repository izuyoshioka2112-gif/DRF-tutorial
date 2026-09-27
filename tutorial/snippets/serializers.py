from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# SnippetインスタンスをJSONなどの形式にシリアライズ（変換) や戻す役割


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style"]


# モデルに書いてあることじゃない設定をしたいときはシリアライズを１から書けばいいが、モデルをそのままシリアライズしたいなら、このModelSerializerで良い
