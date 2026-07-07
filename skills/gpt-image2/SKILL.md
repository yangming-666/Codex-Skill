---
name: gpt-image2
description: Use when 需要生成任何类型的图片，包括插画、照片风图片、海报、社交媒体配图、分镜图、营销素材，或用户明确要求使用 gpt-image-2 / gen_gpt_image2.py / gpt-image。
---

# 通过 TokenX24 使用 GPT Image 2

## 概述

通过 subagent 调用技能内置的 `scripts/gen_gpt_image2.py` 生成图片素材。该脚本调用 TokenX24 的 OpenAI-compatible 图片接口，默认模型为 `gpt-image-2`。

当用户需要生成 PNG 图片，并且明确要求走 TokenX24 / `gpt-image-2` 路径，而不是 Codex 内置图片生成工具时，使用本技能。

## 使用前提

- shell 环境中必须能读取到 `TOKENX24_API_KEY`。
- 脚本只依赖 Python 标准库，不需要额外安装 SDK。
- OpenClaw 只能通过聊天软件与用户交互。缺少 key 时，明确询问用户提供 TokenX24 API key，然后由 agent 调用配置脚本写入本机环境配置。

检查配置：

```bash
source ~/.zshrc >/dev/null 2>&1
test -n "$TOKENX24_API_KEY" && echo TOKENX24_API_KEY_PRESENT || echo TOKENX24_API_KEY_MISSING
```

## 缺少 API key 时配置

如果检查结果是 `TOKENX24_API_KEY_MISSING`，先向用户说明需要 TokenX24 API key，并请用户直接在当前聊天中提供。拿到 key 后，由 agent 显式传入配置脚本写入本机环境配置。不要让用户打开终端输入，也不要要求用户自己编辑 shell 配置文件。

该脚本会根据当前系统和 shell 选择配置文件：

- macOS + zsh：`~/.zshrc`
- macOS + bash：`~/.bash_profile`
- Linux + zsh：`~/.zshrc`
- Linux + bash：`~/.bashrc`
- 其他 POSIX shell：`~/.profile`

查看将要写入的配置文件：

```bash
python3 skills/gpt-image2/scripts/configure_tokenx24_api_key.py --print-target
```

用户在聊天中提供 key 后，由 agent 调用脚本写入配置文件：

```bash
python3 skills/gpt-image2/scripts/configure_tokenx24_api_key.py --api-key "<USER_PROVIDED_TOKENX24_API_KEY>"
```

如果需要避免 key 出现在命令参数中，也可以由 agent 通过 stdin 传入脚本：

```bash
printf '%s' "<USER_PROVIDED_TOKENX24_API_KEY>" | python3 skills/gpt-image2/scripts/configure_tokenx24_api_key.py --stdin
```

脚本要求必须显式提供 `--api-key` 或 `--stdin`，不会等待终端交互输入。脚本会用受控标记块幂等写入 `TOKENX24_API_KEY`，重复执行会替换旧值，不会无限追加。写入后重新加载对应配置文件或打开新终端，再检查：

```bash
PROFILE="$(python3 skills/gpt-image2/scripts/configure_tokenx24_api_key.py --print-target)"
source "$PROFILE" >/dev/null 2>&1
test -n "$TOKENX24_API_KEY" && echo TOKENX24_API_KEY_PRESENT || echo TOKENX24_API_KEY_MISSING
```

key 属于敏感信息。配置成功后，不要在普通回复中复述 key，也不要把包含 key 的命令输出给用户。

## 硬性门禁（主 session 禁止直接生成）

本技能**只允许**通过 subagent 执行图片生成。主 session 负责编排，不得直接调用 `gen_gpt_image2.py`。

### 规则

1. **主 session 禁止 exec 生成。** `python3 skills/gpt-image2/scripts/gen_gpt_image2.py ...` 形式的命令**只能出现在 subagent 内部**，不得出现在主 session 的 `exec` 调用中。
2. **一 agent 一图。** 每个 subagent 只允许生成 1 张图片。需要 N 张图时，创建 N 个 subagent，各自独立生成 1 张。
3. **主 session 只编排。** 主 session 职责：整理 prompt → `sessions_spawn` 派发 subagent → 等通知收图 → 校验发图。不得在同一个 subagent 里塞入多张图片的生成任务。
4. **完成条件必须闭环。** subagent 必须独立完成 key 检查、单图生成、文件存在/非空校验和预览确认；缺少任一步，主 session 不得视为图片已完成。

### 推荐 spawn 参数

```json
{
  "runtime": "subagent",
  "mode": "run",
  "label": "image-gen-xxx",
  "task": "按 gpt-image2 技能生成一张图片。本 subagent 只允许生成 1 张，只产出 1 个最终 PNG 文件。提示词：...，尺寸：...，输出路径：..."
}
```

`context` 不需要 fork（每个 subagent 独立加载 gpt-image2 技能即可）。

## 生成前提示词质量预检（主 session）

主 session 在派发 subagent 之前，先判断用户给出的提示词是否过于简单。若提示词过于简单，不要直接派发；先询问用户是否需要使用 `skills/brainstorming/SKILL.md` 帮助补齐高质量图片生成所需信息。

### 过于简单的判断

满足以下任一情况，视为提示词过于简单：

- 只有主体或画风，例如“画一只杯子”“赛博朋克城市”“做张海报”。
- 缺少目标用途、受众、画幅、场景、主体细节、文字内容、风格约束中的大部分信息。
- 用户只给出抽象情绪或关键词，例如“高级感”“温暖”“科技感”“小红书风”。
- 要求生成营销图、社交媒体图、分镜图或海报，但没有说明核心文案、产品/服务、视觉主体或版式方向。
- 批量生成系列图时，没有说明系列一致性要求，例如角色、场景、服装、色彩或构图延续。

不需要拦截的情况：

- 用户已经给出明确、可执行的完整提示词。
- 用户明确表示先快速出图、草稿、随便试一版或不需要优化。
- 上下文中已有足够信息，可以安全整合成完整提示词。

### 询问方式

提示词过于简单时，用简短问题确认：

```text
当前提示词比较简单，按现有信息生成可能会影响图片稳定性和成片质量。是否先使用 `skills/brainstorming/SKILL.md` 帮你补齐用途、主体、场景、画幅、风格和文字约束后再生成？
```

- 如果用户同意，先使用 `skills/brainstorming/SKILL.md` 整理图片生成 brief，再根据 brief 编写最终提示词并派发 subagent。
- 如果用户拒绝或要求立即出图，仍必须派发 subagent；只是按简略提示词生成，并提醒结果可能需要重试或补充修正。
- 如果只缺少一个关键字段，可以直接只问那个字段，不必进入完整 brainstorming。

## 脚本位置

使用技能目录内的脚本。

配置 TokenX24 API key：

```bash
python3 skills/gpt-image2/scripts/configure_tokenx24_api_key.py --help
```

重要默认值：

- `--base-url https://tokenx24.com/v1`
- `--model gpt-image-2`
- `--api-key "$TOKENX24_API_KEY"`
- 当服务商返回 PNG 兼容数据时，输出文件为 PNG。

## 生成单张图片（subagent 模式）

主 session 整理好 prompt 后，通过 `sessions_spawn` 创建一个 subagent，在 task 中明确指定提示词、尺寸和输出路径。

subagent task 示例：

```
按 gpt-image2 技能生成一张图片。本 subagent 只允许生成 1 张，只产出 1 个最终 PNG 文件，不得批量生成、不得追加备选图。提示词："一张小红书竖版营销插画，中文标题清晰可读，现代中国办公室场景"，尺寸：1200x1600，输出路径：output/imagegen/example.png。生成后确认文件存在且非空，并用 read 工具预览确认。
```

subagent 内部使用 `gen_gpt_image2.py` 执行生成，`timeout` 不得低于 300 秒。主 session 不关心 subagent 内部如何生成，只等待完成通知。

## 生成多张图片（多个 subagent 并行）

需要 N 张图片时，主 session 创建 N 个 subagent，每个负责 1 张。全部并行 `sessions_spawn`，互不阻塞。

不得将多个 prompt 打包发给同一个 subagent。不得在 subagent task 中写入"生成 N 张图"。

示例（2 张图）：

subagent A task：
```
按 gpt-image2 技能生成一张图片。本 subagent 只允许生成 1 张，只产出 1 个最终 PNG 文件，不得批量生成、不得追加备选图。提示词："[prompt A]"，尺寸：1200x1600，输出路径：output/imagegen/image-a.png。生成后确认文件存在且非空，并用 read 预览确认。
```

subagent B task：
```
按 gpt-image2 技能生成一张图片。本 subagent 只允许生成 1 张，只产出 1 个最终 PNG 文件，不得批量生成、不得追加备选图。提示词："[prompt B]"，尺寸：1200x1600，输出路径：output/imagegen/image-b.png。生成后确认文件存在且非空，并用 read 预览确认。
```

subagent 内部每条 `exec` 生成命令 `timeout` 不得低于 300 秒；大图或 `--retries` > 1 时优先 600 秒。

## 提示词建议

生成社交媒体营销图时：

- 说明素材类型、目标平台和画幅比例。
- 需要出现在图里的中文文案用引号标出。
- 图中文字尽量短；密集小字通常需要后期人工修正。
- 系列图要强调视觉连续性：同一角色、同一服装、同一办公室、同一画风。
- 加入反向约束：无水印、除非必要不要英文、不要乱码中文。

可复用的默认提示词尾巴：

```text
clean commercial flat vector illustration, warm pastel colors, Chinese office environment,
Chinese people with East Asian features, all visible text in Chinese, readable UI text,
3:4 portrait, suitable for Xiaohongshu, no watermark
```

## 生成后校验（主 session）

每个 subagent 完成通知到达后，主 session：

1. 确认输出文件存在且非空。
2. 用 `read` 工具预览图片。
3. 检查关键中文标题和文案是否正确。
4. 如果小字不稳定，明确告诉用户需要后期修字或局部重绘。
5. 按当前渠道规则发送给用户（飞书用 IM API 直发，其他渠道用 `MEDIA:`）。

如果校验失败或用户要求重试，主 session 仍必须重新 `sessions_spawn` 一个新 subagent；原 subagent 不得继续生成第二张。

常用命令：

```bash
ls -lh output/imagegen/
```

## 常见问题

- `Missing API key`：先运行 `configure_tokenx24_api_key.py`，再加载脚本输出的目标配置文件或打开新终端。
- `401` 或鉴权错误：TokenX24 key 无效、过期，或没有目标模型权限。
- 空响应或响应格式不支持：服务商没有返回 `b64_json` 或 `url`；可重试一次，再报告原始错误。
- 中文文字不完美：缩短图中文字重新生成，或安排人工修字/局部重绘。
