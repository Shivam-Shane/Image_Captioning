from django.shortcuts import render
from .models import ImageSaver
from src.imagecaptioning.pipeline.app_prediction import DataPredictionPipeline  # type: ignore
from .forms import ImageUploadFile  # Ensure this import is correct
import io
import os
from PIL import Image, UnidentifiedImageError
from django.conf import settings
from logger import logging


def home(request):
    return render(request, 'index.html')

def delete_existing_images():
    images = ImageSaver.objects.all()
    for image in images:
        image_path = os.path.join(settings.MEDIA_ROOT, image.image.path)
        logging.info(f"Deleting image: {image_path}")
        if os.path.exists(image_path):
            os.remove(image_path)
    images.delete()

def predictor(request):
    caption = None
    if request.method == 'POST':
        delete_existing_images()
        form = ImageUploadFile(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Save the instance first
            image_path = instance.image.path  # Get the file path of the saved image
            
            try:
                # Open the image to verify it
                with open(image_path, 'rb') as f:
                    img = Image.open(f)
                    img.verify()  # Verify that it is an image

                # Re-open the image file for processing
                with open(image_path, 'rb') as f:
                    image_file = io.BytesIO(f.read())
                    callableobject = DataPredictionPipeline()
                    caption = callableobject.main(image_file)
                    logging.info(f"Returning caption: {caption}")

            except UnidentifiedImageError:
                logging.error("Uploaded file is not a valid image.")
                caption = "Uploaded file is not a valid image."
    else:
        form = ImageUploadFile()
    images = ImageSaver.objects.all()
    return render(request, 'index.html', {'form': form, 'caption': caption, 'images': images})