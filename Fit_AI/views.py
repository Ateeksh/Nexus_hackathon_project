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
from django.db import connection
import re
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
        info = extract_code(response)
        if extract_code(response)==False:
          response = markdown.markdown(response)
        else:
            if isinstance(info, str):
                response = info.split("\n")
                for command in response:
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(command)
                    except Exception as e:
                        print(f"Error executing command: {command}")
                        print(f"Error: {e}")
            response = "\n".join([line for line in response if not line.startswith("```")])
        return JsonResponse({'response': response})

def extract_code(input_text):
    # Regular expression to match code blocks enclosed in triple backticks
    code_block_pattern = r"```(?:[\w]+)?\n([\s\S]*?)\n```"
    matches = re.findall(code_block_pattern, input_text)

    if matches:
        return matches  # Return a list of code snippets
    return False  # Return False if no code snippets are found
def generateExercises(user):
        initial_prompt = [
          {
            "role": "system",
            "content": "You are a fitness assistant. Generate a list of exercises in JSON format. Each exercise should have a name, Reps, Sets, Timeperrep, and done status."
          },
          {
            "role": "user",
            "content": user
          }
        ]

        messages = initial_prompt + [{"role": "user", "content": user}]
        APIKEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=APIKEY)
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={ "type": "json_object" }  
        )
        response = completion.choices[0].message.content
        return response

def generateDiet(user):
        initial_prompt = [
          {
            "role": "system",
            "content": "You are a fitness assistant. Generate a list of diet items in JSON format. Each item should have a name, calories, protein, and eaten status."
          },
          {
            "role": "user",
            "content": user
          }
        ]

        messages = initial_prompt + [{"role": "user", "content": user}]
        APIKEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=APIKEY)
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={ "type": "json_object" }  
        )
        response = completion.choices[0].message.content
        return response


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
        exercises_data = generateExercises(name)
        diet_data = generateDiet(name)
        print(diet)
        # Populating FoodItem model
        for diet in diet_data:
            FoodItem.objects.create(
                name=diet["name"],
                calories=diet["calories"],
                protein=diet["protein"],
                eaten=diet["eaten"]
            )

        # Populating Exercises model
        for exercise in exercises_data:
            Exercises.objects.create(
                name=exercise["name"],
                Reps=exercise["reps"] if exercise["reps"] is not None else 0,
                Sets=exercise["sets"],
                Timeperrep=exercise["timePerRep"],
                done=exercise["done"]
            )

        fitness_instance = Fitness.objects.create(name=name)
        fitness_instance.diet.add(*FoodItem.objects.all())
        fitness_instance.exercise.add(*Exercises.objects.all())
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
        user_exercise = get_object_or_404(Fitness, name=name) 

        final = user_account+"\n"+user_pro+"\n"+user_goals+"\n"+str([exercises.name for exercises in user_exercise.exercise.all()])+"\n"+str([exercises.name for exercises in user_exercise.diet.all()])
        return JsonResponse({'User': final})

@csrf_exempt
def getExercise(request):
        body = json.loads(request.body)
        name = body.get("name", "")  
        user_account = get_object_or_404(Fitness, name=name) 
        return JsonResponse({'food': [exercises.name for exercises in user_account.exercise.all()]})
@csrf_exempt
def getDiet(request):
        body = json.loads(request.body)
        name = body.get("name", "")  
        user_account = get_object_or_404(Fitness, name=name) 
        return JsonResponse({'food': [exercises.name for exercises in user_account.diet.all()]})

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

def AI_command(request):
    body = json.loads(request.body)
    name = body.get("name", "")
    commands = body.get("code", "")


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
def main(request):
  return render(request,'App.html')

@csrf_exempt
def diet(request):
  return render(request,'diet.html')

@csrf_exempt
def excerCise(request):
  return render(request,'Excersise.html')


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
