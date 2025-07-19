from django.shortcuts import render
from django.http import JsonResponse

# Dummy view for validation
def test_view(request):
    return JsonResponse({'message': 'Chats app is working'})
