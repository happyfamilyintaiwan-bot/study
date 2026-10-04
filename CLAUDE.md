# study.knittinghiyori.com：給 Claude Code 的規則

- 學習筆記站（上過的課、公開課、自學），**負責人 Alison**。
- 筆記原稿只改 `notes/<主題>/*.md`，主題只改 `topics.json`；改完跑 `python3 build.py`，「0 個問題」才能 push。`index.html`、各主題資料夾是產生出來的，不要手改。
- 筆記內容只整理 Alison 給的材料，不替她編造上課內容或心得。

## 每次開工

1. **確認是誰**：Zoe 的桌機預設是 Zoe；網頁版沒說是誰就先問。
2. **讀規範**（knittinghiyori-specs）：`core.md`、`registry.md`、`CHANGELOG.md`＋`study.md`。
   - 桌機：`~/Sites/knittinghiyori/knittinghiyori-specs` 先 `git pull` 再讀。
   - 網頁版：`https://raw.githubusercontent.com/happyfamilyintaiwan-bot/knittinghiyori-specs/main/<檔名>`
   - 第一句回報各檔版本號與 CHANGELOG 最新一筆；讀不到就停下，不用記憶代替。
3. 分工、不越界、放錯位置、存檔流程（DELIVERY 五項）、收工的規範更新包、spec-version，一律照 `core.md` §0。

## Alison

兩人共用同一個 GitHub 帳號，靠分支區分：Alison 一律在 `alison/<主題>` 分支工作、不直接推 main，收工開 PR。
