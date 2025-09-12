import os
import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FishSpecies, ChatSession, ChatMessage
from .chatbot_service import ChatbotService
from .ontology_service import OntologyService


def chat_view(request):
    """Render the main chat interface"""
    return render(request, 'chatbot/chat.html')


@api_view(['GET'])
def species_list(request):
    """Get list of all fish species"""
    species = FishSpecies.objects.all()
    data = []
    for s in species:
        data.append({
            'id': s.id,
            'scientific_name': s.scientific_name,
            'vernacular_name': s.vernacular_name,
            'family': s.family,
            'threat_status': s.threat_status,
            'image_url': s.image_url
        })
    return Response(data)


@api_view(['GET'])
def species_detail(request, species_id):
    """Get detailed information about a specific fish species"""
    try:
        species = FishSpecies.objects.get(id=species_id)
        data = {
            'id': species.id,
            'scientific_name': species.scientific_name,
            'vernacular_name': species.vernacular_name,
            'family': species.family,
            'genus': species.genus,
            'threat_status': species.threat_status,
            'occurrence_status': species.occurrence_status,
            'max_size_cm': species.max_size_cm,
            'body_shape': species.body_shape,
            'body_color': species.body_color,
            'description': species.description,
            'habitat_type': species.habitat_type,
            'water_conditions': species.water_conditions,
            'specific_locations': species.specific_locations,
            'river_basins': species.river_basins,
            'districts': species.districts,
            'protected_areas': species.protected_areas,
            'image_url': species.image_url
        }
        return Response(data)
    except FishSpecies.DoesNotExist:
        return Response({'error': 'Species not found'}, status=404)


@api_view(['POST'])
def chat_api(request):
    """Handle chat API requests"""
    try:
        data = request.data
        message = data.get('message', '')
        session_id = data.get('session_id')
        
        if not message:
            return Response({'error': 'Message is required'}, status=400)
        
        # Get or create session
        if session_id:
            try:
                session = ChatSession.objects.get(session_id=session_id)
            except ChatSession.DoesNotExist:
                session = ChatSession.objects.create(session_id=session_id)
        else:
            session = ChatSession.objects.create(session_id=str(uuid.uuid4()))
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=message
        )
        
        # Get chatbot response
        chatbot_service = ChatbotService()
        response = chatbot_service.get_response(message)
        
        # Save assistant response
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=response
        )
        
        return Response({
            'response': response,
            'session_id': session.session_id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
