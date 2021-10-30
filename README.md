
```py
# 產生 10 個 .com 域名
py generate.py 10

# 產生 20 個 .net 域名，輸出檔名為 20211029，並略過域名檢查
py generate.py 20 \
    --top-level=net \
    --file=20211029 \
    --skip
```
