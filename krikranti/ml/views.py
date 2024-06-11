from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
 #import torch
from PIL import Image
 #import torchvision.transforms as transforms

# Load model
# model = torch.load('/')


def welcome(request):
    return render(request, 'index.html')

# Create your views here.
