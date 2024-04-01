const dropContainer = document.getElementById("dropcontainer");
const fileInput = document.getElementsByClassName("drop-container-input")[0];
const fileUploadDiv = document.getElementsByClassName("drop-container-load")[0];
const fileUploadDivFill = document.getElementsByClassName(
  "drop-container-load-fill"
)[0];
dropContainer.addEventListener(
  "dragover",
  (e) => {
    e.preventDefault();
  },
  false
);

dropContainer.addEventListener("dragenter", () => {
  dropContainer.classList.add("drag-active");
});

dropContainer.addEventListener("dragleave", () => {
  dropContainer.classList.remove("drag-active");
});

dropContainer.addEventListener("drop", (e) => {
  e.preventDefault();
  dropContainer.classList.remove("drag-active");
  fileInput.files = e.dataTransfer.files;
});

// Replace 'your_cloud_name' with your Cloudinary cloud name
const cloudName = "dk5acaaxg";
const uploadPreset = "tzhnmdgj";

// Function to upload image to Cloudinary
function uploadImage(file) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("upload_preset", uploadPreset);
  fileUploadDiv.style.display = "flex";

  //   return fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
  //     method: "POST",
  //     body: formData,
  //     folder: "TensionFlow_CodeCrafter",
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       fileUploadDivFill.style.width = "100%";
  //       setTimeout(() => {
  //         fileUploadDiv.style.display = "none";
  //         document.getElementsByClassName(
  //           "drop-container-done"
  //         )[0].style.display = flex;
  //       }, 3000);
  //       return data.secure_url;
  //     })
  //     .catch((error) =>
  //       console.error("Error uploading image to Cloudinary:", error)
  //     );
  return fetch("http://192.168.213.187:5001/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((result) => {
      fileUploadDivFill.style.width = "100%";
      setTimeout(() => {
        dropContainer.style.display = "none";
        document.getElementById("drop-container-done").style.display = "flex";
      }, 3000);
      console.log("Success:", result);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Event listener for file input change
fileInput.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  const imageUrl = await uploadImage(file);
  console.log("Image uploaded to Cloudinary:", imageUrl);
});
