# api/history.py
from flask import Blueprint, request, jsonify
from sqlalchemy import select, desc
from db.conn import get_session
from db.models import Image, AITest

bp_history = Blueprint("history_api", __name__)

@bp_history.route("/api/history/<client_id>", methods=["GET"])
def api_history(client_id):
    limit = min(int(request.args.get("limit", 50)), 200)
    with_tests = request.args.get("with_tests") == "1"

    s = get_session()
    try:
        q = select(Image).where(Image.client_id == client_id).order_by(desc(Image.created_at)).limit(limit)
        images = s.execute(q).scalars().all()

        items = []
        for img in images:
            row = {
                "image_id": img.id,
                "url": img.url,
                "created_at": img.created_at.isoformat() if img.created_at else None
            }
            if with_tests:
                tq = select(AITest).where(AITest.image_id == img.id).order_by(desc(AITest.created_at))
                tests = s.execute(tq).scalars().all()
                row["ai_tests"] = [{
                    "ai_test_id": t.id,
                    "label": t.label,
                    "confidence": t.confidence,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                } for t in tests]
            items.append(row)

        return jsonify({"client_id": client_id, "items": items})
    finally:
        s.close()
