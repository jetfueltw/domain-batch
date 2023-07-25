# domain-batch

## 批量產生域名
```sh
# 產生 10 個 .com 域名
python3.10  generate.py 10

# 產生 20 個 .net 域名，輸出檔名為 20211029，並略過域名檢查
python3.10  generate.py 20 \
    --top-level=net \
    --file=20211029 \
    --skip
```

---

## 批量購買域名 (GoDaddy)
```sh
# 設定配置
cp config.yaml.default config.yaml

# 透過 godaddy api 購買域名
python3.10  purchase.py ./output/domains.txt
```
