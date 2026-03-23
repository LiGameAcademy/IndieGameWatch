import pandas as pd


def basic_playtime_stats(df: pd.DataFrame, threshold: float = 20.0) -> None:
    playtime = df["游玩时长(小时)"]
    playtime_clean = playtime[(playtime >= 0) & (playtime <= 2000)]

    total = len(df)
    mean_hours = playtime_clean.mean()
    median_hours = playtime_clean.median()
    over_threshold = (playtime_clean >= threshold).sum()

    print("===== 游玩时长统计 =====")
    print(f"总评论数: {total}")
    print(f"平均游玩时长: {mean_hours:.1f} 小时")
    print(f"中位数游玩时长: {median_hours:.1f} 小时")
    print(
        f">= {threshold:.0f} 小时的玩家数: {over_threshold} "
        f"（占 {over_threshold / total:.2%}）"
    )
    print()


def contains_any(text: str, patterns) -> bool:
    lower = text.lower()
    return any(p.lower() in lower for p in patterns)


def keyword_stats(df: pd.DataFrame) -> None:
    texts = df["玩家评价"].fillna("").astype(str)
    total = len(texts)

    keyword_groups = {
        "画质相关": ["画质", "画面"],
        "UI相关": ["UI", "ui", "界面"],
        "Godot引擎": ["Godot", "godot"],
        "创新/缺乏创新": ["缺乏创新", "不够创新", "没创新", "没有创新", "创新不足"],
    }

    print("===== 关键词覆盖率（按评论条数统计） =====")
    for label, patterns in keyword_groups.items():
        mask = texts.apply(lambda x: contains_any(x, patterns))
        count = mask.sum()
        ratio = count / total if total > 0 else 0.0
        print(f"{label}: {count} 条，占 {ratio:.2%}")
    print()


if __name__ == "__main__":
    csv_path = "slay_the_spire_2_reviews.csv"
    df_reviews = pd.read_csv(csv_path)

    basic_playtime_stats(df_reviews, threshold=20.0)
    keyword_stats(df_reviews)

