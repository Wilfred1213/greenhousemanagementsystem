class IntentRouter:
    
    ANALYSIS = [
        "best",
        "highest",
        "lowest",
        "compare",
        "better",
        "most",
    ]

    ROUTES = {

        "harvest": [
            "harvest",
            "yield",
            "produce",
            "production",
            "kg",
            "crate",
            "tomato",
            "tomatoes",
            "cucumber",
            "carrot",
        ],

        "greenhouse": [
            "greenhouse",
            "bed",
            "bay",
            "occupancy",
            "available beds",
        ],

        "weather": [
            "weather",
            "temperature",
            "humidity",
            "rain",
            "wind",
        ],

        "inventory": [
            "inventory",
            "stock",
            "fertilizer",
            "chemical",
        ],
        'crop': [

        'crop',

        'crops',

        'tomato',

        'tomatoes',

        'cucumber',

        'pepper',

        'lettuce',

        'plant',

        'planted',

    ],

    }

    @classmethod
    def detect(cls, question):

        question = question.lower()

        # Check analysis first
        if any(word in question for word in cls.ANALYSIS):
            return "analysis"

        # Then check normal routes
        for intent, words in cls.ROUTES.items():

            if any(word in question for word in words):
                return intent

        return "general"