## これは何？

bi-gram の マルコフ連鎖を使用した単純な人工無脳です。

chat-nomikaiのクライアントとして動作する mave_proxy.py を同梱しています。

## 環境の構築と起動

chat-nomikaiのクライアントとして動作させる場合、mave_proxyが websoket-client を使用しているため、これをインストールしてください。

```
sudo pip install websocket-client
```

起動は以下。

```
python mave_proxy.py
```

## 学習データ

学習データはJSON形式で覚えています。

* mave_<なまえ>.json.starts
* mave_<なまえ>.json.starts

重み付けを同じ語の多重登録で実現する手抜き実装となっていて、それをそのままシリアライズしているので、データフォーマットは冗長です。

起動時にすべての学習内容をメモリ上の読み出します。これはそのうち問題になるかもしれません。

