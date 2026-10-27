import numpy as np


def rhythm_stats(shots):
    #Чек ритма монтажа по шотам
    durs = np.array([e - s for s, e in shots], dtype=np.float32)
    if durs.size == 0:
        return {}
    total = float(durs.sum())
    return {
        #Средняя длина шотов
        "mean_shot_dur": float(durs.mean()),
        #Стандартное отклонение от ритма. Ровный, не ровный монтаж
        "std_shot_dur": float(durs.std()),
        "min_shot_dur": float(durs.min()),
        "max_shot_dur": float(durs.max()),
        #Сколько склеек в минуту при текущем монтаже
        "cuts_per_min": len(shots) / (total / 60.0) if total else 0.0,
        #Сверх короткие кадры
        "fast_cuts_ratio": float((durs < 1.0).mean()),
    }