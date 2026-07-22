from sqlApp.models import Crop, Greenhouse
import re


class EntityExtractor:
    CROP_SYNONYMS = {
        "tomato": "tomato",
        "tomatoes": "tomato",
        "tomatoe": "tomato",
        "tomatoese": "tomato",

        "cucumber": "cucumber",
        "cucumbers": "cucumber",

        "carrot": "carrot",
        "carrots": "carrot",

        "potato": "potato",
        "potatoes": "potato",
        "patatoes": "potato",
    }
    @staticmethod
    def normalize(text):

        text = re.sub(r"[^a-zA-Z0-9 ]", "", text)

        text = text.lower()

        return text

    @staticmethod
    def extract_crop(question):

        question = EntityExtractor.normalize(question)

        words = question.split()

        canonical_crop = None

        for word in words:

            if word in EntityExtractor.CROP_SYNONYMS:

                canonical_crop = EntityExtractor.CROP_SYNONYMS[word]

                break

        if canonical_crop:

            for crop in Crop.objects.all():

                crop_name = EntityExtractor.normalize(crop.crop_name)

                if canonical_crop in crop_name:

                    return crop

        return None


    @staticmethod
    def extract_greenhouse(question):

        question = EntityExtractor.normalize(question)

        aliases = {

            "gh1": "gh001",
            "gh 1": "gh001",
            "greenhouse1": "gh001",
            "greenhouse 1": "gh001",
            "house1": "gh001",
            "house 1": "gh001",

            "gh2": "gh002",
            "gh 2": "gh002",
            "greenhouse2": "gh002",
            "greenhouse 2": "gh002",
            "house2": "gh002",
            "house 2": "gh002",

        }

        for alias, code in aliases.items():

            question = question.replace(alias, code)

        for greenhouse in Greenhouse.objects.all():

            db_code = EntityExtractor.normalize(greenhouse.greenhouse_code)

            if db_code in question:

                return greenhouse

        return None

            