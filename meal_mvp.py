import random

# ==========================
# ① メニュー生成エージェント
# ==========================

MAINS = [
    {"dish": "鶏むね照り焼き", "type": "meat", "cost": 900},
    {"dish": "豚こま生姜焼き", "type": "meat", "cost": 1000},
    {"dish": "鮭の塩焼き", "type": "fish", "cost": 1100},
    {"dish": "サバ味噌煮", "type": "fish", "cost": 950},
    {"dish": "ハンバーグ", "type": "meat", "cost": 1200},
    {"dish": "カレー", "type": "meat", "cost": 1300},
]

SIDES = [
    "ほうれん草おひたし",
    "ひじき煮",
    "冷奴",
    "ポテトサラダ",
    "きんぴらごぼう",
]

def menu_generate():
    weekly_menu = []
    last_type = None
    
    for day in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
        candidates = [m for m in MAINS if m["type"] != last_type]
        main = random.choice(candidates)
        side = random.choice(SIDES)
        
        weekly_menu.append({
            "day": day,
            "main": main,
            "side": side
        })
        
        last_type = main["type"]
    
    return weekly_menu

# ==========================
# ② ルール判定エージェント
# ==========================

def rule_check(menu, budget=10000):
    total_cost = sum([m["main"]["cost"] for m in menu])
    budget_ok = total_cost <= budget
    
    return {
        "total_cost": total_cost,
        "budget_ok": budget_ok
    }

# ==========================
# ③ 買い物リストエージェント
# ==========================

def shopping_list(menu):
    items = {}
    for m in menu:
        dish = m["main"]["dish"]
        items[dish] = items.get(dish, 0) + 1
    return items

# ==========================
# ④ 通知整形エージェント
# ==========================

def format_line_message(menu, shopping, rule_result):
    msg = "【今週の献立】\n"
    
    for m in menu:
        msg += f"{m['day']}: {m['main']['dish']} + {m['side']}\n"
    
    msg += "\n【買い物リスト】\n"
    for k,v in shopping.items():
        msg += f"{k} × {v}\n"
    
    msg += f"\n概算予算: {rule_result['total_cost']}円\n"
    
    if not rule_result["budget_ok"]:
        msg += "※予算オーバー\n"
    
    return msg

# ==========================
# 実行
# ==========================

def run_meal_agent():
    menu = menu_generate()
    rule_result = rule_check(menu)
    shopping = shopping_list(menu)
    message = format_line_message(menu, shopping, rule_result)
    return message


if __name__ == "__main__":
    print(run_meal_agent())
