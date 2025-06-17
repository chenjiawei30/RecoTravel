# -*- coding: utf-8 -*-
"""
季节（时令）景点推荐
@author: 2025-06
"""
import datetime
from typing import Dict, List, Tuple

from .load_spot import load_sp          # 复用原有的景点数据加载函数

# == 1. 定义各季节适宜景点 ========================================
# 这里只给出示例子集，后续可继续补充；务必使用与
# “北京景点名称.txt”中完全一致的中文名称
SEASON_SPOTS: Dict[str, List[str]] = {
    "spring": [
        "玉渊潭公园", "北京植物园", "香山公园", "景山公园", "世界花卉大观园"
    ],
    "summer": [
        "颐和园", "十渡风景区", "青龙峡", "怀柔雁栖湖", "北京欢乐谷"
    ],
    "autumn": [
        "八达岭古长城（残长城）", "妙峰山", "香山公园",
        "奥林匹克森林公园", "蟒山国家森林公园"
    ],
    "winter": [
        "什刹海", "故宫博物院", "南锣鼓巷", "恭王府", "前门大街"
    ],
}


# == 2. 判断当前季节 =============================================
def _today_season(today: datetime.date | None = None) -> str:
    """返回字符串 {spring|summer|autumn|winter}"""
    d = today or datetime.date.today()
    m = d.month
    if 3 <= m <= 5:
        return "spring"
    if 6 <= m <= 8:
        return "summer"
    if 9 <= m <= 11:
        return "autumn"
    return "winter"


# == 3. 推荐接口 ==================================================
def seasonal_recommend(k: int = 5) -> Tuple[str, list, list, list]:
    """
    根据当前日期返回最多 k 个时令景点
    :return: (season, 景点名列表, 地址列表, 经纬度列表)
    """
    season = _today_season()
    cand = SEASON_SPOTS.get(season, [])

    # 加载项目原始全部景点信息
    names, addrs, scores, latlons = load_sp()

    # —— 过滤出季节候选 + 按景点评分降序 ——
    idx = [
        i for i, n in enumerate(names) if n in cand
    ]
    # 若季节候选不足 k，则用其余高分景点补齐
    if len(idx) < k:
        extras = [
            i for i in range(len(names)) if names[i] not in cand
        ]
        # 依据评分排序
        extras.sort(key=lambda i: float(scores[i]), reverse=True)
        idx.extend(extras[: (k - len(idx))])

    # 最终再次按评分排序并截断
    idx.sort(key=lambda i: float(scores[i]), reverse=True)
    idx = idx[:k]

    return (
        season,
        [names[i] for i in idx],
        [addrs[i] for i in idx],
        [latlons[i] for i in idx],
    )
