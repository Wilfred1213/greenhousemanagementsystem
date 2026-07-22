from aiadvisorApp.models import Conversation, Message


class ConversationService:
    
    @staticmethod
    def create_conversation(user, first_message):

        title = first_message.strip()

        # Limit to 50 characters
        if len(title) > 50:
            title = title[:50] + "..."

        conversation = Conversation.objects.create(
            user=user,
            title=title
        )

        Message.objects.create(
            conversation=conversation,
            role="USER",
            content=first_message
        )

        return conversation


    @staticmethod
    def add_user_message(conversation, message):

        return Message.objects.create(

            conversation=conversation,

            role="USER",

            content=message

        )


    @staticmethod
    def add_ai_message(conversation, reply):

        return Message.objects.create(

            conversation=conversation,

            role="AI",

            content=reply or "Sorry, I couldn't generate a response."

        )