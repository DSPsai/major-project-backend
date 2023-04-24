import requests
import os
from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tensorflow import keras
from pathlib import Path
import cv2
import numpy as np
from django.http import JsonResponse
#
CLASSES_LIST=[
    'Bend',
    'Catch Cap',
    'Draw Tick',
    'Draw X',
    'Drink',
    'Forward Kick',
    'Hand Clap',
    'High arm wave',
    'High throw',
    'Horizontal arm wave',
    'Phone Call',
    'Side Kick',
    'Sit down',
    'Stand up',
    'Take Umbrella',
    'Toss Paper',
    'Two hand wave',
    'Walk'
]

BASE_DIR = Path(__file__).resolve().parent.parent
print('Loading Model....')
model = keras.models.load_model(os.path.join(BASE_DIR, 'storefront', 'version3_9627acc.h5'))
print('Model Loaded')
def extract_frames_predict(video_path):
    # read the frames of the video
    n_frames=60
    frames = []
    width=180
    height=140
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(frame)
    cap.release()

    data=[]
    for i in range(0, len(frames), n_frames):
        sequence = frames[i:i+n_frames]
        if len(sequence) == n_frames:
            sequence=np.array([sequence])
            pred=model.predict(sequence)
            data.append(CLASSES_LIST[np.argmax(pred)])
    return data

@csrf_exempt
def index(request):
    print('Request Recieved')
    if request.method == 'POST':
        print('POST Request Recieved')
        video_file = request.FILES.get('file')
        if video_file:
            print('File is Attached')
            file_path = os.path.join(BASE_DIR, 'Prediction', 'pred.mp4')
            with open(file_path, 'wb+') as destination:
                print('Saving File')
                for chunk in video_file.chunks():
                    destination.write(chunk)
            print('Video saved:', file_path)
            predictions=extract_frames_predict(os.path.join(BASE_DIR, 'Prediction', 'pred.mp4'))
            response={
                "predictions":predictions
            }
            print(response)
            return JsonResponse(response)
        else:
            return HttpResponse("Insert a Video",status=500)
    if request.method == 'GET':
        return render(request, 'input.html')
