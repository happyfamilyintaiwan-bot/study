# study.knittinghiyori.com：給 Claude Code 的規則

- 學習筆記站（上過的課、公開課、自學）。**內容負責人 Alison**，上架由 Zoe 的 Claude Code 處理。
- 筆記原稿只改 `notes/<主題>/*.md`，主題只改 `topics.json`；改完跑 `python3 build.py`，「0 個問題」才能 push。`index.html`、各主題資料夾是產生出來的，不要手改。
- 筆記內容只整理 Alison 給的材料，不替她編造上課內容或心得。
- 主題卡：主題還沒有筆記時，直接連 `topics.json` 的 `blog`（部落格主力文章）；有筆記後自動改連主題頁。

## 每次開工

1. **確認是誰**：Zoe 的桌機預設是 Zoe；網頁版沒說是誰就先問。
2. **讀規範**（knittinghiyori-specs）：`core.md`、`registry.md`、`CHANGELOG.md`＋`study.md`。
   - 桌機：`~/Sites/knittinghiyori/knittinghiyori-specs` 先 `git pull` 再讀。
   - 網頁版：`https://raw.githubusercontent.com/happyfamilyintaiwan-bot/knittinghiyori-specs/main/<檔名>`
   - 第一句回報各檔版本號與 CHANGELOG 最新一筆；讀不到就停下，不用記憶代替。
3. 分工、不越界、放錯位置、交件 4 項、存檔流程、收工的規範更新包、spec-version，一律照 `core.md` §0。

## 分工（core v1.3）

Alison 只在 claude.ai 寫內容，交件 4 項：放哪、完整 Markdown、英文網址、特別要求；不碰 repo、分支、PR。所有上架由 Zoe 的 Claude Code 處理：從最新的 main 開 `zoe/<主題>` 分支、build 0 問題、驗收、開 PR、squash 合併；內容來自 Alison 時，合併訊息開頭寫「Alison:」。上架只修格式、規範、錯字與技術問題，要改內容的意思先問內容負責人。

本檔由 Zoe 維護。
