# study.knittinghiyori.com：學習筆記

上過的課、公開課、自學主題的筆記站。內容負責人：Alison（在 claude.ai 寫好交給 Zoe）；上架：Zoe 的 Claude Code。

## 怎麼寫一篇新筆記（3 步）

1. 複製 `notes/_範例筆記.md` 到 `notes/<主題>/`，檔名改成英文小寫＋連字號，例：`notes/cs50/week-0-scratch.md`
2. 改最上面的 `title`、`date`、`summary`、`source`，刪掉 `draft: true` 那一行，下面用 Markdown 寫內容
3. 執行下面這行，看到「0 個問題」才 push：

```bash
python3 build.py
```

## 怎麼加新主題

在 `topics.json` 加一筆（照現有的格式），再建資料夾 `notes/<id>/`。

- `kind`：公開課／自學／上過的課（首頁照這三區分組）
- `status`：進行中／已完成／想學（「想學」會放在首頁最下面的想學清單）
- `blog`：這個主題的部落格主力文章；還沒有筆記時，首頁卡片直接連過去
- `mark`：卡片角落圓形貼紙上的 1～3 個字（例：`</>`、`あ`）
- `color`：紙膠帶與貼紙顏色，只用 sora／peach／lavender／sakura／matcha／lemon

## 檔案在哪

| 檔案 | 做什麼 | 要手改嗎 |
|---|---|---|
| `notes/<主題>/*.md` | 筆記原稿 | ✅ 寫筆記改這裡 |
| `topics.json` | 主題清單 | ✅ 加主題改這裡 |
| `build.py` | 把筆記變成網頁＋上線前檢查 | 很少 |
| `assets/study.css` | 版面配色 | 很少 |
| `index.html`、`<主題>/`、`sitemap.xml`、`404.html` | build 產生的 | ❌ 不要手改，會被蓋掉 |

## 還沒做的

- AdSense 單元、Travelpayouts Drive 還沒建：填進 `build.py` 的 `ADS_SLOT`、`DRIVE`（目前不放廣告）
- 分享預覽圖暫用 story 的 `icons/og-cover.jpg`，之後可以換 study 專屬的
