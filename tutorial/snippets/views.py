from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# この二行のおかげでデータのシリアライズやModelとのやり取りができる
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# モデルとシリアライズはシリアライズ.pyの方に書いてるから繋がっているが、viewsはモデルもシリアライズも操るのにどっちとも繋がっていないから書く必要あり


@api_view(["GET", "POST"])
# APIをラップ
def snippet_list(request, format=None):
    if request.method == "GET":
        # JSONを受け取るのではなく、見せて〜とお願いしてくることがほぼ
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    # リスポーンだけで型を設定せず返せる〜
    # safe=False→リストということを明確に！
    elif request.method == "POST":
        serializer = SnippetSerializer(data=request.data)
        # requestがjsonじゃなくても何でも対応できるからここの一語だけで、jsonにdataを変更してから使わなくてすむ
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # わかりやすくエラーにお名前つけた


# Snippetの取得（retrieve）、更新（update）、削除（delete）に使用
@api_view(["GET", "PUT", "DELETE"])
def snippet_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # HttpResponse→HTMLやプレーンテキストなどのレスポンスを返すための基本的なクラス→でももう指定しなくて良い！

    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        # シリアライズしてる＝Jsonに変換
        return Response(serializer.data)
    # Jsonにして返す
    elif request.method == "PUT":
        # JSONParser は、JSON形式のデータをPythonの辞書型に変換するクラス→でもいらない！
        serializer = SnippetSerializer(snippet, data=request.data)
        # Jsonを解いて、制約通りデータがあるなら保存する
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # 消す
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
