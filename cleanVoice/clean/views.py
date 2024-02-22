from django.shortcuts import render
from django.http import JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import librosa
import librosa.display
import pandas as pd
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from .removeNoise import removeNoise
from pydub import AudioSegment
import io
import soundfile as sf




@csrf_exempt
def process_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        # Get the uploaded MP3 file
        audio_file = request.FILES['audio_file']
        audio_file_name = audio_file.name
        sr = 16000
        y2,sr = librosa.load(audio_file, mono=True, sr=sr, offset=0, duration=10)
        noise2 = y2[0:1*sr]

        try:
            # Convert the MP3 file to AudioSegment
            audio_segment =removeNoise(audio_clip=y2, noise_clip=noise2,
            n_grad_freq=2,
            n_grad_time=4,
            n_fft=2048,
            win_length=2048,
            hop_length=512,
            n_std_thresh=2.5,
            prop_decrease=1.0,
            verbose=False,
            visual=False)

            audio_bytes = io.BytesIO()
            output_file_name = f"clean_{audio_file_name}"
            sf.write(audio_bytes, audio_segment, sr, format='wav')
            response = HttpResponse(audio_bytes.getvalue(), content_type='audio/wav')
            response['Content-Disposition'] = f'attachment; filename="{output_file_name}"'

            return response



        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method or missing audio file'}, status=400)


# Create your views here.
