from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid
import torch
from ultralytics import YOLO
from datetime import datetime

# โหลดโมเดล YOLO (CPU only)
MODEL_PATH = "models/best.pt"
model = YOLO(MODEL_PATH)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# DB จำลอง (ใช้ list แทน database จริง)
detections_db = []


@app.route("/")
def index():
    return render_template("index.html", detections=detections_db)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No filename"}), 400

    # สร้างชื่อไฟล์ไม่ให้ซ้ำ
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # รัน model detect (CPU)
    results = model(filepath)
    labels = results[0].boxes.cls.tolist()
    scores = results[0].boxes.conf.tolist()
    print("Labels:", labels)
    print("Scores:", scores)
    print("Names:", [model.names[int(l)] for l in labels])

    # สมมุติ mapping class
    mapping = {0: "Normal", 1: "Header", 2: "Spaghetti"}
    detected_classes = [mapping.get(int(l), "Unknown") for l in labels]

    # เก็บผลลัพธ์ลง "DB"
    record = {
        "id": len(detections_db) + 1,
        "filename": filename,
        "status": detected_classes[0] if detected_classes else "Unknown",
        "confidence": round(scores[0], 2) if scores else 0,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    detections_db.append(record)

    return jsonify(record)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
