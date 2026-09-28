from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# この二行のおかげでデータのシリアライズやModelとのやり取りができる
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# クラスベースビューでAPIをかく＝urls.pyもリファクタリング（編集）する必要ある
class SnippetList(APIView):
    """
    Snippetの一覧を取得、もしくは新しいSnippetを作成する。
    """

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Snippetの取得（retrieve）、更新（update）、削除（delete）に使用
class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404  # raise→エラーを意図的に発生させる。という命令
            # return Response(status=status.HTTP_404_NOT_FOUND)と同じで、DRFが用意している専用の例外クラス（Http404)があって、自動的にレスポンスを作って返してくれる

    def get(self, request, pk, format=None):
        # プライマリーキーの略で、/1/などを取得
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        # どの行、どのデータをいじるのか示さないといけないからデータをここに入れるためにpkを使って入れてる
        serializer = SnippetSerializer(snippet, data=request.data)
        # ↑ここのsnippetこれが主に示してくれてる
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
