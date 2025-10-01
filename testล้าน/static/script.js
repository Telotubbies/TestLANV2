document.getElementById("add-btn").addEventListener("click", () => {
  // popup 2 ตัวเลือก
  let choice = confirm("OK = Upload Image, Cancel = API Camera");
  if (choice) {
    document.getElementById("upload-popup").classList.remove("hidden");
  } else {
    document.getElementById("api-popup").classList.remove("hidden");
  }
});

document.getElementById("upload-btn").addEventListener("click", async () => {
  const fileInput = document.getElementById("file-input");
  if (!fileInput.files.length) return alert("Please choose a file");

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("/upload", { method: "POST", body: formData });
  const data = await res.json();

  alert("Uploaded! Status: " + data.status);
  location.reload();
});

function closePopup(id) {
  document.getElementById(id).classList.add("hidden");
}
