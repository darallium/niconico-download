[![Build](https://github.com/darallium/niconico-download/actions/workflows/build.yaml/badge.svg?event=deployment_status)](https://github.com/darallium/niconico-download/actions/workflows/build.yaml)
# nico-dlp GUI

ニコニコ動画の動画をダウンロードするためのシンプルなGUIアプリケーションです。yt-dlp と aria2c を利用して、高画質・高速なダウンロードを実現します。

## 機能

* ニコニコ動画の動画URLを入力してダウンロード
* ダウンロード設定をGUIでカスタマイズ可能
    * 出力ファイル名テンプレート
    * 動画の品質 (フォーマット)
    * aria2c のダウンロードオプション
    * メタデータの追加、サムネイルの埋め込み、字幕のダウンロード、コメントの取得など、様々なオプション
* 設定を`config.conf`ファイルに保存し、次回起動時に読み込み
* aria2c が無い場合はダウンロードページを案内

## スクリーンショット

![image](https://github.com/user-attachments/assets/4a4d5651-0396-4d1d-a09c-3da191c18253)



# 開発者向け

## 依存関係

* Python 3.7+
* customtkinter
* CTkMessagebox
* yt-dlp
* aria2c
* rye
* ruff
