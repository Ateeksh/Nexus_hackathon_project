from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from .models import *
import base64
from django.http import JsonResponse
import datetime
from decimal import Decimal
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
import markdown
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
        response = markdown.markdown(response)
        return JsonResponse({'response': response})


def ask_gpt(prompt):
        APIKEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=APIKEY)
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            response_format={ "type": "json_object" }  
        )
        response = completion.choices[0].message.content
        response = markdown.markdown(response)

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



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8") 

def send_to_openai(file_path):
    apikey = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=apikey )
    base64_image = encode_image(file_path)
    response =client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Estimate the Calories and protein in json and return a json like this - '{ 'calories': 300, 'protein': 15}'"},
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
def block_user(request):
        body = json.loads(request.body)
        name = body.get("name", "")  
        UserAccount.objects.filter(name=name).update(usage = False)
        return JsonResponse({'message': 'User blocked successfully', 'user_id': name})

@csrf_exempt
def check_name(request):
            try:
                body = json.loads(request.body)
                name = body.get("name", "")  
                exists = UserAccount.objects.filter(name=name).exists()
                if exists:
                    return JsonResponse({"exists": True})
                else:
                    return JsonResponse({"exists": False})
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

@csrf_exempt
def compare_name_pass(request):
        body = json.loads(request.body)
        name = body.get("name", "")  
        passs = body.get("password", "")  
        user = UserAccount.objects.filter(name=name, password=passs).first()
        if user:
            return JsonResponse({"match": True,"Account":True})
        else:
             return JsonResponse({"match": False,"Account":True})

@csrf_exempt
def set_all(request):
  body = json.loads(request.body)
  name = body.get("name", "")
  user_account = get_object_or_404(User, name=name)
  
  protein = body.get("protein", None)
  if protein is not None:
    user_account.protein = protein
  
  calories = body.get("calories", None)
  if calories is not None:
    user_account.calories = calories
  
  weight = body.get("weight", None)
  if weight is not None:
    print(weight)
    user_account.weight = weight
  
  sleep = body.get("sleep", None)
  if sleep is not None:
    user_account.sleep = sleep
  
  steps = body.get("steps", None)
  if steps is not None:
    user_account.steps = steps
  
  user_account.save()
  return JsonResponse({'message': 'User metrics set successfully', 'user_id': name})
    

@csrf_exempt
def get_all(request):
          body = json.loads(request.body)
          print("19")
          name = body.get("name", "")  
          try:
            print("bye")
            user_account = get_object_or_404(User, name=name)
            user_data = {
          "steps": user_account.steps,
          "sleep": user_account.sleep,
          "calories": user_account.calories,
          "weight": user_account.weight,
          "protein": user_account.protein,  
          }
            return JsonResponse(user_data)
          except: 
            print("Hi")
            return JsonResponse({"error": "User not found"})

@csrf_exempt
def get_all_goals(request):
          body = json.loads(request.body)
          print("19")
          name = body.get("name", "")  
          try:
            print("bye")
            user_account = get_object_or_404(UserGoals, name=name)
            user_data = {
              "steps_goal": user_account.steps_goal,
              "sleep_goal": user_account.sleep_goal,
              "calories_goal": user_account.calories_goal,
              "weight_goal": user_account.weight_goal,
              "protein_goal": user_account.protein_goal,
            }
            return JsonResponse(user_data)
          except: 
            print("Hi")
            return JsonResponse({"error": "User not found"})
@csrf_exempt
def set_all_goals(request):
  body = json.loads(request.body)
  name = body.get("name", "")
  user_goals = get_object_or_404(UserGoals, name=name)
  
  protein_goal = body.get("protein_goal", None)
  if protein_goal is not None:
    user_goals.protein_goal = protein_goal
  
  calories_goal = body.get("calories_goal", None)
  if calories_goal is not None:
    user_goals.calories_goal = calories_goal
  
  weight_goal = body.get("weight_goal", None)
  if weight_goal is not None:
    user_goals.weight_goal = weight_goal
  
  sleep_goal = body.get("sleep_goal", None)
  if sleep_goal is not None:
    user_goals.sleep_goal = sleep_goal
  
  steps_goal = body.get("steps_goal", None)
  if steps_goal is not None:
    user_goals.steps_goal = steps_goal
  
  user_goals.save()
  return JsonResponse({'message': 'User goals set successfully', 'user_id': name})

@csrf_exempt
def add_account(request):
        body = json.loads(request.body)
        name = body.get("name", "")
        passs = body.get("password", "")
        weight = body.get("we", "")
        age = body.get("ag", "")
        height = body.get("he", "")
        Medical_history = body.get("Mh", "")
        Additional_information =  body.get("Ai", "")
        new_account = UserAccount(name=name, password=passs)
        print(f"Saving UserAccount: name={new_account.name}, password={new_account.password}")
        new_account.save()
        new_user = User(name=name, date=datetime.date.today(),weight=weight)
        new_user.save()
        new_profile = UserProfile(
            name=name,
            weight=weight,
            age=age,
            height=height,
            Medical_history=Medical_history,
            Additional_information=Additional_information,
        )
        new_profile.save()
        new_fitness = Fitness(name=name) 
        new_fitness.save()
        goals = UserGoals(name=name)
        goals.save()
        return JsonResponse({'message': 'Account created successfully', 'user_id': name})

@csrf_exempt
def get_user(request):
        body = json.loads(request.body)
        name = body.get("name", "")
        try:
          user_account = str(get_object_or_404(User, name=name))
        except:
            print("user_account not working")
        try:  
          user_pro = str(get_object_or_404(UserProfile, name=name))
        except:
            print("else")
        try:  
          user_goals = str(get_object_or_404(UserGoals, name=name))
        except:
            print("else")
        final = user_account+"\n"+user_pro+"\n"+user_goals
        print(final) 
        return JsonResponse({'User': final})

@csrf_exempt
def getExercise(request):
        body = json.loads(request.body)
        name = body.get("name", "")  
        user_account = get_object_or_404(Fitness, name=name) 
        return JsonResponse({'food': [exercises.name for exercises in user_account.exercise.all()]})

@csrf_exempt
def set_calories(request):
        body = json.loads(request.body)
        name = body.get("name", "")
        calories = body.get("calories", "")
        protein = body.get("protein", "")
        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid amount"})
        user = User.objects.filter(name=name).first()
        if user:
            user.calories =  Decimal(calories)
            user.protein =  Decimal(protein)
            user.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})


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
def exercise_info(request):
  return render(request,'exercise.html')

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
def steps(request):
  return render(request,'steps.html')

@csrf_exempt
def steps(request):
  return render(request,'steps.html')

@csrf_exempt
def Ai(request):
  return render(request,'AI_assistant.html')

@csrf_exempt
def scan(request):
  return render(request,'calories_camera.html')

@csrf_exempt
def weight(request):
  return render(request,'Weight.html')
