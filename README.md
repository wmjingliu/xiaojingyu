# 小鲸鱼：ChatGPT/Codex 桌面宠物

![小鲸鱼待机动画](showcase/00-idle-slow.gif)

小鲸鱼是一套给 **ChatGPT/Codex 桌面应用**使用的自定义宠物图片。安装并在应用里选中后，蓝发、带鲸鱼尾巴的小女仆会作为桌面上的悬浮宠物出现。它会随聊天状态显示待机、工作、等待你回答、完成和出错等动作。

这个仓库提供的是**宠物素材**，不是需要双击运行的独立软件。它不会替你安装 ChatGPT/Codex，也不会改变 AI 的回答能力。安装当前发布版不需要 Python、Git、API Key 或付费图片生成服务。

> **适用范围：**下面的步骤按 **Windows 桌面版**编写，已在本地桌面应用 `26.930.7945.0` 的 v2 宠物格式上核对。它不适用于把图片直接上传到 ChatGPT 网页版的「Upload pet」入口；网页版要求的精灵图尺寸不同。其他桌面版本如果不识别，请先更新应用并查看[常见问题](#常见问题)。

## 先看效果

这里先展示三个常见状态；下载并解压项目后，双击 `showcase/index.html` 可以在浏览器中看完整动画。预览里的“慢速”GIF 方便看清像素细节；安装后的播放速度由桌面应用决定，不会因为慢速预览而变慢。

| 正在工作 | 等待你回答 | 完成且未读 |
|---|---|---|
| ![敲键盘](showcase/07-running-slow.gif) | ![问号气泡](showcase/06-waiting-slow.gif) | ![挥手和勾号](showcase/08-review-slow.gif) |

| 你在做什么 | 小鲸鱼大致会怎样 |
|---|---|
| 没有正在处理的聊天 | 站立待机 |
| 聊天正在运行 | 伏案敲键盘 |
| 聊天需要你回答或批准 | 疑惑，并出现问号 |
| 聊天完成且有未读内容 | 轻挥手，并出现勾号 |
| 聊天失败或被阻塞 | 显示委屈动作 |

**播放限制：**在已核对的桌面版本中，工作等非待机动作播放约三轮后会回到待机；“完成”通常只在结果尚未读过时出现。素材包无法改变应用的播放规则，所以小鲸鱼不一定会一直敲键盘。详见[状态与限制](docs/runtime.md)。

## 安装到 Windows 桌面应用

以下只用浏览器、文件资源管理器和 ChatGPT/Codex 桌面应用。请先确认桌面应用已经安装并能在 **Settings → Pets** 看到宠物设置；如果没有这个页面，请先更新应用或检查当前工作区是否开放 Pets。

### 第 1 步：下载并解压项目

1. 打开本仓库主页：<https://github.com/wmjingliu/xiaojingyu>。
2. 点击绿色的 **Code** 按钮，再点击 **Download ZIP**。
3. 在“下载”文件夹中找到 `xiaojingyu-main.zip`，右键选择 **全部解压缩**（或 **Extract All**）。
4. 打开解压后的 `xiaojingyu-main` 文件夹。你应能看到 `README.md` 和 `pet` 文件夹。

> 只需安装 `pet` 文件夹里的三个文件。`assets`、`scripts`、`docs` 和 `showcase` 是项目素材、工具与说明，不需要复制到宠物安装位置。

### 第 2 步：打开宠物安装位置

1. 打开 Windows **文件资源管理器**。
2. 点击窗口顶部的**地址栏**，粘贴下面这一行，然后按 **Enter**：

   ```text
   %USERPROFILE%\.codex\pets
   ```

3. 如果 Windows 提示该位置不存在，先在地址栏输入 `%USERPROFILE%` 并按 Enter；在打开的文件夹里依次新建 `.codex` 和 `pets` 文件夹，然后进入 `pets`。

`%USERPROFILE%` 会自动指向你自己的 Windows 用户文件夹，不要把它改成别人的用户名。如果你特意设置过 `CODEX_HOME`，安装位置是 `CODEX_HOME\pets`；普通用户通常无需处理这一项。

### 第 3 步：复制小鲸鱼文件

1. 在 `pets` 文件夹里新建一个文件夹，名称**必须**是 `xiaojingyu-keleus`。
2. 如果这里已经有同名文件夹，先把旧文件夹**复制**到桌面留作备份，再继续下一步。
3. 回到解压出的 `xiaojingyu-main\pet` 文件夹，选中其中的 `pet.json`、`spritesheet.png` 和 `LICENSE.txt`，复制到 `pets\xiaojingyu-keleus`。如果 Windows 询问是否替换同名文件，选择替换。

复制完成后，文件结构应当是这样：

```text
你的用户文件夹
└─ .codex
   └─ pets
      └─ xiaojingyu-keleus
         ├─ pet.json
         ├─ spritesheet.png
         └─ LICENSE.txt
```

请特别检查：`xiaojingyu-keleus` 里应**直接**看到这三个文件，而不是再套一层 `pet` 文件夹。不要重新保存、缩放或压缩 `spritesheet.png`，否则像素清晰度和动画格可能受到影响。

### 第 4 步：在应用里启用

1. 打开 ChatGPT/Codex **桌面应用**。
2. 打开 **Settings → Pets**（设置 → 宠物）。
3. 点击 **Refresh**（刷新），在宠物列表中选择 **小鲸鱼**。
4. 如果宠物没有出现在桌面，回到聊天输入框输入 `/pet`，或从应用的命令菜单选择 **Show pet**（显示宠物）。

到这里安装完成。官方 [Pets 使用说明](https://learn.chatgpt.com/docs/pets) 也介绍了宠物的选择、刷新和显示方式。

## 常见问题

### 宠物列表里找不到“小鲸鱼”

先检查第 3 步的文件夹名称和层级，尤其是 `pet.json` 是否直接位于 `xiaojingyu-keleus` 中。然后在 **Settings → Pets** 再点一次 **Refresh**。仍找不到时，完全退出并重新打开桌面应用；同时确认桌面版已经更新且当前账户或工作区支持 Pets。

### 选中了宠物，但桌面上看不到

在聊天框输入 `/pet`，或使用命令菜单中的 **Show pet**。宠物也可能被右键菜单里的 **Hide** 隐藏。Windows 默认快捷键 **Win + Alt + P** 可显示悬浮控件；如果快捷键被改过，以应用设置为准。

### 动作太快、工作时又变回待机，或只看到静止图片

慢速 GIF 只是预览。桌面应用决定真实动作的帧速和播放轮数；已核对版本中，工作动作约 2.46 秒后会回到待机。若所有动作都静止，检查 Windows 是否启用了“减少动画”之类的动态效果设置。详情见[状态与限制](docs/runtime.md)。

### 想恢复原来的宠物

如果第 3 步把旧的 `xiaojingyu-keleus` 文件夹备份到了桌面，可把备份中的文件复制回同名安装文件夹，再到 **Settings → Pets** 点击 **Refresh**。如果只是想换成内置宠物，直接在宠物列表中选择其他宠物即可。

### 能直接上传到 ChatGPT 网页版吗？

不能直接用这里的 `spritesheet.png` 上传。这个仓库使用桌面应用的 **v2 精灵图**（1536 × 2288）；官方网页版上传入口要求另一种尺寸。桌面安装的自定义宠物也不会自动同步到网页版。

## 项目文件说明

| 路径 | 用途 | 普通安装是否需要 |
|---|---|---|
| `pet/` | 当前可安装的宠物文件 | **需要**，复制其中三个文件 |
| `showcase/` | 慢速、原速和状态示意动画 | 可选，安装前预览 |
| `assets/` | 保留像素清晰度的基底和状态图层 | 不需要 |
| `scripts/` | 开发者构建、格式核对和安装工具 | 不需要 |
| `docs/` | 来源、技术说明及运行限制 | 不需要 |

### 给维护者：构建与验证

当前发布精灵图为 **1536 × 2288** 的透明 PNG，8 列 × 11 行，每格 192 × 208 像素，共有 73 个必需动画格。SHA-256：

```text
b9f89cb64753b051b5bdb2a86c36b5898d3265462029002f720b2a1c8ea43566
```

维护者可安装 Python 依赖并在项目根目录运行以下命令；**普通安装无需执行**：

```powershell
python -m pip install -r requirements.txt
python scripts/build_release.py
python scripts/validate_release.py
python scripts/check_project.py
```

构建脚本从 `assets/clarity-base.png` 和两张状态图层离线重建发布图，并比较哈希；它默认不会覆盖 `pet/spritesheet.png`。`scripts/install_release.py` 是带格式核对、哈希确认和备份的高级安装工具，需要先定位当前桌面应用的 `resources/app.asar`；新手请使用上面的文件复制步骤。格式或应用版本发生变化时，不应假定旧脚本仍适用。

## 来源与许可

角色源自 [`keleus/deepseek-pet`](https://github.com/keleus/deepseek-pet) 的提交 `b9b61a35c3b2443ecdeab0ed442d6b33c603d343`，原仓库声明 MIT，版权为 `Copyright (c) 2026 keleus <jen.hs@outlook.com>`。许可全文见 [LICENSE](LICENSE)。当前清晰化基底包含此前经 AI 辅助补绘的衍生画面；来源与构建边界见[来源说明](docs/source.md)。
