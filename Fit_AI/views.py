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


