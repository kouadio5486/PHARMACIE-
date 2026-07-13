"""API assistant IA (optionnel)."""
# Permet de créer automatiquement les opérations CRUD
# (Create, Read, Update, Delete)
from rest_framework import viewsets, status
from rest_framework.response import Response
# Permission : utilisateur connecté obligatoire
from rest_framework.permissions import IsAuthenticated
# Modèle contenant les interactions IA
from apps.ai.models import AIInteraction
from apps.ai.services import speech_to_text, text_to_speech, generate_ai_response

# IsOwnerOrAdmin : seul le propriétaire ou l'admin peut voir l'objet
# _is_admin : fonction qui vérifie si l'utilisateur est admin
from ..permissions import IsOwnerOrAdmin, _is_admin
# Serializers utilisés
from ..serializers.ai_serializers import (
    AIInteractionCreateSerializer,
    AIInteractionSerializer,
)


class AIInteractionViewSet(viewsets.ModelViewSet):
    """
    Historique des interactions IA par utilisateur.
    Types : search, symptom, general
    """
# /api/ai/?type=symptom
    filterset_fields = ("type",)
    ordering_fields = ("created_at",)
    http_method_names = ["get", "post", "head", "options"]
# Choix du serializer selon l'action
    def get_serializer_class(self):
        if self.action == "create":
            return AIInteractionCreateSerializer
        return AIInteractionSerializer

    def get_permissions(self):
        if self.action == "create":
            # Il suffit d'être connecté
            return [IsAuthenticated()]
            # connecté + propriétaire ou admin
        return [IsAuthenticated(), IsOwnerOrAdmin()]
 # Détermine quelles données l'utilisateur peut voir
    def get_queryset(self):
        # Utilisateur connecté
        user = self.request.user
        if _is_admin(user):
             # Il voit toutes les interactions
            return AIInteraction.objects.select_related("user").all()
             # l'utilisateur ne voit que ses propres interactions
        return AIInteraction.objects.filter(user=user)
 # Exécuté automatiquement lors du POST
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Process audio input if provided
        input_audio = serializer.validated_data.get('input_audio')
        input_text = serializer.validated_data.get('input')

        if input_audio and not input_text:
            # Convert speech to text
            input_text = speech_to_text(input_audio)
            if input_text:
                serializer.validated_data['input'] = input_text

        # Generate AI response if no output is provided
        output_text = serializer.validated_data.get('output')
        interaction_type = serializer.validated_data.get('type', 'general')
        
        if not output_text and input_text:
            output_text = generate_ai_response(input_text, interaction_type)
            serializer.validated_data['output'] = output_text

        # Generate audio output if we have text
        output_audio = serializer.validated_data.get('output_audio')
        if output_text and not output_audio:
            output_audio = text_to_speech(output_text)

        # Save the interaction
        ai_interaction = serializer.save(
            user=request.user,
            input=input_text,
            output=output_text
        )

        if output_audio:
            ai_interaction.output_audio.save(output_audio.name, output_audio)
            ai_interaction.save()

        # Return the response
        headers = self.get_success_headers(serializer.data)
        return Response(
            AIInteractionSerializer(ai_interaction, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
