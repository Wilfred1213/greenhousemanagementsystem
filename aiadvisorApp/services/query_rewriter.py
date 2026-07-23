import re

from .conversation_memory import ConversationMemory


class QueryRewriter:

    @staticmethod
    def rewrite(question, context):

        crop = ConversationMemory.latest_crop(context)

        greenhouse = ConversationMemory.latest_greenhouse(context)

        rewritten = question

        if crop:
            rewritten = re.sub(
                r"\bit\b",
                crop,
                rewritten,
                flags=re.IGNORECASE
            )

            rewritten = re.sub(
                r"\bthem\b",
                crop,
                rewritten,
                flags=re.IGNORECASE
            )

        if greenhouse:
            rewritten = re.sub(
                r"\bthat greenhouse\b",
                greenhouse,
                rewritten,
                flags=re.IGNORECASE
            )

        print("=" * 50)
        print("Memory crop:", crop)
        print("Original :", question)
        print("Rewritten:", rewritten)
        print("=" * 50)

        return rewritten

# from .conversation_memory import ConversationMemory


# class QueryRewriter:

#     @staticmethod
#     def rewrite(question, context):

#         crop = ConversationMemory.latest_crop(context)

#         greenhouse = ConversationMemory.latest_greenhouse(context)

#         rewritten = question.lower()

#         if crop:

#             rewritten = rewritten.replace(" it ", f" {crop} ")
#             rewritten = rewritten.replace(" them ", f" {crop} ")
#             rewritten = rewritten.replace(" that crop ", f" {crop} ")
#             rewritten = rewritten.replace(" the crop ", f" {crop} ")

#         if greenhouse:

#             rewritten = rewritten.replace(" that greenhouse ", greenhouse.lower())

#         print("=" * 50)
#         print("Original :", question)
#         print("Rewritten:", rewritten)
#         print("=" * 50)

#         return rewritten