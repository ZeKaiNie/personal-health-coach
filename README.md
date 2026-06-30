# 🩺 Personal Health Coach — 私人健康管家 Agent Skill

> 一个开源的 [Anthropic Agent Skill](https://claude.com/docs/skills/how-to)，把零散的身体数据、生活习惯和症状，转化为「**根因 → 底层逻辑 → 可执行方案**」的循证健康分析。给学生、年轻人、老年人——任何想认真管理自己健康/状态/外貌的人——一个**基于真实研究、且记得你是谁**的私人健康教练。
>
> An open-source agent skill that turns your body data, habits, and symptoms into an evidence-based analysis: **root cause → underlying mechanism → actionable plan** for diet, sleep, supplements (with dosage/timing/cautions), skincare, and exercise.

> ⚠️ **不是医疗诊断 / Not medical advice.** 见 [DISCLAIMER.md](DISCLAIMER.md)。涉及疾病、用药、孕期或严重症状请就医。

---

## 它解决什么问题 / Why

人们在网上找健康建议时常遇到：来源不权威、内容过时、千篇一律不适合自己、且没人「记得」你的情况。这个 skill 针对性地：

- 📁 **有记忆**：把你的身高/体重/性别/年龄/补剂/血检/习惯存进一个本地档案，每次基于事实推理，**不失忆、不编数据**。
- 🧠 **讲底层逻辑**：不只给「吃这个」，而是解释「为什么」——让你能自己灵活搭配安排。
- 🔬 **循证 + 标注强度**：每条结论标 `[A/B/C/D]` 证据强度，拿不准就去查最新研究，**不夸大、不贩卖焦虑**。
- 💊 **可执行**：补剂给到剂量/时间/注意/相互作用；饮食/作息/运动给到可量化的模板与复盘指标。
- 🛡️ **有安全边界**：命中红线（疾病/孕期/未成年/多重用药/红旗症状）会建议就医而非替代处方。

## 适用人群 / Who it's for

- **学生 / 青少年**：专注力、记忆、熬夜、刷短视频、痘、外貌焦虑、考试压力。
- **年轻成人**：健身增肌减脂、皮肤抗老、精力、代谢、压力。
- **中老年**：养生长寿、肌少症、骨骼、认知、慢病生活方式辅助（务必配合主治医生）。

---

## 这个 skill 能回答什么（举例）

> 「我长期熬夜刷短视频、爱吃甜食喝牛奶、食堂吃饭油多，最近注意力/记忆力下降、皮肤暗沉爆痘——我最可能是什么问题？怎么造成的？大脑和皮肤怎么修？底层逻辑是什么？饮食作息怎么调？补剂吃啥、多少、什么时候吃、注意什么？」

它会：定位最可能的根因 → 用因果链讲透机制 → 给分模块方案（饮食/作息/大脑/皮肤/补剂/运动）→ 压成「先做这 3 件事」+ 复盘指标，并把更新写回你的记忆档案。
完整示例见 [`examples/example-report.md`](examples/example-report.md)。

---

## 目录结构 / Structure

```
personal-health-coach/
├── README.md
├── LICENSE                      # MIT
├── DISCLAIMER.md                # 医疗免责
├── CONTRIBUTING.md              # 贡献指南（含证据/引用规范）
├── .gitignore                   # 关键：排除个人健康档案，防止误提交隐私
├── examples/
│   └── example-report.md        # 一份完整的示例分析报告
└── skills/
    └── holistic-health-coach/
        ├── SKILL.md             # 主流程编排 + 工作流 + 证据分级 + 安全
        ├── assets/
        │   ├── profile-template.md  # 记忆档案模板（你的数据存这里）
        │   └── plan-template.md     # 输出方案模板
        ├── references/          # 按需加载的知识分册
        │   ├── intake-protocol.md
        │   ├── root-cause-framework.md
        │   ├── brain-repair.md
        │   ├── skin-repair.md
        │   ├── nutrition.md
        │   ├── sleep-circadian.md
        │   ├── exercise.md
        │   ├── population-considerations.md
        │   ├── supplements.md
        │   └── evidence-and-safety.md
        └── scripts/
            └── bmi_tdee.py      # 计算 BMI / TDEE / 蛋白宏量目标
```

---

## 安装与使用 / Install & Use

### 在 Claude / 支持 Agent Skills 的客户端中

1. 把 `skills/holistic-health-coach/` 整个目录放到你的 skills 目录（例如 Claude Code 的 `~/.claude/skills/` 或项目内 `.claude/skills/`）。
2. 目录名必须与 `SKILL.md` 中的 `name`（`holistic-health-coach`）一致。
3. 直接对它说你的情况即可，例如：「我 22 岁男，身高 175 体重 70……最近注意力下降、爆痘，帮我分析」。它会引导你建立记忆档案并给出方案。

> 详见 Anthropic 官方文档：<https://claude.com/docs/skills/how-to>

### 你的「记忆档案」

- 首次使用时，skill 会用 `assets/profile-template.md` 帮你生成一份 `health-profile.md`。
- **这个文件包含你的隐私健康数据**，已被 `.gitignore` 排除——**不要提交到任何公开仓库**。
- 跨会话它都会先读这个档案，所以越用越准。

### 单独用 BMI/TDEE 脚本

```bash
python skills/holistic-health-coach/scripts/bmi_tdee.py \
    --sex male --age 25 --height 175 --weight 70 \
    --activity moderate --goal fat_loss
```

---

## 证据分级 / Evidence grading

| 等级 | 含义 |
|------|------|
| **[A]** | 多项 RCT / meta 分析 / 权威指南一致支持 |
| **[B]** | 有 RCT 或一致观察性证据，但有局限 |
| **[C]** | 机制合理 + 小样本/动物/观察性，个体差异大 |
| **[D]** | 主要靠机制推演，证据稀少 |

权威来源优先级、安全红线见 [`skills/holistic-health-coach/references/evidence-and-safety.md`](skills/holistic-health-coach/references/evidence-and-safety.md)。

---

## 贡献 / Contributing

欢迎补充/纠正基于最新研究的内容、新增人群或专题分册、翻译成英文等。请先读 [CONTRIBUTING.md](CONTRIBUTING.md)，**所有健康主张都需附可核查的权威来源并标注证据强度**。

## 许可 / License

[MIT](LICENSE)。健康内容仅供教育参考，使用风险自负，详见 [DISCLAIMER.md](DISCLAIMER.md)。
