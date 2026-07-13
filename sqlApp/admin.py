from django.contrib import admin
from . models import *

# Register your models here.
admin.site.site_header ="SCL Greenhouse Management System"
admin.site.site_title ="SCL Admin"
admin.site.index_title ="Administration"
admin.site.register([Farmer, ProductionCycleSummary])

@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):

    list_display = (
        "bay_code",
        "bay_name",
        "greenhouse",
        "number_of_beds",
        "created_at",
    )

    list_filter = (
        "greenhouse",
    )

    search_fields = (
        "bay_code",
        "bay_name",
        "greenhouse__greenhouse_name",
        "greenhouse__greenhouse_code",
    )

    ordering = (
        "greenhouse",
        "bay_code",
    )

    autocomplete_fields = (
        "greenhouse",
    )

    readonly_fields = (
        "created_at",
    )
@admin.register(Greenhouse)
class GreenhouseAdmin(admin.ModelAdmin):

    list_display = (
        "greenhouse_code",
        "greenhouse_name",
        "greenhouse_type",
        "status",
        "location",
    )

    list_filter = (
        "greenhouse_type",
        "status",
    )

    search_fields = (
        "greenhouse_code",
        "greenhouse_name",
        "location",
    )

    ordering = (
        "greenhouse_code",
    )


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):

    list_display = (
        "bed_code",
        "bed_name",
        "bay",
        "capacity",
        "status",
    )

    list_filter = (
        "bay",
        "status",
    )

    search_fields = (
        "bed_code",
        "bed_name",
    )

    ordering = (
        "bay",
        "bed_code",
    )

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):

    list_display = (
        "crop_name",
        "scientific_name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "crop_name",
        "scientific_name",
    )


@admin.register(CropVariety)
class CropVarietyAdmin(admin.ModelAdmin):

    list_display = (
        "variety_name",
        "crop",
        "expected_yield_per_plant",
        "maturity_days",
    )

    list_filter = (
        "crop",
        "is_active",
    )

    search_fields = (
        "variety_name",
        "crop__crop_name",
    )

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):

    list_display = (
        "season_name",
        "season_type",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "season_type",
        "is_active",
    )

    search_fields = (
        "season_name",
    )

@admin.register(ProductionCycle)
class ProductionCycleAdmin(admin.ModelAdmin):

    list_display = (
        "cycle_number",
        "greenhouse",
        "crop_variety",
        "status",
        "beds_used_display",
        "seedlings_display",
        "harvest_display",
        "yield_display",
    )

    autocomplete_fields = (
        "greenhouse",
        "season",
        "crop_variety",
        "nursery_batch",
        "responsible_staff",
    )

    search_fields = (
        "cycle_number",
        "crop_variety__variety_name",
    )

    list_filter = (
        "greenhouse",
        "status",
        "season",
    )

    def beds_used_display(self, obj):
        return obj.beds_used

    beds_used_display.short_description = "Beds"

    def seedlings_display(self, obj):
        return obj.total_seedlings

    seedlings_display.short_description = "Plants"

    def harvest_display(self, obj):
        return obj.total_harvest_kg

    harvest_display.short_description = "Harvest (kg)"

    def yield_display(self, obj):
        return obj.yield_per_plant

    yield_display.short_description = "Kg / Plant"

@admin.register(ProductionCycleBed)
class ProductionCycleBedAdmin(admin.ModelAdmin):

    list_display = (
        "production_cycle",
        "bed",
        "transplanted_seedlings",
        "status",
        "transplant_date",
    )

    list_filter = (
        "status",
        "production_cycle__season",
        "bed__bay",
    )

    search_fields = (
        "production_cycle__cycle_number",
        "bed__bed_code",
    )

    autocomplete_fields = (
        "production_cycle",
        "bed",
    )

@admin.register(HarvestGrade)
class HarvestGradeAdmin(admin.ModelAdmin):

    list_display = (
        "grade_code",
        "grade_name",
        "is_marketable",
    )

    list_filter = (
        "is_marketable",
    )

    search_fields = (
        "grade_code",
        "grade_name",
    )

@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):

    list_display = (
        "harvest_date",
        "production_cycle_bed",
        "harvest_grade",
        "quantity_kg",
        "crates",
        "harvested_by",
    )

    list_filter = (
        "harvest_grade",
        "harvest_date",
        "production_cycle_bed__production_cycle__season",
    )

    search_fields = (
        "production_cycle_bed__production_cycle__cycle_number",
        "production_cycle_bed__bed__bed_code",
    )

    autocomplete_fields = (
        "production_cycle_bed",
        "harvest_grade",
        "harvested_by",
    )

@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):

    list_display = (
        "maintenance_name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "maintenance_name",
    )

@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):

    list_display = (
        "activity_date",
        "maintenance_type",
        "production_cycle",
        "performed_by",
        "quantity",
        "unit",
        "product_cost",
        "labour_cost",
    )

    list_filter = (
        "maintenance_type",
        "activity_date",
    )

    search_fields = (
        "production_cycle__production_cycle__cycle_number",
        "maintenance_type__maintenance_name",
    )

    autocomplete_fields = (
        "production_cycle",
        "maintenance_type",
        "performed_by",
    )
    list_display = (
    "activity_date",
    "maintenance_type",
    "product",
    "production_cycle",
    "performed_by",
    "quantity",
    "unit",
    "product_cost",
    "labour_cost",
    )
    autocomplete_fields = (
    "production_cycle",
    "maintenance_type",
    "performed_by",
    "product",
)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "product_code",
        "product_name",
        "category",
        "brand",
        "unit",
        "unit_cost",
        "minimum_stock",
        "is_active",
    )

    list_filter = (
        "category",
        "unit",
        "is_active",
    )

    search_fields = (
        "product_code",
        "product_name",
        "brand",
    )

    ordering = (
        "product_name",
    )

    autocomplete_fields = (
        "category",
    )


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_date",
        "product",
        "transaction_type",
        "quantity",
        "unit_cost",
        "performed_by",
    )

    list_filter = (
        "transaction_type",
        "transaction_date",
    )

    search_fields = (
        "product__product_name",
        "reference",
    )

    autocomplete_fields = (
        "product",
        "performed_by",
    )

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "category_name",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "category_name",
    )


@admin.register(ProductionEvent)
class ProductionEventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "production_cycle",
        "event_date",
        "priority",
        "status",
        "assigned_to",
    )

    list_filter = (
        "status",
        "priority",
        "event_date",
    )

    search_fields = (
        "title",
        "production_cycle__cycle_number",
    )

    autocomplete_fields = (
        "production_cycle",
        "assigned_to",
    )

@admin.register(ProductionSOP)
class ProductionSOPAdmin(admin.ModelAdmin):

    list_display = (
        "crop_variety",
        "version",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "crop_variety__variety_name",
    )


@admin.register(SOPActivity)
class SOPActivityAdmin(admin.ModelAdmin):

    list_display = (
        "activity_name",
        "sop",
        "day_after_sowing",
        "frequency",
        "priority",
    )

    list_filter = (
        "frequency",
        "priority",
    )
    search_fields = (
    "activity_name",
    "sop__sop_name",
    "sop__crop_variety__variety_name",
    )

    autocomplete_fields = (
        "sop",
        "maintenance_type",
    )

@admin.register(ActivityResource)
class ActivityResourceAdmin(admin.ModelAdmin):

    list_display = (
        "sop_activity",
        "resource_type",
        "product",
        "resource_name",
        "quantity",
        "unit",
        "estimated_cost",
    )

    list_filter = (
        "resource_type",
    )

    search_fields = (
        "resource_name",
        "product__product_name",
    )

    autocomplete_fields = (
        "sop_activity",
        "product",
    )

@admin.register(Pest)
class PestAdmin(admin.ModelAdmin):

    list_display = (
        "pest_name",
        "scientific_name",
        "is_active",
    )

    search_fields = (
        "pest_name",
        "scientific_name",
    )


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):

    list_display = (
        "disease_name",
        "scientific_name",
        "is_active",
    )

    search_fields = (
        "disease_name",
        "scientific_name",
    )


@admin.register(Scouting)
class ScoutingAdmin(admin.ModelAdmin):

    list_display = (
        "scouting_date",
        "production_cycle_bed",
        "pest",
        "disease",
        "severity",
        "affected_plants",
        "observed_by",
    )

    list_filter = (
        "severity",
        "scouting_date",
    )

    autocomplete_fields = (
        "production_cycle_bed",
        "pest",
        "disease",
        "observed_by",
    )

@admin.register(PackingBatch)
class PackingBatchAdmin(admin.ModelAdmin):

    list_display = (
        "packing_date",
        "harvest",
        "package_type",
        "number_of_packages",
        "total_weight",
        "status",
    )

    list_filter = (
        "status",
        "packing_date",
    )

    autocomplete_fields = (
        "harvest",
        "packed_by",
    )

@admin.register(NurseryBatch)
class NurseryBatchAdmin(admin.ModelAdmin):

    list_display = (
        "batch_number",
        "crop_variety",
        "season",
        "sowing_date",
        "expected_germination_date",
        "expected_transplant_date",
        "seeds_sown",
        "trays_used",
        "status",
    )

    list_filter = (
        "status",
        "season",
        "crop_variety",
    )

    search_fields = (
        "batch_number",
        "crop_variety__variety_name",
        "crop_variety__crop__crop_name",
    )

    ordering = (
        "-sowing_date",
    )

    autocomplete_fields = (
        "crop_variety",
        "season",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):

    list_display = (
        "supplier_code",
        "supplier_name",
        "contact_person",
        "phone",
        "is_active",
    )

    search_fields = (
        "supplier_code",
        "supplier_name",
        "contact_person",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "supplier_name",
    )

@admin.register(StockReceipt)
class StockReceiptAdmin(admin.ModelAdmin):

    list_display = (
        "received_date",
        "product",
        "supplier",
        "quantity",
        "received_by",
    )

    search_fields = (
        "product__product_name",
        "supplier__supplier_name",
    )

    autocomplete_fields = (
        "product",
        "supplier",
        "received_by",
    )

    list_filter = (
        "received_date",
        "supplier",
    )

    date_hierarchy = "received_date"

    ordering = (
        "-received_date",
    )

    def get_readonly_fields(self, request, obj=None):

        if obj:

            return (
                "product",
                "supplier",
                "quantity",
                "received_date",
                "received_by",
                "remarks",
            )

        return ()

@admin.register(OperationBed)
class OperationBedAdmin(admin.ModelAdmin):

    list_display = (
        "operation",
        "bed",
    )

    search_fields = (
        "operation__operation_number",
        "bed__bed_code",
    )