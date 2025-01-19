from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def ask(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        prompt = body.get("prompt", "")  
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt
        )
        return JsonResponse({'access': completion})

def login(request):
  return render(request,'Login.html')

def register(request):
  return render(request,'register.html')

def main(request):
  return render(request,'App.html')

def Ai(request):
  return render(request,'AI_assistant.html')

def scan(request):
  return render(request,'calories_camera.html')
