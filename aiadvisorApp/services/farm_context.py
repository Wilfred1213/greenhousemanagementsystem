from sqlApp.models import (
    Greenhouse,
    Crop,
    Harvest,
    ProductionCycle,
    Bed,
)

from django.db.models import Sum


class FarmContext:

    @staticmethod
    def get_summary():

        return {

            "greenhouses": Greenhouse.objects.count(),

            "beds": Bed.objects.count(),

            "occupied_beds": Bed.objects.filter(
                status="Occupied"
            ).count(),

            "available_beds": Bed.objects.filter(
                status="Available"
            ).count(),

            "production_cycles": ProductionCycle.objects.count(),

            "crops": Crop.objects.count(),

            "harvests": Harvest.objects.count(),

            "total_harvest": Harvest.objects.aggregate(
                total=Sum("quantity_kg")
            )["total"] or 0,

        }