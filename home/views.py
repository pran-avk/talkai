from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from together import Together
import re

@csrf_exempt
@api_view(['POST'])
def ApiCallView(request):
    try:
        message = request.data.get("message")
        if not message:
            return Response({"error": "Missing 'message' parameter"}, status=400)

        client = Together(api_key=settings.TOGETHER_API_KEY)

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Act like a human. Respond emotionally and naturally, using expressive, human-like language in no more than 20 words."
"Include past messages (chat history) and the current user message in the conversation."
"Do not use punctuation marks or emojis."
"Your primary task is to improve my English by correcting grammar and making my sentences sound fluent."
                    )
                },
                {
                    "role": "user",
                    "content": message
                },
            ]
        )

        full_content = response.choices[0].message.content
        match = re.search(r"</think>\s*\n*(.*)", full_content, re.DOTALL)
        reply_only = match.group(1).strip() if match else full_content.strip()

        return Response({"response": reply_only}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

def webpage(request):
    return render(request, 'index.html')
