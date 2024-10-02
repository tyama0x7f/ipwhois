# 使い方
1. dist\ip_to_whois\ip_to_whois.exeを同じディレクトリにinput.csvを置いてください。
2. ip_to_whois.exeを実行してください。1件あたり2秒程度かかります。
3. すべての実行が完了したら、final_yyyymmddhhmmss.csvというファイルが生成されます。

※output_yyyymmddhhmmss.csvは中間ファイルです。

# サンプルファイル
- input.csv : IPアドレス50件だけのファイルです。
- (600件あるので注意)input.csv : 600件あるファイルです。試す場合はinput.csvにリネームしてください。

# input.csvのフォーマット
以下のようなカラム名が「clientip」である1列のCSVファイルを作成してください。

```
clientip
18.180.61.48
35.75.14.153
54.64.0.104
54.250.76.62
...
...
...
```

エンコーディングは「UTF-8 BOMあり」です。