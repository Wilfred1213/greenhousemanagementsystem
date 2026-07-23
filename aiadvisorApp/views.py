from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Conversation
from django.shortcuts import get_object_or_404

from .models import Conversation
from .services.ai_engine import KwasariAI
from .services.conversation_service import ConversationService
from .services.memory_service import MemoryService



from .models import Conversation

# @login_required
def chat(request, conversation_id=None):

    conversations = Conversation.objects.filter(

        user=request.user

    )

    conversation = None

    if conversation_id:

        conversation = Conversation.objects.get(

            id=conversation_id,

            user=request.user

        )

    return render(

        request,

        "aiadvisorApp/chat.html",

        {

            "conversation": conversation,

            "conversations": conversations,

        }

    )



def send_message(request):

    print("=" * 60)
    print("send_message view called")
    print("=" * 60)

    conversation_id = request.POST.get("conversation_id")
    user_message = request.POST.get("message", "").strip()

    # Prevent empty messages
    if not user_message:
        return render(
            request,
            "aiadvisorApp/partials/chat_window.html",
            {"conversation": None}
        )

    # --------------------------------------
    # Create or retrieve conversation
    # --------------------------------------

    if conversation_id:

        conversation = get_object_or_404(
            Conversation,
            id=conversation_id
        )

        # Save this new user message
        ConversationService.add_user_message(
            conversation,
            user_message
        )

    else:

        # create_conversation() already saves the first message
        conversation = ConversationService.create_conversation(
            request.user,
            user_message
        )

    # --------------------------------------
    # Build conversation memory
    # --------------------------------------

    context = MemoryService.build_context(conversation)

    print("=" * 60)
    print("Conversation Context")
    print(context)
    print("=" * 60)

    # --------------------------------------
    # Ask Kwasari
    # --------------------------------------

    ai = KwasariAI()

    reply = ai.ask(
        user_message,
        context=context
    )

    # --------------------------------------
    # Save AI response
    # --------------------------------------

    ConversationService.add_ai_message(
        conversation,
        reply
    )

    # --------------------------------------
    # Refresh conversation timestamp
    # --------------------------------------

    conversation.save()

    # --------------------------------------
    # Return updated chat window
    # --------------------------------------
    return render(
    request,
    "aiadvisorApp/partials/chat_response.html",
    {
        "conversation": conversation,
        "conversations": Conversation.objects.filter(
            user=request.user
        )
    }
)
    # return render(
    #     request,
    #     "aiadvisorApp/partials/chat_window.html",
    #     {
    #         "conversation": conversation
    #     }
    # )
# def send_message(request):
    
#     print("send_message view called")

#     conversation_id = request.POST.get("conversation_id")
#     user_message = request.POST.get("message")

#     # Create a new conversation if none exists
#     if conversation_id:

#         conversation = get_object_or_404(
#             Conversation,
#             id=conversation_id
#         )

#     else:

#         conversation = ConversationService.create_conversation(
#             request.user,
#             user_message
#         )

#     ai = KwasariAI()

#     # reply = ai.ask(user_message)
    
#     context = MemoryService.build_context(conversation)

#     reply = ai.ask(

#         user_message,

#         context=context

#     )

#     ConversationService.add_ai_message(

#         conversation,

#         reply

#     )

#     return render(

#         request,

#         "aiadvisorApp/partials/chat_window.html",

#         {

#             "conversation": conversation

#         }

#     )


# @login_required
def new_conversation(request):

    conversation = Conversation.objects.create(

        user=request.user,

        title="New Conversation"

    )

    return redirect(

        "ai:conversation",

        conversation_id=conversation.id

    )