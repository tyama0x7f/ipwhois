import csv
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError, WhoisLookupError

import pandas as pd
import json
import ast

# マルチスレッド処理
from concurrent.futures import ThreadPoolExecutor

# マルチスレッド処理の関数
def get_whois(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        return results
    except (IPDefinedError, WhoisLookupError) as e:
        return None
    
# マルチスレッド処理の関数


# 入力ファイル名と出力ファイル名を指定
input_filename = 'input.csv'


# 上の処理をdfに変更
df = pd.read_csv(input_filename, encoding='utf-8-sig')
df['whois'] = None

# マルチスレッド処理
with ThreadPoolExecutor(max_workers=1) as executor:
    results = executor.map(get_whois, df['clientip'])
    for i, res in enumerate(results):
        print(i+1,'行目: ', end='')
        print(df.at[i,'clientip'], end=' ')
        if res is not None:
            print(res)
            df.at[i, 'whois'] = res
        else:
            print('None')


# csvに書き込み。名前はoutput_yyyyMMddhhmmss.csv
output_filename = "output_"+ pd.Timestamp.now().strftime('%Y%m%d%H%M%S') + ".csv"
df.to_csv(output_filename, index=False)


# output.csvを読み込む
df = pd.read_csv(output_filename, encoding='utf-8-sig')

#カラム追加: name
df['name'] = ""

for i in range(len(df)):
    #print(df['clientip'][i], df['所属'][i])
    # whoisはPythonのJSON風の形式になっているので、JSON形式に変換する
    try:
        json_data = ast.literal_eval(df['whois'][i])
        json_data = json.dumps(json_data)
        #print(df['clientip'][i], json_data)
        #print('NOT AMAZON')
        try:
            # json_dataから"name"を取得
            # nir>nets>name
            json_data = json.loads(json_data)
            #print(json_data)
            df.loc[i, 'name'] = json_data['nir']['nets'][0]['name']
        except:
            try:
                # json_dataから"name"を取得
                # asn_description
                df.loc[i, 'name'] = json_data['asn_description']
            except:                    
                # jsonデータを表示
                print(json_data)
                df.loc[i, 'name'] = "#whois_parse_error#"
    except:
        print('json_error')
        df.loc[i, 'name'] = "#json_parse_error#"

# final.csvに書き込む。UTF-8 BOMあり
final_filename = "final_"+ pd.Timestamp.now().strftime('%Y%m%d%H%M%S') + ".csv"
df.to_csv(final_filename, encoding='utf_8_sig', index=False)