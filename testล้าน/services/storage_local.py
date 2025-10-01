# services/storage_local.py
import os, uuid
from werkzeug.utils import secure_filename

ALLOWED = {"jpg","jpeg","png","webp"}

def save_image(file, base_dir: str, client_id: str) -> tuple[str, str]:
    # return (disk_path, rel_path)
    ext = (file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg").lower()
    if ext not in ALLOWED:
        raise ValueError("file type not allowed")

    cid = secure_filename(client_id) or "anon"
    subdir = os.path.join(base_dir, cid)
    os.makedirs(subdir, exist_ok=True)

    fname = f"{uuid.uuid4().hex}.{ext}"
    disk_path = os.path.join(subdir, fname)
    file.save(disk_path)
    rel_path = f"{cid}/{fname}"
    return disk_path, rel_path
