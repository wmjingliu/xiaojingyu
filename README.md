# 小鲸鱼 · 桌面自定义桌宠

蓝发女仆与鲸鱼尾巴角色的本地 v2 精灵图项目，身份固定为 `custom:xiaojingyu-keleus`。这是桌面应用的**素材包**，不是独立桌宠程序，也不修改应用安装包。

## 当前发布版

- 安装文件：`pet/`（`pet.json`、`spritesheet.png`、`LICENSE.txt`）。
- 精灵图 SHA-256：`b9f89cb64753b051b5bdb2a86c36b5898d3265462029002f720b2a1c8ea43566`。
- 格式：1536×2288 RGBA、8 列×11 行、每格 192×208；73 个必需动画格。
- 完成未读：轻挥手与勾号；等待输入：问号气泡。人物像素来自已确认的清晰化基底，没有再次缩放。
- [逐状态预览](showcase/index.html)含慢速观感与应用原速对照。慢速预览不会改变应用的播放时长。

## 目录

| 路径 | 用途 |
|---|---|
| `pet/` | 可安装的当前素材包 |
| `assets/clarity-base.png` | 冻结的清晰化基底；构建输入 |
| `assets/*-overlays.png` | 六帧状态标记图层；构建输入 |
| `scripts/build_release.py` | 离线重建当前精灵图并核对哈希 |
| `scripts/validate_release.py` | 检查 v2 结构与全部必需格 |
| `scripts/verify_app_format.py` | 只读检查本机应用是否仍使用已知 v2 格式 |
| `scripts/install_release.py` | 默认预检；显式确认哈希后备份并安装 |
| `scripts/audit_runtime.py` | 只读检查当前桌面悬浮层状态播放逻辑 |
| `showcase/` | 逐行动画与实际调度示意 GIF |
| `docs/` | 来源、许可及运行态限制 |

## 本地验证

安装 Python 依赖后，在项目根目录运行：

```powershell
python -m pip install -r requirements.txt
python scripts/build_release.py
python scripts/validate_release.py
python scripts/check_project.py
```

`build_release.py` 默认只在内存重建并比较 `pet/spritesheet.png`，不覆盖文件。上述三项检查均应通过，重建哈希应与上面的发布版哈希一致。无需 API key 或联网生成图片。

## 本机安装

先查看 `showcase/index.html`，确认当前哈希对应的外观，再找到**当前**桌面应用的 `resources/app.asar` 路径。安装器只认已核实的 v2 格式；未知版本会停止。

```powershell
python scripts/verify_app_format.py --asar "<当前应用的 resources/app.asar>"
python scripts/install_release.py --asar "<当前应用的 resources/app.asar>"
python scripts/install_release.py --asar "<当前应用的 resources/app.asar>" --approved-hash b9f89cb64753b051b5bdb2a86c36b5898d3265462029002f720b2a1c8ea43566 --apply
```

安装器仅更新 `CODEX_HOME/pets/xiaojingyu-keleus`（未设置 `CODEX_HOME` 时使用用户的 `.codex/pets`），先在本项目的 `backups/install/` 创建可恢复备份。`backups/` 被 Git 忽略，不会进入待上传仓库。安装后通过桌面应用 **Settings → Pets → Refresh** 选用“小鲸鱼”；脚本不改全局选择或应用资源。

## 已知运行限制

当前核对的桌面版 `26.930.7945.0` 在悬浮层播放非待机动作三轮后切回待机；运行中敲键盘约 2.46 秒，不能由素材配置为持续循环。Ready 只对应完成且未读，观察方向帧还可能盖过运行帧。素材包改善了等待和完成的外观表达，**不保证所有任务状态持续一一对应**。详见 [状态说明](docs/runtime.md)。

## 来源与许可

原角色来自 [`keleus/deepseek-pet`](https://github.com/keleus/deepseek-pet) 的提交 `b9b61a35c3b2443ecdeab0ed442d6b33c603d343`，仓库声明 MIT，版权 `Copyright (c) 2026 keleus <jen.hs@outlook.com>`。许可全文见 [LICENSE](LICENSE)。本项目的清晰化基底包含此前经 AI 辅助补绘的衍生画面；精确来源与当前构建边界见 [来源说明](docs/source.md)。
