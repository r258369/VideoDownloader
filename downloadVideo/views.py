from django.shortcuts import render
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yt_dlp import YoutubeDL

# Load environment variables for login
YTDLP_USERNAME = os.environ.get("xyz328719@gmail.com")  # Your Gmail
YTDLP_PASSWORD = os.environ.get("ratul@369")     # Optional: path to cookies.txt


def home(request):
    return render(request, 'index.html')


@csrf_exempt
def download_media(request):
    if request.method == "POST":
        url = request.POST.get("url")
        media_type = request.POST.get("type", "video")  # video or audio

        if not url:
            return JsonResponse({"error": "No URL provided"}, status=400)

        try:
            # Setup yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best' if media_type == "audio" else 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'noplaylist': True,
            }

            # Add login if credentials are provided
            if YTDLP_USERNAME and YTDLP_PASSWORD:
                ydl_opts['username'] = YTDLP_USERNAME
                ydl_opts['password'] = YTDLP_PASSWORD


            # Download using yt-dlp
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Serve file as download
            with open(filename, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
