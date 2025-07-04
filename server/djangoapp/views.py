from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            logger.debug(f"Login attempt for user: {username}")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {username} authenticated successfully")
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                logger.warning(f"Invalid credentials for user: {username}")
                return JsonResponse({"userName": username, "status": "Invalid credentials"}, status=401)

        except Exception as e:
            logger.error(f"Error in login view: {e}")
            return JsonResponse({"status": "Invalid request"}, status=400)
    else:
        return JsonResponse({"status": "Only POST allowed"}, status=405)

@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Already Registered"}, status=400)

            # Create new user
            user = User.objects.create_user(username=username, password=password, email=email,
                                            first_name=first_name, last_name=last_name)
            user.save()

            # Automatically log in the new user
            login(request, user)

            logger.info(f"User {username} registered and logged in successfully")
            return JsonResponse({"userName": username, "status": "Registered"})

        except Exception as e:
            logger.error(f"Error in register view: {e}")
            return JsonResponse({"status": "Invalid request"}, status=400)
    else:
        return JsonResponse({"status": "Only POST allowed"}, status=405)
