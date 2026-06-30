#!/usr/bin/env python3
"""计算 BMI、BMR (Mifflin-St Jeor)、TDEE、蛋白质与热量目标。

用法示例:
  python bmi_tdee.py --sex male --age 25 --height 175 --weight 70 \
      --activity moderate --goal fat_loss

说明:
- 这是估算，需结合 2-4 周体重/围度趋势调整。
- BMI 对肌肉量高的人会高估肥胖程度，仅作粗筛。
"""
import argparse

ACTIVITY_FACTORS = {
    "sedentary": 1.2,      # 久坐，几乎不运动
    "light": 1.375,        # 每周轻度运动 1-3 天
    "moderate": 1.55,      # 中等运动 3-5 天
    "active": 1.725,       # 高强度 6-7 天
    "very_active": 1.9,    # 体力工作 / 每天高强度
}

GOAL_ADJUST = {
    "maintain": (0, "维持"),
    "fat_loss": (-400, "减脂 (缺口约 400 kcal/日)"),
    "muscle_gain": (250, "增肌 (盈余约 250 kcal/日)"),
}


def bmi_category(bmi: float) -> str:
    # WHO 国际标准；亚洲人群超重/肥胖切点偏低 (23/27.5)，仅作参考
    if bmi < 18.5:
        return "偏瘦 underweight"
    if bmi < 25:
        return "正常 normal"
    if bmi < 30:
        return "超重 overweight"
    return "肥胖 obese"


def main() -> None:
    p = argparse.ArgumentParser(description="BMI / TDEE / 宏量目标计算")
    p.add_argument("--sex", required=True, choices=["male", "female"])
    p.add_argument("--age", required=True, type=float)
    p.add_argument("--height", required=True, type=float, help="身高 cm")
    p.add_argument("--weight", required=True, type=float, help="体重 kg")
    p.add_argument("--activity", default="moderate", choices=list(ACTIVITY_FACTORS))
    p.add_argument("--goal", default="maintain", choices=list(GOAL_ADJUST))
    p.add_argument("--protein-per-kg", type=float, default=None,
                   help="蛋白 g/kg/日；默认按目标自动取值")
    args = p.parse_args()

    h_m = args.height / 100.0
    bmi = args.weight / (h_m * h_m)

    # Mifflin-St Jeor BMR
    s = 5 if args.sex == "male" else -161
    bmr = 10 * args.weight + 6.25 * args.height - 5 * args.age + s
    tdee = bmr * ACTIVITY_FACTORS[args.activity]

    adjust, goal_label = GOAL_ADJUST[args.goal]
    target_kcal = tdee + adjust

    if args.protein_per_kg is not None:
        ppk = args.protein_per_kg
    else:
        ppk = {"maintain": 1.4, "fat_loss": 1.8, "muscle_gain": 1.8}[args.goal]
    protein_g = ppk * args.weight
    fat_g = (target_kcal * 0.275) / 9  # ~25-30% 热量来自脂肪
    carb_g = max(0.0, (target_kcal - protein_g * 4 - fat_g * 9) / 4)

    print("=" * 48)
    print(f"BMI        : {bmi:.1f}  ({bmi_category(bmi)})")
    print(f"BMR        : {bmr:.0f} kcal/日 (Mifflin-St Jeor)")
    print(f"TDEE       : {tdee:.0f} kcal/日 (活动系数 {ACTIVITY_FACTORS[args.activity]})")
    print(f"目标       : {goal_label}")
    print(f"目标热量   : {target_kcal:.0f} kcal/日")
    print("-" * 48)
    print(f"蛋白质     : {protein_g:.0f} g/日 ({ppk} g/kg)")
    print(f"脂肪       : {fat_g:.0f} g/日 (~27.5% 热量)")
    print(f"碳水       : {carb_g:.0f} g/日 (其余)")
    print("=" * 48)
    print("注: 估算值, 结合 2-4 周体重/围度趋势调整; BMI 对高肌肉量者会高估。")


if __name__ == "__main__":
    main()
