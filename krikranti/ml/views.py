from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import torch
import io
from PIL import Image
import torchvision.transforms as tt
from .load_model import model

classes = {0: 'bacterial_leaf_blight', 1: 'brown_spot', 2: 'healthy', 3: 'leaf_blast', 4: 'leaf_scald',
           5: 'narrow_brown_spot'}  # Dictionary mapping index to label name


stats = ((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))

# Data augmentation and normalization for training
train_tfms = tt.Compose([
    tt.Resize((32, 32)),  # Resize images to 32x32 pixels
    tt.RandomHorizontalFlip(),
    tt.ToTensor(),
    tt.Normalize(*stats, inplace=True)
])

# Normalization for validation
valid_tfms = tt.Compose([
    tt.Resize((32, 32)),  # Resize images to 32x32 pixels
    tt.ToTensor(),
    tt.Normalize(*stats)
])


def welcome(request):
    return render(request, 'index.html')


# Create your views here.

@csrf_exempt
def predict(request):
    """Handle the image upload and return the model prediction."""
    if request.method == 'POST' and 'image' in request.FILES:
        try:
            # Open the uploaded image file
            image = Image.open(request.FILES['image'])

            # Preprocess the image
            image = valid_tfms(image)
            image = image.unsqueeze(0)  # Add batch dimension

            # Perform inference
            with torch.no_grad():
                output = model(image)

            # Process output (example: convert to label)
            _, predicted = torch.max(output, 1)
            predicted_label = classes[predicted.item()]  # Convert tensor to a Python integer

            # Return prediction as JSON response
            return JsonResponse({'prediction': predicted_label})

        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'POST request with image file required'})
