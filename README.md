# Mt. Gox Alert
Mt. Gox のアドレスを監視して、twitter および line に通知を送る。

## How to use
.apisecret に通知に必要となる鍵を記入。  
必要なパッケージを
`pip install urllib3 pandas twitter`
によりインストール。  
`python MtGoxAlert.py`
として稼働。

## twitter
一般利用では、twitterへの通知機能は必要ありません。  
[MTGoxBot] <https://twitter.com/whale_NK> を試験運用中です。

## line
line に通知するために必要な鍵を [LINE Notify]<https://notify-bot.line.me/ja/> にて作成。  
.apisecret の line_token の欄に記入。  
