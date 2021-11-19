# domain-batch

## 批量產生域名
```py
# 產生 10 個 .com 域名
python generate.py 10

# 產生 20 個 .net 域名，輸出檔名為 20211029，並略過域名檢查
python generate.py 20 \
    --top-level=net \
    --file=20211029 \
    --skip
```

---

## 自動購買域名

### 設定環境變數
api url
api key
api secret
購買域名相關資訊(需填寫真實城市名、(州/省),國家(ISO country code), 電話(會驗證輸入國家的電話格式))

### 網域自動購買指令
單一網域自動購買
```
py buy.py --domain-name xxxxx(輸入域名)
```

多個網域自動購買
```
py buy.py --file xxxxx.txt(輸入域名檔案位置)
```

---

## 透過 godday api 購買域名
```
# 設定購買域名的參數 (apiKey, apiSecret, nameServers ...)
cp buy-conf.example.yaml buy-conf.yaml

# 透過 godaddy api 購買域名
python buy.py ./output/domains.txt
```
