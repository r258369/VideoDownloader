

from django.shortcuts import render
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yt_dlp import YoutubeDL

YOUTUBE_EMAIL = "xyz328719@gmail.com"
YOUTUBE_PASSWORD = "ratul@369"  # use app password if 2FA is enabled

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def download_media(request):
    if request.method == "POST":
        url = request.POST.get("url")
        media_type = request.POST.get("type", "video")  # video or audio

        if not url:
            return JsonResponse({"error": "URL is required"}, status=400)

        try:
            # yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best' if media_type == "audio" else 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'username': YOUTUBE_EMAIL,
                'password': YOUTUBE_PASSWORD,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Serve file back
            with open(filename, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
