from django.shortcuts import render
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Downloader.settings import BASE_DIR
from yt_dlp import YoutubeDL



def home(request):
    return render(request, 'index.html')

@csrf_exempt
def download_media(request):
    if request.method == "POST":
        url = request.POST.get("url")
        media_type = request.POST.get("type", "video")  # video or audio

        try:
            ydl_opts = {
                'format': 'bestaudio/best' if media_type == "audio" else 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'cookiefile': os.path.join(BASE_DIR, 'cookies.txt'),
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Serve file back as download
            with open(filename, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
