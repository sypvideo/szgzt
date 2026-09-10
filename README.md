# 📖 识字小天地 · 4-6岁 200字识字管理台

一个给 4 岁宝贝用的识字学习管理台：形象字卡、组词、田字格描红笔画练习，目标 **6 岁前认识 200 个常用字**。

纯静态网页（单 HTML 文件），无需服务器、无需数据库，部署到任意静态托管即可运行。

---

## ✨ 功能

| 板块 | 功能 |
|------|------|
| 🏠 工作台 | 学习进度环、每日推荐 5 个新字、13 类分类进度、最近 7 天学习记录 |
| 🃏 字卡乐园 | 200 张形象字卡（象形 emoji + 大字 + 拼音 + 组词）、分类筛选、搜索、大字卡弹窗（含形象记忆口诀 + 真实笔形笔顺） |
| ✍️ 笔画练习 | 田字格描红（触屏/鼠标）、6 色蜡笔、笔顺逐笔图形提示、点字发音 |
| 🔊 发音点读 | 每个汉字旁 🔊 按钮点读，组词可点读，支持慢速跟读、自动朗读、音频缺失时自动降级 |
| 📊 学习报告 | 24 个月里程碑、分类掌握情况、发音设置、音频包检测、导出清单、重置进度 |

字库：200 个常用字，覆盖数字/方位/比一比/颜色/自然/身体/动物/植物/食物/家人/动作/物品/时间 13 大类。

## 📁 文件结构

```
识字小天地/
├── index.html                  # 主程序（自包含，全部逻辑都在里面）
├── vercel.json                 # Vercel 静态托管配置
├── gen_audio.py                # 音频批量生成脚本（edge-tts）
├── 识字小天地-音频文件清单.txt   # 733 个音频文件的完整清单
└── audio/                      # 音频包（发音文件）
    ├── README.md               # 音频规范说明
    ├── chars/                  # 单字读音 200 个，如 水.mp3
    ├── words/                  # 组词读音 533 个，如 喝水.mp3
    └── slow/                   # 慢速单字（可选）
```

## 🔊 音频包（发音功能）

发音采用**预生成音频包**方案：点 🔊 播放 `audio/` 目录里对应的 mp3。

**命名规范：文件名 = 文本本身**，例如 `水.mp3`、`喝水.mp3`（详细规范见 `audio/README.md`）。

**一键生成全部音频：**
```bash
pip install edge-tts
python gen_audio.py            # 生成 200 单字 + 533 组词，约 5~10 分钟
python gen_audio.py --only char # 只生成单字
python gen_audio.py --slow      # 额外生成慢速版
```

**没放音频也能用**：会自动降级到设备自带的浏览器语音朗读（可在「学习报告 → 发音设置」里关闭）。


## 🚀 部署到线上（GitHub + Vercel）

### 第一步：上传到 GitHub

1. 打开 https://github.com/new 创建新仓库
   - Repository name 填：`shizi-200`（可自定义）
   - 选 **Public**（公开，免费）或 Private（私有，Vercel 免费版也能用）
   - 不要勾选 "Add a README file"（避免冲突）
   - 点击 **Create repository**
2. 在仓库页面点 **Add file → Upload files**
3. 把 `index.html`、`vercel.json` 和 **`audio` 文件夹**（发音文件）一起拖进上传区
   > 💡 文件夹可直接拖入浏览器上传区，GitHub 会保留目录结构
   > ⚠️ 音频共 933 个文件（7.5MB），**网页上传可能很慢或中断**，推荐下面两种方式：
   > - **GitHub Desktop**（推荐给非技术用户）：把 `识字小天地` 文件夹拖进软件 → 一键 Publish
   > - **命令行**：`git add . && git commit -m "识字小天地" && git push`
   > - 或者先用网页上传 `index.html` + `vercel.json`（30 秒搞定），音频文件夹之后用 Desktop 补传
4. 点 **Commit changes** 完成上传

> 💡 命令行方式（可选）：
> ```
> cd 识字小天地
> git init && git add . && git commit -m "识字小天地 v1.0"
> git branch -M main
> git remote add origin https://github.com/你的用户名/shizi-200.git
> git push -u origin main
> ```

### 第二步：用 Vercel 部署

1. 打开 https://vercel.com 并登录（推荐用 GitHub 账号一键登录）
2. 点 **Add New… → Project**
3. 在 Import Git Repository 列表里找到刚建的 `shizi-200`，点 **Import**
4. 配置保持默认即可：
   - Framework Preset 会自动识别为 **Other**（静态站，不需要选）
   - Build Command / Output Directory 留空
5. 点 **Deploy**，等待约 1 分钟
6. 部署完成后你会得到一个网址：**`https://shizi-200.vercel.app`**（或随机名），点开即运行 ✅

> 之后每次在 GitHub 更新 `index.html`（Commit 新版本），Vercel 会自动重新部署，无需手动操作。

## 📱 手机上使用

- 手机浏览器打开你的 Vercel 网址即可使用，支持触屏描红
- 添加到主屏幕（iPhone：Safari 分享 → 添加到主屏幕；安卓：浏览器菜单 → 添加到主屏幕），像 App 一样点开就用

## ⚠️ 注意事项

- 学习进度保存在**当前设备的浏览器本地**（localStorage），换手机/电脑是两套独立进度，不会自动同步
- 更新系统时：直接在 GitHub 上传新版本 `index.html` 覆盖即可，不影响已学进度（进度在访问者的浏览器里）
- 部署到线上后，任何知道网址的人都能打开使用，但数据互不相通（各自浏览器独立存储）

## 🛠️ 本地使用（不部署也行）

直接用浏览器双击打开 `index.html` 即可使用，所有功能正常，进度保存在本机浏览器。
