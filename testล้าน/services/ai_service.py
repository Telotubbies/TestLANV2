# services/ai_service.py
from ultralytics import YOLO

# โหลด 1 ครั้งตอนสตาร์ต
_model = None

def load_model(path: str):
    global _model
    if _model is None:
        _model = YOLO(path)
    return _model

def predict(filepath: str, mapping: dict[int, str] | None = None):
    """
    คืนค่า: (label, confidence)
    ถ้าไม่มีผล → ("Unknown", 0.0)
    """
    if _model is None:
        raise RuntimeError("Model is not loaded. Call load_model() first.")

    results = _model(filepath)
    labels = results[0].boxes.cls.tolist() if results and results[0].boxes is not None else []
    scores = results[0].boxes.conf.tolist() if results and results[0].boxes is not None else []

    if not labels or not scores:
        return "Unknown", 0.0

    idx = int(labels[0])
    conf = float(scores[0])
    if mapping:
        return mapping.get(idx, "Unknown"), conf
    return str(idx), conf
