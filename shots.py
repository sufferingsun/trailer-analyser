from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector


def detect_shots(video_path: str, threshold: float = 27.0):
    video = open_video(video_path)
    manager = SceneManager()
    #Производство склеек. Шайтам штука делает магию. threshold - определяет чувствительность склеек
    manager.add_detector(ContentDetector(threshold=threshold))
    manager.detect_scenes(video, show_progress=False)

    shots = []
    for start, end in manager.get_scene_list():
        shots.append((start.get_seconds(), end.get_seconds()))
    #Возвращаем массив начала и конца шотов
    return shots