import pyperclip
from bs4 import BeautifulSoup
import csv
import re
from collections import Counter

# クリップボードからHTMLデータを読み込む
html_data = pyperclip.paste()

soup = BeautifulSoup(html_data, 'html.parser')
# シーン情報の初期化
scene_info = ""
filename_info = ""

# シーン情報を抽出
scene_search = re.search('scene_(\w+)', soup.find('div', class_='prt-log-display')['style'])
if scene_search:
    scene_info = scene_search.group(1)
    filename_info = scene_info
else:
    # シーン情報が抽出できなかった場合の処理
    voice_data_list = []

    for log in soup.find_all('div', class_='prt-log-each'):
        voice_element = log.find('div', class_='btn-play-log-voice')
        if voice_element:
            voice_data_raw = voice_element['data-voice'].replace('voice/', '')
            
            # 最初の_と最後の_の間にある部分を取得
            voice_data_segment = "_".join(voice_data_raw.split('_')[1:-1])
            voice_data_list.append(voice_data_segment)

    # 最も多く出現する要素を取得
    most_common = Counter(voice_data_list).most_common(1)
    if most_common:
        most_common_element = most_common[0][0]
        scene_info = most_common_element
        filename_info = f"{most_common_element}_en"

# CSVファイルのヘッダーを更新
headers = ['Scene', 'Scenario Index', 'Name', 'Message', 'Voice Data']

# データの抽出
data = []
for log in soup.find_all('div', class_='prt-log-each'):
    scenario_index = log['data-scenario-index']
    name = log.find('div', class_='txt-log-name').text.strip()
    message = log.find('div', class_='txt-log-message').text.strip().replace('\n', ' ')
    
    # voice/の削除と存在チェック
    voice_element = log.find('div', class_='btn-play-log-voice')
    voice_data = voice_element['data-voice'].replace('voice/', '') if voice_element else ''
    
    data.append([scene_info, scenario_index, name, message, voice_data])

# シーン情報を元にCSVファイル名を設定
filename = f"{filename_info}.csv"

# CSVファイルの作成
with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:  # エンコーディングをshift_jisに変更
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(data)

print(f"CSV file created: {filename}!")