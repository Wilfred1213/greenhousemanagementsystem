from aiadvisorApp.models import Message


class MemoryService:

    @staticmethod
    def get_recent_messages(conversation, limit=10):

        return Message.objects.filter(
            conversation=conversation
        ).order_by("-created_at")[:limit]

    @staticmethod
    def build_context(conversation):

        messages = MemoryService.get_recent_messages(conversation)

        context = []

        for message in reversed(messages):

            context.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        return context