import json
from shots import detect_shots
from composition import analyse_shot_frames
from rhythm import rhythm_stats

#Связка всех приколов
def analyse_trailer(video_path):
    shots = detect_shots(video_path)
    shot_reports = []
    for i, (s, e) in enumerate(shots):
        #Для каждого шота вызывается анализ
        comp = analyse_shot_frames(video_path, s, e)
        shot_reports.append({
            "shot_id": i,
            "start": round(s, 3),
            "end": round(e, 3),
            "duration": round(e - s, 3),
            #Распаковка внутри словаря
            **comp,
        })

    rhythm = rhythm_stats(shots)

    return {
        "video": video_path,
        "shots_count": len(shots),
        "shots": shot_reports,
        "rhythm": rhythm,
    }


if __name__ == "__main__":
    import sys
    result = analyse_trailer(sys.argv[1])
    with open("trailer_report.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Отчёт сохранён: trailer_report.json")