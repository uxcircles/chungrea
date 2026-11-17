# Chung & Rea：重新設計概念網站

這是 UX CIRCLES 為格拉斯哥 **Chung & Rea Solicitors & Notaries Public**（CCMC Limited，公司編號 SC534437）製作的重新設計概念網站，**並非官方網站**。每頁頂部都有概念標示，全站設 `noindex, nofollow`，`robots.txt` 禁止搜尋引擎收錄。

- 線上版本：https://uxcircles.github.io/chungrea/
- 官方網站：https://chungrea.com/

## 頁面

| 英文 `/` | 繁體 `/zh/` | 简体 `/sc/` |
|---|---|---|
| `index.html` 首頁（上訴期限工作紙、服務、法律援助、語言、地圖） | 同左 | 同左 |
| `services.html` 服務範圍及期限 | | |
| `contact.html` 聯絡、預約表格、地圖 | | |
| `privacy.html` 私隱聲明（草稿） | | |
| `accessibility.html` 無障礙聲明 | | |
| `404.html`（只有英文，GitHub Pages 通用） | | |

## 如何修改

所有頁面由 `_build/pages.py` 產生，文字寫成 `L(英文, 繁體)`；簡體由 OpenCC（hk2s）自動轉換，再按 `SC_WORDS` 換成內地用詞，也可以給 `L()` 第三個參數直接指定簡體。

```bash
pip install opencc-python-reimplemented
python3 _build/pages.py      # 重建 HTML
python3 _build/fonts.py      # 改過中文字後重新子集化字體
```

修改 CSS / JS 後，請把 `pages.py` 裏的 `V` 加一（cache-bust）。

## 設計概念

- **招牌元素：五角形。** 辦公室位於 Pentagon Centre，五角形用於標誌、地圖圖釘、favicon、手機按鈕及 404 頁。
- **Hero 類型：`document-object`。**（第二版：去掉橫線紙、傾斜、印章、編號圈及等寬字體，畫面更簡潔） 首屏是一張「拒絕信工作紙」：輸入信件寄出日期、選擇身在英國境內或境外，即時算出上訴表格一般須送達的日期（14 日或 28 日，週末順延）及剩餘日數，並可把期限帶入預約表格。標明「只屬估算，並非法律意見」。
- **字體：** Young Serif（標題）、Schibsted Grotesk（內文）；中文用 Noto Serif / Sans TC 及 SC，只子集化網站用到的字。
- **顏色：** 法律援助藍 `#1f2a8f`（取自蘇格蘭法律援助委員會標誌）、格拉斯哥紅砂岩 `#a5442d`（市內維多利亞式建築）、紙白。
- **標題：** "Bring the letter to Washington Street"／「收到內政部的信，帶來 Washington Street 給我們看」。
- **與同類網站的分別：** 之前的律師網站（Chu & Company、Lu Oliphant、Lee & Kan）都是左文右圖／資料卡、Fraunces／Newsreader／Manrope 字體及斜體重點字；這個網站沒有照片、沒有拱形圖框、沒有斜體重點，首屏是一件可以使用的「文件」。

## 資料來源

- 地址、電話、傳真、電郵、服務範圍、「Solicitors & Notaries Public」、CCMC Limited 及註冊辦事處：chungrea.com（2026 年 11 月 17 日查閱）
- 公司資料（SC534437，2016 年 5 月 4 日成立，SIC 69102 律師）：Companies House
- 法律援助登記、移民／庇護／國籍個案「Active」、輪椅通道、附近泊車、上門探訪、員工說廣東話及普通話、無感應環路：蘇格蘭法律援助委員會律師名錄 https://slab.org.uk/solicitor-finder/ccmc-limited-t-a-chung-and-rea-solicitors
- 上訴期限：First-tier Tribunal (IAC) Procedure Rules 2014 第 19 條（境內 14 日、境外 28 日）；司法覆核：Court of Session Act 1988 第 27A 條（三個月）
- 步行時間：routing.openstreetmap.de 步行路線（Anderston 266 米約 3 分鐘；Glasgow Central 866 米約 11 分鐘）

## 需要律師行確認

- 各服務的細項描述（例如家庭簽證、羈留保釋、公證服務內容）是按一般業務範圍撰寫，需由律師行確認。
- 辦公時間不詳，網站寫「會面須預約」。
- 現有網站稱「距 Glasgow Central 少於 5 分鐘步行」，實際步行路線約 11 分鐘；本網站採用路線計算結果。
- 私隱聲明及無障礙聲明是草稿（現有網站沒有），需律師行審閱。
- 沒有使用任何人物照片或圖庫照片。
