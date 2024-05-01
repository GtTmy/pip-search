# pip-search

Python Package Compatibility Checker

## 概要
このアプリケーションは、指定されたPythonバージョンに対応するパッケージのバージョンを検索するためのツールです。PyPIからパッケージ情報を取得し、指定されたPythonバージョンと互換性のあるバージョンのリストを提供します。

## 使用方法
コマンドラインからこのスクリプトを実行するには、以下の形式でコマンドを入力します。

```
$ python pip_search/search.py 3.6 typing-extensions
Maximum compatible version for typing-extensions with Python 3.6:
4.1.1
```
