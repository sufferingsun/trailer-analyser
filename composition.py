import cv2
import numpy as np

THIRDS = (1/3, 2/3)
GOLDEN = (0.382, 0.618)

#Считает расстояние от точи до ближ прикола композиции
def _nearest_line_dist(x_norm: float, lines) -> float:
    return min(abs(x_norm - l) for l in lines)

#Смотрим насколько лица подходят под правило третей
def rule_of_thirds(frame, faces) -> float:
    if not faces:
        return None
    h, w = frame.shape[:2]
    devs = []
    for (x, y, fw, fh) in faces:
        cx, cy = (x + fw / 2) / w, (y + fh / 2) / h
        devs.append(min(_nearest_line_dist(cx, THIRDS),
                        _nearest_line_dist(cy, THIRDS)))
    return float(np.mean(devs))

#Смотрим насколько лица подходят под золотое сечение
def golden_ratio_deviation(frame, faces) -> float:
    if not faces:
        return None
    h, w = frame.shape[:2]
    devs = []
    for (x, y, fw, fh) in faces:
        cx, cy = (x + fw / 2) / w, (y + fh / 2) / h
        devs.append(min(_nearest_line_dist(cx, GOLDEN),
                        _nearest_line_dist(cy, GOLDEN)))
    return float(np.mean(devs))

#Ищем лица
def detect_faces(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8, minSize=(40, 40))
    #возврат списка кортежей позиция, ширина и высота
    return [tuple(f) for f in faces]


def analyse_shot_frames(video_path, start_sec, end_sec, sample_step=0.5):
    #sample_step чтоб не считывать каждый кадр
    cap = cv2.VideoCapture(video_path)
    #Каскад Хаара. Определает лица. Технически сейчас считается неэффективной технологией
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    results = {"thirds": [], "golden": []}
    frames_seen = 0
    t = start_sec
    while t < end_sec:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        if not ok:
            break
        frames_seen += 1
        faces = detect_faces(frame, cascade)
        r = rule_of_thirds(frame, faces)
        g = golden_ratio_deviation(frame, faces)
        if r is not None:
            results["thirds"].append(r)
            results["golden"].append(g)
        t += sample_step
    cap.release()

    #Возврат среднего
    def avg(xs):
        return float(np.mean(xs)) if xs else None

    return {
        "rule_of_thirds_dev": avg(results["thirds"]),
        "golden_ratio_dev": avg(results["golden"]),
        "frames_sampled": frames_seen,
    }