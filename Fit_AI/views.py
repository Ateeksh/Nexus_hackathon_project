from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from django.http import JsonResponse
import os
from dotenv import load_dotenv
load_dotenv()
# Create your views here.
@csrf_exempt
def ask(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        prompt = body.get("prompt", "")  
        APIKEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=APIKEY)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt
        )
        response = completion.choices[0].message.content
        return JsonResponse({'response': response})



@csrf_exempt
def login(request):
  return render(request,'Login.html')

@csrf_exempt
def register(request):
  return render(request,'register.html')

@csrf_exempt
def main(request):
  return render(request,'App.html')

@csrf_exempt
def Ai(request):
  return render(request,'AI_assistant.html')

@csrf_exempt
def scan(request):
  return render(request,'calories_camera.html')
