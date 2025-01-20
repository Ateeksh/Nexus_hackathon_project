from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from pydantic import BaseModel
from openai import OpenAI
from .models import *
import base64
from django.http import JsonResponse
from decimal import Decimal
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
load_dotenv()
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
def file_upload(request):
    if request.method == 'POST':
            uploaded_file = request.FILES['file']
            temp_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(temp_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            openai_response = send_to_openai(temp_file_path)
            openai_response = openai_response.choices[0].message.content
            print(openai_response)
            os.remove(temp_file_path)
            return JsonResponse({'message': 'File processed successfully!', 'response': openai_response})
    return JsonResponse({'error': 'Invalid request method or missing file.'}, status=400)


class Nutrient(BaseModel):
    Protien: str
    Calories: list[str] 
res_for = {
  "name": "nutrition_analysis",
  "schema": {
    "type": "object",
    "properties": {
      "calories": {
        "type": "number",
        "description": "The total calories present in the food item identified from the image."
      },
      "protein": {
        "type": "number",
        "description": "The total protein content present in the food item identified from the image."
      }
    },
    "required": [
      "calories",
      "protein"
    ],
    "additionalProperties": False
  },
  "strict": True
}
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8") 
    
def send_to_openai(file_path):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") )
    base64_image = encode_image(file_path)

    response =client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Estimate the Calories and Protien in json and return a json like this - '{ 'calories': 300, 'protein': 15}'"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},

                },

                    ],
                }
            ],
            response_format={ "type": "json_object" }  # Ensure JSON response

        )
    return response

@csrf_exempt
def getDiet(request):
    if request.method == "POST":
        body = json.loads(request.body)
        name = body.get("name", "")  
        user_account = get_object_or_404(Fitness, name=name)
        access_value = user_account.diet  
        return JsonResponse({'access': access_value})

@csrf_exempt
def add_calories(request):
    if request.method == "POST":
        body = json.loads(request.body)
        name = body.get("name", "")
        calories = body.get("cal", "")
        protien = body.get("pro", "")
        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid amount"})
        user = UserAccount.objects.filter(name=name).first()
        if user:
            user.balance =  Decimal(amount)
            user.save()
            return JsonResponse({"success": True, "new_balance": user.balance})
        return JsonResponse({"success": False, "message": "User not found"})
@csrf_exempt
def getCalories(request):
    if request.method == "POST":
        body = json.loads(request.body)
        name = body.get("name", "")
        calories = body.get("cal", "")
        protien = body.get("pro", "")
        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid amount"})
        user = UserAccount.objects.filter(name=name).first()
        if user:
            user.balance =  Decimal(amount)
            user.save()
            return JsonResponse({"success": True, "new_balance": user.balance})
        return JsonResponse({"success": False, "message": "User not found"})

@csrf_exempt
def compare_namenpass(request):
    pass

@csrf_exempt
def check_email(request):
    pass

@csrf_exempt
def create_account(request):
    pass

@csrf_exempt
def Add_to_profile(request):
    pass

@csrf_exempt
def get_sleep(request):
    pass

@csrf_exempt
def add_sleep(request):
    pass 

@csrf_exempt
def add_food(request):
    pass

@csrf_exempt
def login(request):
  return render(request,'Login.html')

@csrf_exempt
def register(request):
  return render(request,'register.html')

@csrf_exempt
def Nutrient_info(request):
  return render(request,'Nutrient.html')

@csrf_exempt
def register(request):
  return render(request,'Excersise.html')

@csrf_exempt
def main(request):
  return render(request,'App.html')

@csrf_exempt
def diet(request):
  return render(request,'diet.html')

@csrf_exempt
def sleep(request):
  return render(request,'sleep.html')

@csrf_exempt
def Ai(request):
  return render(request,'AI_assistant.html')

@csrf_exempt
def scan(request):
  return render(request,'calories_camera.html')
