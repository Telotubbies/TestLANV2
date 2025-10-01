# api/ai_test.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from db.conn import get_session
from db.models import Image, AITest

bp_ai = Blueprint("ai_api", __name__)

@bp_ai.route("/api/ai_test", methods=["POST"])
def api_ai_test():
    data = request.get_json(silent=True) or {}
    image_id = data.get("image_id")
    label = data.get("label")
    confidence = data.get("confidence")

    if not image_id:
        return jsonify({"error": "image_id is required"}), 400

    s = get_session()
    try:
        img = s.get(Image, int(image_id))
        if not img:
            return jsonify({"error": "image_id not found"}), 404

        test = AITest(image_id=int(image_id), label=label, confidence=confidence)
        s.add(test)
        s.commit()
        return jsonify({
            "ai_test_id": test.id,
            "created_at": datetime.utcnow().isoformat()+"Z"
        }), 201
    finally:
        s.close()
