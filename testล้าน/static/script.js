// -------------------------------
// script.js
// -------------------------------

// ตัวแปรเดิม
const addBtn = document.getElementById("add-btn");
const uploadPopup = document.getElementById("upload-popup");

// -------------------------------
// เปิด popup + แสดง default Upload
addBtn.addEventListener("click", () => {
  setUploadContent();
  uploadPopup.classList.remove("hidden");
});

// -------------------------------
// ฟังก์ชันเปลี่ยน content เป็น Upload
function setUploadContent() {
  uploadPopup.innerHTML = `
    <h2>Upload Image</h2>
    <input id="file-input" type="file" name="file[]" multiple>
    <div style="margin-top:10px;">
      <button id="upload-btn" class="btn btn-primary">Upload</button>
      <button id="btn-switch-api" class="btn btn-secondary">Switch to API</button>
      <button onclick="closePopup('upload-popup')" class="btn btn-light">Close</button>
    </div>
  `;

  // -------------------------------
  // Bind Krajee Fileinput
  $("#file-input").fileinput({
    maxFileCount: '',
    allowedFileExtensions: ["jpg", "png", "gif", "jpeg"],
    showUpload: false,
    showRemove: true,
    browseLabel: "Select File",
    removeLabel: "Remove"
  });

  // Bind Upload button
  document.getElementById("upload-btn").addEventListener("click", async () => {
    const fileInput = document.getElementById("file-input");
    if (!fileInput.files.length) return alert("Please choose a file");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
      const res = await fetch("/upload", { method: "POST", body: formData });
      const data = await res.json();
      alert("Uploaded! Status: " + data.status);
      location.reload();
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Please try again.");
    }
  });

  // Bind switch to API
  document.getElementById("btn-switch-api").addEventListener("click", () => {
    setApiContent();
  });
}

// -------------------------------
// ฟังก์ชันเปลี่ยน content เป็น API
function setApiContent() {
  uploadPopup.innerHTML = `
    <h2>Real-time Camera (API)</h2>
    <p>TODO: connect Raspberry Pi camera stream every 2s</p>
    <div style="margin-top:10px;">
      <button id="btn-switch-upload" class="btn btn-secondary">Switch to Upload</button>
      <button onclick="closePopup('upload-popup')" class="btn btn-light">Close</button>
    </div>
  `;

  // Bind switch กลับไป Upload
  document.getElementById("btn-switch-upload").addEventListener("click", () => {
    setUploadContent();
  });
}

// -------------------------------
// ปิด popup (เหมือนเดิม)
function closePopup(id) {
  document.getElementById(id).classList.add("hidden");
}
