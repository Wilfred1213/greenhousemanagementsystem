from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    OperationLog,
    InventoryTransaction
)


@receiver(post_save, sender=OperationLog)
def create_inventory_issue(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.product is None:
        return

    if not instance.quantity:
        return

    InventoryTransaction.objects.create(
        product=instance.product,
        transaction_type="Issue",
        quantity=instance.quantity,
        transaction_date=instance.activity_date,
        unit_cost=instance.product.unit_cost,
        reference=f"Maintenance #{instance.id}",
        performed_by=instance.performed_by,
        remarks=(
            f"Automatically generated from "
            f"{instance.maintenance_type}"
        )
    )