import io
import os
from PIL import Image, UnidentifiedImageError
from django.shortcuts import render
from .models import ImageSaver
from src.imagecaptioning.pipeline.app_prediction import DataPredictionPipeline  # type: ignore
from .forms import ImageUploadFile  
from django.conf import settings
from logger import logging


def home(request):
    return render(request, 'index.html')

def delete_existing_images():
    images = ImageSaver.objects.all() # Getting all the images store in the database
    for image in images:
        image_path = os.path.join(settings.MEDIA_ROOT, image.image.path)
        logging.info(f"Deleting image: {image_path}")
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
                logging.error(f"Error deleting image {image_path}: {e}")

    images.delete()  #deletes from database

def predictor(request):
    caption = None
    if request.method == 'POST':
        delete_existing_images() #calling function to delete existing images
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
                    dataprediction = DataPredictionPipeline()
                    caption = dataprediction.main(image_file)
                    logging.info(f"Generated caption: {caption}")

            except UnidentifiedImageError:
                logging.error("Uploaded file is not a valid image.")
                caption=None
    else:
        form = ImageUploadFile()
    images = ImageSaver.objects.all()
    return render(request, 'index.html', {'form': form, 'caption': caption, 'images': images})