# api/upload.py
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from datetime import datetime
from db.conn import get_session
from db.models import Client, Image
from services.storage_local import save_image
from services.ai_service import predict

bp_upload = Blueprint("upload_api", __name__)

@bp_upload.route("/api/upload", methods=["POST"])
def api_upload():
    # รับค่า
    client_id = request.form.get("client_id") or request.headers.get("X-Client-Id")
    if not client_id:
        return jsonify({"error": "client_id is required"}), 400

    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "file is required"}), 400

    f = request.files["file"]

    # เซฟไฟล์
    disk_path, rel_path = save_image(f, current_app.config["UPLOAD_DIR"], client_id)
    url = f'{current_app.config["PUBLIC_BASE"]}/uploads/{rel_path}'

    # บันทึก DB
    s = get_session()
    try:
        # ensure client exists
        if not s.get(Client, client_id):
            s.add(Client(id=client_id))
        img = Image(client_id=client_id, url=url)
        s.add(img)
        s.commit()
        image_id = img.id
    finally:
        s.close()

    # (ตัวเลือก) ทำ AI ทันทีหลังอัปโหลด — ถ้ายังไม่ต้องใช้ ให้คอมเมนต์บรรทัดด้านล่างได้
    # label, conf = predict(disk_path, mapping={0:"Normal",1:"Header",2:"Spaghetti"})

    return jsonify({"image_id": image_id, "url": url, "created_at": datetime.utcnow().isoformat()+"Z"}), 201

# เสิร์ฟไฟล์ uploads แบบ basic
@bp_upload.route("/uploads/<path:rel_path>", methods=["GET"])
def serve_uploads(rel_path):
    return send_from_directory(current_app.config["UPLOAD_DIR"], rel_path)
