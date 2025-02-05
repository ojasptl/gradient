from django.shortcuts import render
from django.http import JsonResponse
import json
import pickle
import numpy as np
import os
from django.middleware.csrf import get_token
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

@csrf_exempt
def predict_price(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "condition"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing field '{field}'"}, status=400)
                
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
            return JsonResponse({"predicted_price": float(prediction)})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)
