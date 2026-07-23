from sqlApp.models import Crop, Greenhouse


class ConversationMemory:

    @staticmethod
    def latest_crop(context):

        if not context:
            return None

        crops = Crop.objects.all()

        for message in reversed(context):

            text = message["content"].lower()

            for crop in crops:

                if crop.crop_name.lower() in text:
                    return crop.crop_name.lower()

        return None


    @staticmethod
    def latest_greenhouse(context):

        if not context:
            return None

        greenhouses = Greenhouse.objects.all()

        for message in reversed(context):

            text = message["content"].lower()

            for gh in greenhouses:

                if gh.greenhouse_name.lower() in text:
                    return gh.greenhouse_code

                if gh.greenhouse_code.lower() in text:
                    return gh.greenhouse_code

        return None