function showPopup(imageSrc, captionText) {
    document.getElementById('popupImage').src = imageSrc;
    document.getElementById('popupCaption').innerText = captionText;
    document.getElementById('imagePopup').style.display = 'flex';
  }

  function closePopup() {
    document.getElementById('imagePopup').style.display = 'none';
  }