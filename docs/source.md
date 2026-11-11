# 来源与构建边界

- 上游仓库：<https://github.com/keleus/deepseek-pet>
- 固定参考提交：`b9b61a35c3b2443ecdeab0ed442d6b33c603d343`（包版本 0.2.1）。
- 上游声明 MIT，原版权 `Copyright (c) 2026 keleus <jen.hs@outlook.com>`。许可原文保留于项目根目录 `LICENSE`，安装包也包含 `pet/LICENSE.txt`。
- 角色是蓝发女仆与鲸鱼尾巴的拟人形象。此前构建使用上游原画，并进行 AI 辅助补绘、抠图与清晰化；最终经用户审查的基底冻结为 `assets/clarity-base.png`。本仓库不声称能从上游原画自动重现全部补绘历史。
- `scripts/build_release.py` 能从**冻结基底**和 `assets/*-overlays.png` 离线、确定性地重建当前发布精灵图：第 6 行添加问号气泡，第 8 行复用同一画风的挥手姿态并添加完成勾号。其余格保持基底原像素。状态图层已固化为 PNG，因此重建不依赖本机字体。重建结果与 `pet/spritesheet.png` 的 SHA-256 完全一致。
- 待上传 Git 仓库只包含当前发布版与重建所需文件；历史生成响应、临时图、失败候选和上游克隆被 `.gitignore` 排除。需要核对原始上游文件时，使用上述固定提交获取。
