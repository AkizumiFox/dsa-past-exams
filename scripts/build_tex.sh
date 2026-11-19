#!/usr/bin/env bash
# 在 build 目錄裡用 latexmk 編一個 .tex，失敗時印出錯誤並以非零結束。
# latexmk 有時候回傳 0 卻沒有產生新的 PDF（例如它認為「沒有東西要重編」，
# 目錄裡留著上一次編好的舊 PDF），Makefile 就會把舊檔複製到 output/。
# 所以這裡先刪掉舊的 PDF，編完再確認：latexmk 成功、PDF 存在、log 裡沒有錯誤。
# 用法：scripts/build_tex.sh <build 目錄> <檔名.tex> <latexmk 指令與選項...>
set -u
dir=${1:?usage: build_tex.sh <build-dir> <file.tex> <latexmk command...>}
file=${2:?usage: build_tex.sh <build-dir> <file.tex> <latexmk command...>}
shift 2
cd "$dir" || exit 1
base=${file%.tex}
rm -f "$base.pdf"
"$@" "$file" > "$base.latexmk.out" 2>&1
status=$?
# -file-line-error 讓錯誤寫成「檔案:行號: 訊息」，沒有這個選項時是「! 訊息」
err=""
if [ -f "$base.log" ]; then
    err=$(grep -nE -A 6 '^(! |[^ :]+\.(tex|sty|cls|def|cfg|fd|ltx):[0-9]+: )' "$base.log" | head -40)
fi
if [ "$status" -ne 0 ] || [ ! -s "$base.pdf" ] || [ -n "$err" ]; then
    echo "Build failed: $file (latexmk exit $status)"
    if [ -n "$err" ]; then
        echo "$err"
    elif [ -f "$base.log" ]; then
        tail -20 "$base.log"
    else
        tail -20 "$base.latexmk.out"
    fi
    exit 1
fi
