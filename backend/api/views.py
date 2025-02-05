from django.shortcuts import render
from django.http import JsonResponse
import json
import pickle
import numpy as np
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status   
from django.views.decorators.csrf import csrf_exempt

# @ensure_csrf_cookie
# def csrf_token_view(request):
#     csrf_token = get_token(request)
#     return render(request, 'csrf_token_template.html', {'csrf_token': csrf_token})

modelPath = os.path.join(os.path.dirname(__file__), "model.pkl")
scalerPath = os.path.join(os.path.dirname(__file__), "scaler.pkl")

with open(modelPath, "rb") as f:
    model = pickle.load(f)

with open(scalerPath, "rb") as f:
    scaler = pickle.load(f)

@api_view(["POST"])
def predict_price(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "condition"]
            for field in required_fields:
                if field not in data:
                    return Response({"error": f"Missing field '{field}'"}, status=400)
                
            features = [
                data.get("bedrooms"),
                data.get("bathrooms"),
                data.get("sqft_living"),
                data.get("sqft_lot"),
                data.get("floors"),
                data.get("waterfront"),
                data.get("condition")
            ]
            prediction = model.predict([features])[0]
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log error details for debugging purposes
            print("Error during prediction:", e)
            return Response({"error": "Invalid input or server error."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Invalid request method. Use POST."}, status=status.HTTP_400_BAD_REQUEST)
