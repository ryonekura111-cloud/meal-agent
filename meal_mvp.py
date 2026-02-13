import random

DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# 主菜（最低7品以上）
MAINS = [
    {"dish": "鶏むね照り焼き", "type": "meat", "cost": 900, "protein": 55},
    {"dish": "豚こま生姜焼き", "type": "meat", "cost": 1000, "protein": 50},
    {"dish": "ハンバーグ", "type": "meat", "cost": 1200, "protein": 55},
    {"dish": "カレー", "type": "meat", "cost": 1300, "protein": 40},
    {"dish": "鮭の塩焼き", "type": "fish", "cost": 1100, "protein": 45},
    {"dish": "サバ味噌煮", "type": "fish", "cost": 950, "protein": 45},
    {"dish": "ブリ照り焼き", "type": "fish", "cost": 1200, "protein": 45},
    {"dish": "アジ南蛮", "type": "fish", "cost": 1000, "protein": 40},
]

SIDES = [
    "ほうれん草おひたし",
    "ひじき煮",
    "冷奴",
    "ポテトサラダ",
    "きんぴらごぼう",
    "コールスロー",
    "かぼちゃ煮"
]

BUDGET = 10000

# ==========================
# ① 制約付きメニュー生成
# ==========================
def menu_generate(budget=BUDGET):
    weekly_menu = []
    used_mains = set()
    last_type = None
    total_cost = 0

    for day in DAYS:
        candidates = [
            m for m in MAINS
            if m["dish"] not in used_mains
            and m["type"] != last_type
            and total_cost + m["cost"] <= budget
        ]

        if not candidates:
            return None  # 制約満たせず失敗

        main = random.choice(candidates)
        side = random.choice(SIDES)

        weekly_menu.append({
            "day": day,
            "main": main,
            "side": side
        })

        used_mains.add(main["dish"])
        last_type = main["type"]
        total_cost += main["cost"]

    return weekly_menu

# ==========================
# ② ルール確認
# ==========================
def rule_check(menu):
    total_cost = sum([m["main"]["cost"] for m in menu])
    return {
        "total_cost": total_cost,
        "budget_ok": total_cost <= BUDGET
    }

# ==========================
# ③ 買い物リスト集約
# ==========================
def shopping_list(menu):
    items = {}
    for m in menu:
        dish = m["main"]["dish"]
        items[dish] = items.get(dish, 0) + 1
    return items
def nutrition_score(menu):
    total_protein = sum([m["main"]["protein"] for m in menu])
    avg_protein = round(total_protein / 7, 1)

    protein_score = round(min((avg_protein / 60) * 100, 100), 1)

    return {
        "avg_protein": avg_protein,
        "protein_score": protein_score
    }

# ==========================
# ④ LINE用整形
# ==========================
def format_line_message(menu, shopping, rule_result, nutrition):

    msg = "【今週の献立】\n"

    for m in menu:
        msg += f"{m['day']}: {m['main']['dish']} + {m['side']}\n"

    msg += "\n【買い物リスト】\n"
    for k, v in shopping.items():
        msg += f"{k} × {v}\n"

    msg += f"\n概算予算: {rule_result['total_cost']}円\n"

    if not rule_result["budget_ok"]:
        msg += "※予算オーバー\n"

    return msg
    msg += "\n【栄養スコア】\n"
    msg += f"平均タンパク質/日: {nutrition['avg_protein']}g\n"
    msg += f"タンパク質スコア: {nutrition['protein_score']}点\n"

# ==========================
# 実行制御（最大50回再試行）
# ==========================
def run_meal_agent():
    for _ in range(50):
        menu = menu_generate()
        if menu:
            break
    else:
        return "制約を満たす献立が生成できませんでした。"

    rule_result = rule_check(menu)
    shopping = shopping_list(menu)
   nutrition = nutrition_score(menu)
message = format_line_message(menu, shopping, rule_result, nutrition)

    return message


if __name__ == "__main__":
    print(run_meal_agent())
