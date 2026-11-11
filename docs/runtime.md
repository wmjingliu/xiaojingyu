# 桌面状态与已知限制

状态含义及多聊天优先级以[官方 Pets 文档](https://learn.chatgpt.com/docs/pets)为准：Needs input → Blocked → Ready → Running。Ready 指完成且存在未读活动。

本机 `26.930.7945.0` 的只读实现检查得到下表；这是版本观察，不是公开 API 保证。

| 行 | 动画 | 用途 | 当前素材 |
|---:|---|---|---|
| 0 | idle | 待机 | 站立轻动 |
| 1–2 | running-right/left | 左右拖动 | 迈步 |
| 3 | waving | 首次招呼 | 挥手 |
| 4 | jumping | 悬停 | 跳跃 |
| 5 | failed | Blocked | 委屈 |
| 6 | waiting | Needs input | 疑惑并带问号 |
| 7 | running | Running | 伏案敲键盘 |
| 8 | review | Ready | 轻挥手并带勾号 |
| 9–10 | look | 16 向观察 | 眼神与朝向 |

悬浮层调用渲染器时没有启用循环。非待机动作播三轮后回到待机：Running 约 2.46 秒、Needs input 约 3.03 秒、Ready 约 3.09 秒、Blocked 约 3.66 秒。观察方向帧可能覆盖 Running、idle 或 waving 的普通帧。应用已经读到结果时，Ready 可能很快消失；每次结果到达也不一定触发 Ready。减少动态效果开启时，静帧属于预期行为。

`pet.json` 只声明名称、版本和精灵图路径，没有循环或结果事件参数。持续敲键盘及每次完成都出现完成动作，需要应用提供播放逻辑或设置支持；不应修改 `app.asar`、内置资源或全局状态来伪装素材修复。应用更新后可运行 `scripts/audit_runtime.py` 核对；未知代码模式应人工审查，不能自动宣布状态正确。
