# gbflog

グラブルのテキストをcsv形式で保存するPythonのスクリプトです。
98%がChatGPTで作られています。
Pythonうまおはいい感じに編集してください。

コードの挙動は
1 クリップボードを読み込みprt-log-display classを含む目的の形式か判定する。trueなら次へ。

2  各classを検索し、シーン名、キャラ名、セリフ、関連するボイスのmp3の表を作る。

3  シーン名.csvで2の内容をcsv出力。言語設定が英語の場合_enを末尾につけて出力。
