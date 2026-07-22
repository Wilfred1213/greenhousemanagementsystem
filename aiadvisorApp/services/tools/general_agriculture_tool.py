from .base_tool import BaseTool


class GeneralAgricultureTool(BaseTool):

    name = "General Agriculture"

    description = "Answers general agriculture questions."

    keywords = []

    def execute(self, question):

        return f"""
        I understand your question:

        "{question}"

        At the moment I specialize in analysing your farm records.

        Soon I will also answer general agricultural questions using an AI language model.

        For example:

        • Crop production
        • Livestock
        • Poultry
        • Beekeeping
        • Soil fertility
        • Pest and disease management
        • Irrigation
        • Weather advice
        """