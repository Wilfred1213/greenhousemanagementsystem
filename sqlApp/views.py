from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q, Avg
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from django.contrib.auth.decorators import login_required

from .models import Farmer, Crop, Greenhouse, Harvest
from django.db.models.functions import Coalesce
import json
from django.db.models.functions import TruncMonth

from django.shortcuts import render
from django.db.models import Sum, F,  DecimalField, ExpressionWrapper, Count, Prefetch

import json

from .models import *
from decimal import Decimal
from . forms import OperationLogForm
from django.http import JsonResponse
from itertools import chain
from operator import attrgetter
from django.contrib import messages

def dashboard(request):

    farmers = Farmer.objects.count()
    crops = Crop.objects.count()
    greenhouses = Greenhouse.objects.count()
    active_cycles = (
    ProductionCycle.objects
    .exclude(status="Completed")
    .count()
    )

    beds = Bed.objects.count()

    nursery_batches = NurseryBatch.objects.count()

    operations = OperationLog.objects.count()

    products = Product.objects.count()

    inventory_value = (
    Product.objects.aggregate(
        total=Coalesce(
            Sum(
                F("current_stock") * F("unit_cost"),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            ),
            Decimal("0.00")
        )
    )["total"]
    )

    low_stock_products = (
    Product.objects
    .filter(
        current_stock__lte=F("minimum_stock"),
        is_active=True
    )
    .order_by("current_stock")
    )

    harvests = Harvest.objects.count()

    total_harvest = Harvest.objects.aggregate(
        total=Coalesce(Sum("quantity_kg"), Decimal("0"))
    )["total"]

    average_harvest = Harvest.objects.aggregate(
        avg=Coalesce(Avg("quantity_kg"), Decimal("0"))
    )["avg"]

    today = timezone.now().date()

    harvest_today = (
        Harvest.objects.filter(
            harvest_date=today
        ).aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0")
            )
        )["total"]
    )


    crop_data = (
        Harvest.objects
        .values("production_cycle_bed__production_cycle__crop_variety__crop__crop_name")
        .annotate(total=Sum("quantity_kg"))
        .order_by("production_cycle_bed__production_cycle__crop_variety__crop__crop_name")
    )

    crop_labels = [i["production_cycle_bed__production_cycle__crop_variety__crop__crop_name"] for i in crop_data]
    crop_totals = [float(i["total"]) for i in crop_data]


    greenhouse_data = (
        Harvest.objects
        .values("production_cycle_bed__production_cycle__greenhouse__greenhouse_name")
        .annotate(total=Sum("quantity_kg"))
    )

    greenhouse_labels = [
        g["production_cycle_bed__production_cycle__greenhouse__greenhouse_name"]
        for g in greenhouse_data
    ]

    greenhouse_totals = [
        float(g["total"])
        for g in greenhouse_data
    ]


    recent_harvests = (
    Harvest.objects.select_related(
        "production_cycle_bed",
        "production_cycle_bed__production_cycle",
        "production_cycle_bed__production_cycle__crop_variety",
        "production_cycle_bed__production_cycle__crop_variety__crop",
        "harvest_grade",
        "harvested_by",
    ).order_by("-harvest_date")[:5]
    )

    recent_operations = (
    OperationLog.objects
    .select_related(
        "maintenance_type",
        "production_cycle",
        "bay",
        "performed_by",
        "product"
    )
    .order_by("-activity_date")[:5]
    )
    

    monthly_data = (
        Harvest.objects
        .annotate(month=TruncMonth("harvest_date"))
        .values("month")
        .annotate(total=Sum("quantity_kg"))
        .order_by("month")
    )

    month_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_data
    ]

    month_totals = [
        float(item["total"])
        for item in monthly_data
    ]

    recent_farmers = Farmer.objects.order_by("-id")[:5]

    

    context = {
        "farmers": farmers,
        "crops": crops,
        "greenhouses": greenhouses,
        "harvests": harvests,
        "total_harvest": total_harvest,
        "average_harvest": average_harvest,
        "recent_harvests": recent_harvests,

        "crop_labels": json.dumps(crop_labels),
        "crop_totals": json.dumps(crop_totals),

        "greenhouse_labels": json.dumps(greenhouse_labels),
        "greenhouse_totals": json.dumps(greenhouse_totals),
        "month_labels": json.dumps(month_labels),
        "month_totals": json.dumps(month_totals),
        "recent_farmers": recent_farmers,
        "active_cycles": active_cycles,
        "beds": beds,
        "nursery_batches": nursery_batches,
        "operations": operations,
        "products": products,
        "harvest_today": harvest_today,
        "recent_operations": recent_operations,
        "low_stock_products": low_stock_products,
        "inventory_value": inventory_value,
    }

    return render(request, "dashboard.html", context)


def harvest_list(request):

    harvests = (
        Harvest.objects
        .select_related(
            "production_cycle_bed__bed",
            "production_cycle_bed__production_cycle",
            "production_cycle_bed__production_cycle__greenhouse",
            "production_cycle_bed__production_cycle__crop_variety",
            "production_cycle_bed__production_cycle__crop_variety__crop",
            "harvest_grade",
            "harvested_by",
        )
        .order_by("-harvest_date")
    )

    total_harvest = harvests.aggregate(
        total=Coalesce(
            Sum("quantity_kg"),
            Decimal("0")
        )
    )["total"]

    context = {
        "harvests": harvests,
        "total_harvest": total_harvest,
    }

    return render(
        request,
        "production/harvest_list.html",
        context,
    )

def harvest_detail(request, pk):
    
    harvest = get_object_or_404(
        Harvest.objects
        .select_related(
            "production_cycle_bed__bed",
            "production_cycle_bed__production_cycle",
            "production_cycle_bed__production_cycle__greenhouse",
            "production_cycle_bed__production_cycle__crop_variety",
            "production_cycle_bed__production_cycle__crop_variety__crop",
            "harvest_grade",
            "harvested_by",
        ),
        pk=pk,
    )

    return render(
        request,
        "production/harvest_detail.html",
        {
            "harvest": harvest,
        },
    )
def reports(request):

    harvests = Harvest.objects.select_related(
        "production_cycle_bed",
        "production_cycle_bed__production_cycle",
        "production_cycle_bed__production_cycle__crop_variety",
        "production_cycle_bed__production_cycle__crop_variety__crop",
    )

    total_harvest = (
        harvests.aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0")
            )
        )["total"]
    )

    average_harvest = (
        harvests.aggregate(
            avg=Coalesce(
                Avg("quantity_kg"),
                Decimal("0")
            )
        )["avg"]
    )

    total_records = harvests.count()

    top_crops = (
        harvests
        .values(
            "production_cycle_bed__production_cycle__crop_variety__crop__crop_name"
        )
        .annotate(
            total=Sum("quantity_kg")
        )
        .order_by("-total")
    )

    recent_harvests = harvests.order_by("-harvest_date")[:10]

    monthly_data = (
    Harvest.objects
    .annotate(month=TruncMonth("harvest_date"))
    .values("month")
    .annotate(total=Sum("quantity_kg"))
    .order_by("month")
    )

    month_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_data
    ]

    month_totals = [
        float(item["total"])
        for item in monthly_data
    ]

    context = {

        "total_harvest": total_harvest,
        "average_harvest": average_harvest,
        "total_records": total_records,
        "top_crops": top_crops,
        "recent_harvests": recent_harvests,
        "month_labels": json.dumps(month_labels),
        "month_totals": json.dumps(month_totals),

    }

    
    
    return render(
        request,
        "reports/dashboard.html",
    )

def farmer_list(request):

    search = request.GET.get("search", "")

    farmers = Farmer.objects.all()

    if search:
        farmers = farmers.filter(
            Q(farmer_name__icontains=search) |
            Q(location__icontains=search)
        )

    paginator = Paginator(farmers, 5)   # 5 farmers per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search": search,
    }

    return render(request, "farmers.html", context)




def export_harvest_excel(request):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Harvest Report"

    # Header row
    worksheet.append([
        "Date",
        "Farmer",
        "Crop",
        "Greenhouse",
        "Quantity (kg)"
    ])

    # Data rows
    harvests = Harvest.objects.select_related(
        "farmer",
        "crop",
        "greenhouse"
    )

    for harvest in harvests:
        worksheet.append([
            harvest.harvest_date.strftime("%Y-%m-%d"),
            harvest.farmer.farmer_name,
            harvest.crop.crop_name,
            harvest.greenhouse.greenhouse_name,
            float(harvest.quantity_kg),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="harvest_report.xlsx"'
    )

    workbook.save(response)

    return response


def production_cycle_list(request):

    cycles = (
        ProductionCycle.objects
        .select_related(
            "greenhouse",
            "crop_variety",
            "season"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "production/production_cycle_list.html",
        {
            "cycles": cycles
        }
    )



def production_cycle_detail(request, pk):
    
    operation_form = OperationLogForm()

    cycle = get_object_or_404(
        ProductionCycle.objects.select_related(
            "greenhouse",
            "crop_variety",
            "season",
            "nursery_batch",
        ),
        pk=pk,
    )

    beds = (
        ProductionCycleBed.objects
        .filter(production_cycle=cycle)
        .select_related("bed")
    )
    
    # operation_form.fields["production_cycle_bed"].queryset = beds
    # ==================================
    # SAVE OPERATION
    # ==================================
    if request.method == "POST":
    
        operation_form = OperationLogForm(request.POST)

        if operation_form.is_valid():

            operation = operation_form.save(commit=False)

            operation.production_cycle = cycle
            operation.greenhouse = cycle.greenhouse
            operation.performed_by = request.user
            operation.status = "Completed"

            # ===============================
            # CHECK SELECTED BEDS
            # ===============================

            selected_beds = request.POST.getlist("beds")

            if not selected_beds:

                messages.error(
                    request,
                    "Please select at least one bed."
                )

                return redirect(
                    "production_cycle_detail",
                    pk=cycle.pk
                )

            # -----------------------------
            # Calculate Product Cost
            # -----------------------------
            if operation.product and operation.quantity:

                operation.product_cost = (
                    operation.product.unit_cost *
                    operation.quantity
                )

                # Deduct stock only if required
                if operation.maintenance_type.deduct_inventory:

                    if operation.product.current_stock < operation.quantity:

                        messages.error(
                            request,
                            "Not enough stock available."
                        )

                        return redirect(
                            "production_cycle_detail",
                            pk=cycle.pk
                        )

                    operation.product.current_stock -= operation.quantity
                    operation.product.save()

            else:

                operation.product_cost = Decimal("0")

            operation.save()

            # Link selected beds
            for bed_id in selected_beds:

                OperationBed.objects.create(
                    operation=operation,
                    bed_id=bed_id,
                )

            messages.success(
                request,
                "Operation recorded successfully."
            )

            return redirect(
                "production_cycle_detail",
                pk=cycle.pk,
            )

            # --------------------------------
            # Save selected beds
            # --------------------------------

            selected_beds = request.POST.getlist("beds")

            for bed_id in selected_beds:

                OperationBed.objects.create(

                    operation=operation,

                    bed_id=bed_id,

                )

            messages.success(

                request,

                "Operation recorded successfully."

            )

            return redirect(

                "production_cycle_detail",

                pk=cycle.pk

            )

    else:

        operation_form = OperationLogForm()

    # ==================================
    # HARVESTS
    # ==================================

    harvests = (
        Harvest.objects
        .filter(
            production_cycle_bed__production_cycle=cycle
        )
        .select_related(
            "production_cycle_bed",
            "harvest_grade",
            "harvested_by",
        )
        .order_by("-harvest_date")
    )

    # ==================================
    # OPERATIONS
    # ==================================

    operations = (
        OperationLog.objects
        .filter(
            production_cycle=cycle
        )
        .select_related(
            "maintenance_type",
            "performed_by",
            "product",
        )
        .prefetch_related(
            "operation_beds__bed",
        )
        .order_by("-activity_date")
    )

    # ==================================
    # HARVEST SUMMARY
    # ==================================

    total_harvest = (
        harvests.aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0"),
            )
        )["total"]
    )

    # ==================================
    # COST SUMMARY
    # ==================================

    product_cost = Decimal("0")

    product_cost = operations.aggregate(
    total=Coalesce(
        Sum("product_cost"),
        Decimal("0")
    )
    )["total"]

    labour_cost = operations.aggregate(
        total=Coalesce(
            Sum("labour_cost"),
            Decimal("0")
        )
    )["total"]

    total_cost = product_cost + labour_cost
    # ==================================
    # CONTEXT
    # ==================================
    cycle_beds =(
        ProductionCycleBed.objects.filter(production_cycle =cycle)
        .select_related("bed")
    )
    context = {

        "cycle": cycle,

        "beds": beds,

        "harvests": harvests,

        "operations": operations,

        "operation_form": operation_form,

        "total_harvest": total_harvest,

        "product_cost": product_cost,

        "labour_cost": labour_cost,

        "total_cost": total_cost,
        "cycle_beds" : cycle_beds

    }

    return render(
        request,
        "production/production_cycle_detail.html",
        context,
    )
    

def operation_type_detail_api(request, pk):
    operation_type =get_object_or_404(
        Operation_type, pk=pk
    )

    data = {

        "requires_product": operation_type.requires_product,

        "requires_quantity": operation_type.requires_quantity,

        "requires_unit": operation_type.requires_unit,

        "requires_cost": operation_type.requires_cost,

        "requires_remarks": operation_type.requires_remarks,

    }

    return JsonResponse(data)


def inventory_dashboard(request):

    total_products = Product.objects.count()

    low_stock = (
        Product.objects.filter(
            current_stock__lte=F("minimum_stock")
        )
        .order_by("current_stock")
    )

    recent_receipts = (
        StockReceipt.objects
        .select_related(
            "product",
            "supplier",
            "received_by",
        )
        .order_by("-received_date")[:5]
    )

    recent_usage = (
        OperationLog.objects
        .select_related(
            "product",
            "performed_by",
            "maintenance_type",
        )
        .exclude(product=None)
        .order_by("-activity_date")[:5]
    )

    inventory_value = (
        Product.objects.aggregate(
            total=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F("current_stock") * F("unit_cost"),
                        output_field=DecimalField(
                            max_digits=15,
                            decimal_places=2
                        )
                    )
                ),
                Decimal("0")
            )
        )["total"]
    )

    context = {

        "total_products": total_products,
        "inventory_value": inventory_value,
        "low_stock": low_stock,
        "recent_receipts": recent_receipts,
        "recent_usage": recent_usage,

    }

    return render(
        request,
        "inventory/dashboard.html",
        context
    )


def reports_dashboard(request):
    
    return render(
        request,
        "reports/dashboard.html"
    )


def harvest_report(request):
    
    harvests = (
        Harvest.objects
        .select_related(
            "production_cycle_bed",
            "production_cycle_bed__production_cycle",
            "production_cycle_bed__production_cycle__crop_variety",
            "production_cycle_bed__production_cycle__crop_variety__crop",
            "production_cycle_bed__production_cycle__greenhouse",
            "harvest_grade",
            "harvested_by",
        )
        .order_by("-harvest_date")
    )

    total_harvest = (
        harvests.aggregate(
            total=Sum("quantity_kg")
        )["total"] or 0
    )

    return render(
        request,
        "reports/harvest_report.html",
        {
            "harvests": harvests,
            "total_harvest": total_harvest,
        }
    )

def stock_ledger(request):
    
    receipts = (
        StockReceipt.objects
        .select_related(
            "product",
            "supplier",
            "received_by",
        )
    )

    operations = (
        OperationLog.objects
        .filter(product__isnull=False)
        .select_related(
            "product",
            "performed_by",
            "maintenance_type",
        )
    )

    ledger = []

    # Stock IN
    for receipt in receipts:

        ledger.append({

            "date": receipt.received_date,

            "product": receipt.product,

            "type": "Receipt",

            "quantity": receipt.quantity,

            "user": receipt.received_by,

            "reference": receipt.supplier,

            "movement": "IN",

        })

    # Stock OUT
    for operation in operations:

        ledger.append({

            "date": operation.activity_date,

            "product": operation.product,

            "type": operation.maintenance_type,

            "quantity": operation.quantity,

            "user": operation.performed_by,

            "reference": operation.production_cycle,

            "movement": "OUT",

        })

    ledger.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return render(
        request,
        "inventory/stock_ledger.html",
        {
            "ledger": ledger
        }
    )

def greenhouse_list(request):
    
    greenhouses = (
        Greenhouse.objects
        .all()
        .order_by("greenhouse_name")
    )

    return render(
        request,
        "greenhouse/greenhouse_list.html",
        {
            "greenhouses": greenhouses,
        }
    )



def greenhouse_detail(request, pk):

    greenhouse = get_object_or_404(
        Greenhouse,
        pk=pk
    )

    cycles = (
        ProductionCycle.objects
        .filter(greenhouse=greenhouse)
        .select_related(
            "crop_variety",
            "crop_variety__crop",
            "season",
        )
        .order_by("-created_at")
    )

    total_cycles = cycles.count()

    active_cycles = (
        cycles
        .exclude(status="Completed")
        .count()
    )

    bays = (
        Bay.objects
        .filter(greenhouse=greenhouse)
        .prefetch_related(
            Prefetch(
                "beds",
                queryset=Bed.objects.prefetch_related(
                    "production_cycles",
                    "operations",
                )
            )
        )
    )

    total_beds = Bed.objects.filter(
        bay__greenhouse=greenhouse
    ).count()

    total_harvest = (
        Harvest.objects
        .filter(
            production_cycle_bed__production_cycle__greenhouse=greenhouse
        )
        .aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0")
            )
        )["total"]
    )

    operations = (
        OperationLog.objects
        .filter(
            greenhouse=greenhouse
        )
        .select_related(
            "maintenance_type",
            "performed_by",
            "production_cycle",
            "product",
        )
        .prefetch_related(
            "operation_beds__bed",
        )
        .order_by("-activity_date")
    )

    product_cost = (
        operations.aggregate(
            total=Coalesce(
                Sum("product_cost"),
                Decimal("0")
            )
        )["total"]
    )

    labour_cost = (
        operations.aggregate(
            total=Coalesce(
                Sum("labour_cost"),
                Decimal("0")
            )
        )["total"]
    )

    total_cost = product_cost + labour_cost

    context = {
        "greenhouse": greenhouse,
        "cycles": cycles,
        "bays": bays,
        "total_cycles": total_cycles,
        "active_cycles": active_cycles,
        "total_beds": total_beds,
        "total_harvest": total_harvest,
        "operations": operations,
        "product_cost": product_cost,
        "labour_cost": labour_cost,
        "total_cost": total_cost,
    }

    return render(
        request,
        "greenhouse/greenhouse_detail.html",
        context,
    )
def greenhouse_performance(request, pk):
    
    greenhouse = get_object_or_404(
        Greenhouse,
        pk=pk
    )

    cycles = (
        ProductionCycle.objects
        .filter(greenhouse=greenhouse)
    )

    total_cycles = cycles.count()

    active_cycles = (
        cycles
        .exclude(status="Completed")
        .count()
    )

    total_beds = (
        ProductionCycleBed.objects
        .filter(
            production_cycle__greenhouse=greenhouse
        )
        .count()
    )

    total_operations = (
        OperationLog.objects
        .filter(
            production_cycle_bed__production_cycle__greenhouse=greenhouse
        )
        .count()
    )

    total_harvest = (
        Harvest.objects
        .filter(
            production_cycle_bed__production_cycle__greenhouse=greenhouse
        )
        .aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0")
            )
        )["total"]
    )

    average_harvest = (
        Harvest.objects
        .filter(
            production_cycle_bed__production_cycle__greenhouse=greenhouse
        )
        .aggregate(
            avg=Coalesce(
                Avg("quantity_kg"),
                Decimal("0")
            )
        )["avg"]
    )

    monthly_harvest = (
    Harvest.objects
    .filter(
        production_cycle_bed__production_cycle__greenhouse=greenhouse
    )
    .annotate(month=TruncMonth("harvest_date"))
    .values("month")
    .annotate(total=Sum("quantity_kg"))
    .order_by("month")
    )

    month_labels = [
        item["month"].strftime("%b %Y")
        for item in monthly_harvest
    ]

    month_totals = [
        float(item["total"])
        for item in monthly_harvest
    ]
    context = {

        "greenhouse": greenhouse,

        "total_cycles": total_cycles,

        "active_cycles": active_cycles,

        "total_beds": total_beds,

        "total_operations": total_operations,

        "total_harvest": total_harvest,

        "average_harvest": average_harvest,
        "month_labels": json.dumps(month_labels),
        "month_totals": json.dumps(month_totals),

    }

    return render(
        request,
        "greenhouse/performance.html",
        context
    )



# @login_required
def operation_list(request):

    operations = (
        OperationLog.objects
        .select_related(
            "production_cycle",
            "maintenance_type",
            "performed_by",
        )
        .order_by("-activity_date")
    )

    total_operations = operations.count()

    total_product_cost = operations.aggregate(
        total=Coalesce(
            Sum("product_cost"),
            Decimal("0")
        )
    )["total"]

    total_labour_cost = operations.aggregate(
        total=Coalesce(
            Sum("labour_cost"),
            Decimal("0")
        )
    )["total"]

    context = {
        "operations": operations,
        "total_operations": total_operations,
        "total_product_cost": total_product_cost,
        "total_labour_cost": total_labour_cost,
    }

    return render(
        request,
        "operations/operation_list.html",
        context,
    )

def production_cycle_performance(request, pk):

    cycle = get_object_or_404(
        ProductionCycle,
        pk=pk
    )

    beds = (
        ProductionCycleBed.objects
        .filter(production_cycle=cycle)
    )

    total_beds = beds.count()

    total_plants = beds.aggregate(
        total=Coalesce(
            Sum("transplanted_seedlings"),
            0
        )
    )["total"]

    total_harvest = (
        Harvest.objects
        .filter(
            production_cycle_bed__production_cycle=cycle
        )
        .aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0")
            )
        )["total"]
    )

    operations = (
        OperationLog.objects
        .filter(
            production_cycle=cycle
        )
    )

    product_cost = operations.aggregate(
        total=Coalesce(
            Sum("product_cost"),
            Decimal("0")
        )
    )["total"]

    labour_cost = operations.aggregate(
        total=Coalesce(
            Sum("labour_cost"),
            Decimal("0")
        )
    )["total"]

    total_cost = product_cost + labour_cost

    yield_per_bed = (
        total_harvest / total_beds
        if total_beds else 0
    )

    yield_per_plant = (
        total_harvest / total_plants
        if total_plants else 0
    )

    cost_per_kg = (
        total_cost / total_harvest
        if total_harvest else 0
    )

    context = {
        "cycle": cycle,
        "total_beds": total_beds,
        "total_plants": total_plants,
        "total_harvest": total_harvest,
        "product_cost": product_cost,
        "labour_cost": labour_cost,
        "total_cost": total_cost,
        "yield_per_bed": yield_per_bed,
        "yield_per_plant": yield_per_plant,
        "cost_per_kg": cost_per_kg,
    }

    return render(
        request,
        "production/production_cycle_performance.html",
        context,
    )


def bed_performance(request, pk):

    bed = get_object_or_404(
        Bed.objects.select_related(
            "bay",
            "bay__greenhouse",
        ),
        pk=pk,
    )

    cycles = (
        ProductionCycleBed.objects
        .filter(bed=bed)
        .select_related(
            "production_cycle",
            "production_cycle__crop_variety",
            "production_cycle__crop_variety__crop",
        )
        .order_by("-transplant_date")
    )

    harvests = (
        Harvest.objects
        .filter(
            production_cycle_bed__bed=bed
        )
    )

    operations = (
        OperationLog.objects
        .filter(
            operation_beds__bed=bed
        )
        .select_related(
            "maintenance_type",
            "performed_by",
            "product",
        )
        .distinct()
        .order_by("-activity_date")
    )

    total_harvest = (
        harvests.aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0"),
            )
        )["total"]
    )

    product_cost = (
        operations.aggregate(
            total=Coalesce(
                Sum("product_cost"),
                Decimal("0"),
            )
        )["total"]
    )

    labour_cost = (
        operations.aggregate(
            total=Coalesce(
                Sum("labour_cost"),
                Decimal("0"),
            )
        )["total"]
    )

    total_cost = product_cost + labour_cost

    total_operations = operations.count()

    total_harvests = harvests.count()

    context = {

        "bed": bed,

        "cycles": cycles,

        "operations": operations,

        "harvests": harvests,

        "total_harvest": total_harvest,

        "product_cost": product_cost,

        "labour_cost": labour_cost,

        "total_cost": total_cost,

        "total_operations": total_operations,

        "total_harvests": total_harvests,

    }

    return render(
        request,
        "production/bed_performance.html",
        context,
    )


def operation_type_fields(request, pk):

    operation_type = get_object_or_404(
        OperationType,
        pk=pk,
    )

    return render(
        request,
        "production/partials/operation_fields.html",
        {
            "operation_type": operation_type,
        },
    )

def operation_detail(request, pk):
    
    operation = get_object_or_404(
        OperationLog.objects
        .select_related(
            "greenhouse",
            "production_cycle",
            "maintenance_type",
            "performed_by",
            "product",
        )
        .prefetch_related(
            "operation_beds__bed",
        ),
        pk=pk,
    )

    return render(
        request,
        "production/operation_detail.html",
        {
            "operation": operation,
        },
    )

def nursery_batch_list(request):
    
    batches = (
        NurseryBatch.objects
        .select_related(
            "crop_variety",
            "crop_variety__crop",
            "season",
        )
        .order_by("-sowing_date")
    )

    return render(
        request,
        "nursery/nursery_batch_list.html",
        {
            "batches": batches,
        },
    )

def nursery_batch_detail(request, pk):

    batch = get_object_or_404(
        NurseryBatch.objects.select_related(
            "crop_variety",
            "crop_variety__crop",
            "season",
        ),
        pk=pk,
    )

    production_cycles = (
        ProductionCycle.objects
        .filter(
            nursery_batch=batch
        )
        .select_related(
            "greenhouse"
        )
    )

    context = {

        "batch": batch,

        "production_cycles": production_cycles,

    }

    return render(
        request,
        "nursery/nursery_batch_detail.html",
        context,
    )


from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from decimal import Decimal


def harvest_report(request):

    harvests = (
        Harvest.objects
        .select_related(
            "production_cycle_bed__production_cycle",
            "production_cycle_bed__bed",
            "harvest_grade",
            "harvested_by",
        )
        .order_by("-harvest_date")
    )

    total_harvest = harvests.aggregate(
        total=Coalesce(
            Sum("quantity_kg"),
            Decimal("0")
        )
    )["total"]

    average_harvest = harvests.aggregate(
        avg=Coalesce(
            Avg("quantity_kg"),
            Decimal("0")
        )
    )["avg"]

    context = {

        "harvests": harvests,

        "total_harvest": total_harvest,

        "average_harvest": average_harvest,

        "total_records": harvests.count(),

    }

    return render(
        request,
        "reports/harvest_report.html",
        context,
    )

def inventory_report(request):
    
    products = (
        Product.objects
        .all()
        .order_by("product_name")
    )

    inventory_value = (
        Product.objects.aggregate(
            total=Coalesce(
                Sum(
                    F("current_stock") * F("unit_cost"),
                    output_field=DecimalField(
                        max_digits=15,
                        decimal_places=2,
                    ),
                ),
                Decimal("0"),
            )
        )["total"]
    )

    low_stock = (
        products.filter(
            current_stock__lte=F("minimum_stock")
        ).count()
    )

    context = {

        "products": products,

        "inventory_value": inventory_value,

        "low_stock": low_stock,

        "total_products": products.count(),

    }

    return render(
        request,
        "reports/inventory_report.html",
        context,
    )

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from decimal import Decimal


def production_report(request):

    cycles = (
        ProductionCycle.objects
        .select_related(
            "greenhouse",
            "crop_variety",
            "crop_variety__crop",
            "season",
        )
        .annotate(

            total_harvest=Coalesce(
                Sum(
                    "cycle_beds__harvests__quantity_kg"
                ),
                Decimal("0")
            ),

            total_operations=Count(
                "operations",
                distinct=True
            ),

        )
        .order_by("-created_at")
    )

    total_cycles = cycles.count()

    active_cycles = cycles.exclude(
        status="Completed"
    ).count()

    completed_cycles = cycles.filter(
        status="Completed"
    ).count()

    total_harvest = cycles.aggregate(

        total=Coalesce(
            Sum("total_harvest"),
            Decimal("0")
        )

    )["total"]

    context = {

        "cycles": cycles,

        "total_cycles": total_cycles,

        "active_cycles": active_cycles,

        "completed_cycles": completed_cycles,

        "total_harvest": total_harvest,

    }

    return render(

        request,

        "reports/production_report.html",

        context,

    )