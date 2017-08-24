# フィックスポイント プログラミング試験問題 

　言語はPython3.5を用いた. 各フォルダ(AnalysisQ1, AnalysisQ2, AnalysisQ3, AnalysisQ4)ごとに各設問に対応するプログラムとアクセスログファイルを置いて実行する.実装した工夫としてリモートホストと日付の取得に正規表現によるパターンマッチを行った. パターンマッチで抽出できる年は4桁までとした.<br />
　プログラムはQ3まで完成しています.

## Q1. アクセス件数の集計

　AnalysisQ1フォルダ内のAnalysisQ1.pyを実行する.access.logが同フォルダ内にあると想定して実装した. アクセス件数の集計は,1行ずつ読み込むfor文内で実行している. 

### ・各時間帯毎のアクセス件数

各時間帯ごとの集計において, 時(hour)に注目し1時間ごとに集計し結果を出力した. 日付(年/月/日)が違っても, 1時間単位で同じ時間帯に属していれば一緒と見なす. (s.t.18/Apr/2005:00:10:47と28/Apr/2015:00:12:47は時間帯(hour)が一致してるため同類と見なされる.) 集計結果はTimeZoneReport関数で処理する.

### ・リモートホスト別のアクセス件数
　新規のリモートホストは集計用の連想配列に新規のリモートホストアドレスをkeyとし, valueを1にする. 既存のリモートホストは, 対応するkeyを探索しvalueをインクリメントして集計する. 集計結果はRemoteHostReport関数で処理する.

## Q2. 複数ファイルの対応
　AnalysisQ2フォルダ内のAnalysisQ2.pyを実行する. 同フォルダ内にaccess1.log, access2.log, access3.log,...と連続して存在すると仮定して実装した. 複数ファイルが存在しなくなるまでfileIndexをインクリメントしwhile文で制御する.

## Q3. 期間の指定
　AnalysisQ3フォルダ内のAnalysisQ3.pyを実行する. 初めにユーザーに期間の開始と終了の日付を指定してから集計するように実装した. 期間の開始と終了の各々に対しエポック秒を算出し, 読み込んだサーバーリクエストの日付のエポック秒が期間開始と終了のエポック秒の間に属していれば集計をする. 集計結果は指定期間中のみに限定する.

## Q4. 大規模データへの対応
　10GBのデータを集計するとプログラム中の変数に値がスタックされていき,やがてある瞬間からスタックオーバーフローしてしまう.マシンメモリーが2GBの環境でも動くようにスタックレスにしないといけない.<br/>　スタックされるデータは, 別ファイルreport.txtに集計する度にデータを書き出しておく.(例.集計する変数であるtimeZoneTotalやremoteHostTotalなど) 集計結果の際にはreport.txtを読み込んで結果を出力する.
