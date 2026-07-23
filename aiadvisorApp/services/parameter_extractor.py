from dataclasses import dataclass

from .entity_extractor import EntityExtractor


@dataclass
class Parameters:

    crop = None

    greenhouse = None

    season = None

    month = None

    year = None

    date = None


class ParameterExtractor:

    @staticmethod
    def extract(question):

        p = Parameters()

        p.crop = EntityExtractor.extract_crop(question)

        p.greenhouse = EntityExtractor.extract_greenhouse(question)

        return p