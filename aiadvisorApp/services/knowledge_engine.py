class KnowledgeEngine:
    
    @staticmethod
    def gather(plan):

        context = {}

        if plan.crop:
            context["crop"] = plan.crop

        if plan.greenhouse:
            context["greenhouse"] = plan.greenhouse

        if plan.month:
            context["month"] = plan.month

        if plan.year:
            context["year"] = plan.year

        return context