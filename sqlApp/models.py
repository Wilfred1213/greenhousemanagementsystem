from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Sum
from decimal import Decimal
from django.db import transaction

# Create your models here.


class Farmer(models.Model):
    farmer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.farmer_name

class Crop(models.Model):
    
    crop_name = models.CharField(
        max_length=100,
        unique=True
    )

    scientific_name = models.CharField(
        max_length=150,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        default =timezone.now
    )

    class Meta:
        ordering = ["crop_name"]

    def __str__(self):
        return self.crop_name

class CropVariety(models.Model):
    
    crop = models.ForeignKey(
        Crop,
        on_delete=models.CASCADE,
        related_name="varieties"
    )

    variety_name = models.CharField(
        max_length=100
    )

    expected_yield_per_plant = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Expected yield (kg) per plant."
    )

    maturity_days = models.PositiveIntegerField(
        help_text="Days from transplant to first harvest."
    )

    plant_spacing_cm = models.PositiveIntegerField()

    row_spacing_cm = models.PositiveIntegerField()

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = [
            "crop",
            "variety_name"
        ]

        unique_together = (
            "crop",
            "variety_name",
        )

    def __str__(self):
        return f"{self.crop.crop_name} - {self.variety_name}"


class Greenhouse(models.Model):

    GREENHOUSE_TYPES = [
        ("Tunnel", "Tunnel"),
        ("Gothic", "Gothic"),
        ("Multi-Span", "Multi-Span"),
        ("Shade Net", "Shade Net"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Maintenance", "Maintenance"),
        ("Inactive", "Inactive"),
    ]

    greenhouse_code = models.CharField(max_length=20, unique=True, help_text="Example: GH001", null =True)

    greenhouse_name = models.CharField(max_length=100)

    location = models.CharField(max_length=200, blank=True)

    greenhouse_type = models.CharField(max_length=20, choices=GREENHOUSE_TYPES, default="Tunnel")

    length_m = models.DecimalField(max_digits=6, decimal_places=2, null =True)

    width_m = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    status = models.CharField( max_length=20, choices=STATUS_CHOICES,
        default="Active"
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def area(self):
        if self.length_m and self.width_m:
            return self.length_m * self.width_m
        return 0

    def __str__(self):
        return f"{self.greenhouse_code} - {self.greenhouse_name}"


class Harvest(models.Model):

    production_cycle_bed = models.ForeignKey(
        "ProductionCycleBed",
        on_delete=models.PROTECT,
        related_name="harvests",
        
    )

    harvest_grade = models.ForeignKey(
        "HarvestGrade",
        on_delete=models.PROTECT,
        related_name="harvests",
        null=True
    )

    harvest_date = models.DateField()

    quantity_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    crates = models.PositiveIntegerField(
        default=0
    )

    average_fruit_weight_g = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    harvested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="harvest_records",
        null = True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ["-harvest_date"]

    def __str__(self):
        return (
            f"{self.production_cycle_bed.production_cycle.cycle_number} "
            f"- {self.harvest_date}"
        )
    @property
    def production_cycle(self):
        return self.production_cycle_bed.production_cycle


    @property
    def crop_variety(self):
        return self.production_cycle.crop_variety


    @property
    def crop(self):
        return self.crop_variety.crop


    @property
    def greenhouse(self):
        return self.production_cycle.greenhouse


    @property
    def bed(self):
        return self.production_cycle_bed.bed



class Season(models.Model):

    SEASON_TYPES = [
        ("Rainy", "Rainy"),
        ("Dry", "Dry"),
        ("Special", "Special"),
    ]

    season_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Example: 2026 Dry Season"
    )

    season_type = models.CharField(
        max_length=20,
        choices=SEASON_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError(
                "End date must be after the start date."
            )

    def __str__(self):
        return self.season_name



class ProductionCycle(models.Model):

    STATUS_CHOICES = [
        ("Planning", "Planning"),
        ("Nursery", "Nursery"),
        ("Ready for Transplant", "Ready for Transplant"),
        ("Growing", "Growing"),
        ("Harvesting", "Harvesting"),
        ("Completed", "Completed"),
        ("Archived", "Archived"),
    ]

    cycle_number = models.CharField(
        max_length=30,
        unique=True,
        help_text="Example: PC-2026-001"
    )
    greenhouse = models.ForeignKey(
    Greenhouse,
    on_delete=models.PROTECT,
    related_name="production_cycles",
    null =True
)

    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="production_cycles"
    )

    crop_variety = models.ForeignKey(
        CropVariety,
        on_delete=models.PROTECT,
        related_name="production_cycles"
    )

    responsible_staff = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="production_cycles"
    )

    nursery_batch = models.ForeignKey(
    "NurseryBatch",
    on_delete=models.PROTECT,
    related_name="production_cycles"
    )

    nursery_date = models.DateField()

    expected_transplant_date = models.DateField()

    actual_transplant_date = models.DateField(
        null=True,
        blank=True
    )

    expected_first_harvest = models.DateField(
        null=True,
        blank=True
    )

    expected_last_harvest = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Planning"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def total_seedlings(self):
        return sum(
            bed.transplanted_seedlings
            for bed in self.cycle_beds.all()
        )


    @property
    def total_harvest_kg(self):
        result = Harvest.objects.filter(
            production_cycle_bed__production_cycle=self
        ).aggregate(
            total=Coalesce(
                Sum("quantity_kg"),
                Decimal("0.00")
            )
        )

        return result["total"]


    @property
    def total_crates(self):
        result = Harvest.objects.filter(
            production_cycle_bed__production_cycle=self
        ).aggregate(
            total=Coalesce(
                Sum("crates"),
                0
            )
        )

        return result["total"]


    @property
    def beds_used(self):
        return self.cycle_beds.count()


    @property
    def yield_per_plant(self):

        if self.total_seedlings == 0:
            return 0

        return round(
            self.total_harvest_kg / self.total_seedlings,
            2
        )


    @property
    def yield_per_bed(self):

        if self.beds_used == 0:
            return 0

        return round(
            self.total_harvest_kg / self.beds_used,
            2
        )

    def __str__(self):
        return self.cycle_number

class ProductionCycleBed(models.Model):
    
    STATUS_CHOICES = [
        ("Planned", "Planned"),
        ("Transplanted", "Transplanted"),
        ("Growing", "Growing"),
        ("Harvesting", "Harvesting"),
        ("Completed", "Completed"),
    ]

    production_cycle = models.ForeignKey(
        ProductionCycle,
        on_delete=models.CASCADE,
        related_name="cycle_beds"
    )

    bed = models.ForeignKey(
        "Bed",
        on_delete=models.PROTECT,
        related_name="production_cycles"
    )

    transplanted_seedlings = models.PositiveIntegerField()

    transplant_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Planned"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "production_cycle",
            "bed"
        ]

        unique_together = (
            "production_cycle",
            "bed",
        )

    def __str__(self):
        return f"{self.production_cycle.cycle_number} - {self.bed.bed_code}"

class HarvestGrade(models.Model):
    
    grade_code = models.CharField(
        max_length=10,
        unique=True
    )

    grade_name = models.CharField(
        max_length=50
    )

    description = models.TextField(
        blank=True
    )

    is_marketable = models.BooleanField(
        default=True,
        help_text="Can this grade be sold?"
    )

    created_at = models.DateTimeField(
        default =timezone.now
    )

    class Meta:
        ordering = ["grade_code"]

    def __str__(self):
        return self.grade_name

class OperationType(models.Model):
    
    maintenance_name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    # --------------------------
    # Form Behaviour
    # --------------------------

    requires_product = models.BooleanField(
        default=False
    )

    requires_quantity = models.BooleanField(
        default=False
    )

    requires_unit = models.BooleanField(
        default=False
    )

    requires_cost = models.BooleanField(
        default=False
    )

    requires_remarks = models.BooleanField(
        default=False
    )

    # --------------------------
    # Inventory
    # --------------------------

    deduct_inventory = models.BooleanField(
        default=False,
        help_text="Should this operation reduce inventory?"
    )

    # --------------------------
    # Production
    # --------------------------

    affects_crop = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["maintenance_name"]

    def __str__(self):

        return self.maintenance_name

class OperationLog(models.Model):
    
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    APPLY_TO_CHOICES = [
        ("BEDS", "Selected Beds"),
        ("BAY", "Entire Bay"),
        ("GREENHOUSE", "Entire Greenhouse"),
    ]

    operation_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    production_cycle = models.ForeignKey(
        ProductionCycle,
        on_delete=models.PROTECT,
        related_name="operations",
    )

    greenhouse = models.ForeignKey(
        Greenhouse,
        on_delete=models.PROTECT,
    )

    bay = models.ForeignKey(
        "Bay",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    apply_to = models.CharField(
        max_length=20,
        choices=APPLY_TO_CHOICES,
        default="BEDS",
    )

    maintenance_type = models.ForeignKey(
        OperationType,
        on_delete=models.PROTECT,
    )

    activity_date = models.DateField()

    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    unit = models.CharField(
        max_length=20,
        blank=True,
    )

    product_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    labour_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Completed",
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-activity_date", "-id"]

    from django.db import transaction
    def save(self, *args, **kwargs):
    
        if not self.operation_number:

            last = (
                OperationLog.objects
                .order_by("-id")
                .first()
            )

            if last and last.operation_number:

                number = int(last.operation_number[2:]) + 1

            else:

                number = 1

            self.operation_number = f"OP{number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.operation_number} - {self.maintenance_type}"

class OperationBed(models.Model):
    
    operation = models.ForeignKey(
        OperationLog,
        on_delete=models.CASCADE,
        related_name="operation_beds",
    )

    bed = models.ForeignKey(
        "Bed",
        on_delete=models.PROTECT,
        related_name="operations",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "operation",
            "bed",
        )

    def __str__(self):
        return f"{self.operation} - {self.bed}"

class ProductCategory(models.Model):
    
    category_name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["category_name"]

    def __str__(self):
        return self.category_name

class Product(models.Model):
    
    UNIT_CHOICES = [
        ("kg", "Kilogram"),
        ("g", "Gram"),
        ("L", "Litre"),
        ("ml", "Millilitre"),
        ("pcs", "Pieces"),
        ("bags", "Bags"),
        ("packs", "Packs"),
        ("bottles", "Bottles"),
    ]

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products"
    )

    product_code = models.CharField(
        max_length=30,
        unique=True
    )

    product_name = models.CharField(
        max_length=200
    )

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    minimum_stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    current_stock = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    help_text="Current quantity available in inventory."
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return f"{self.product_code} - {self.product_name}"


class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = [
        ("Purchase", "Purchase"),
        ("Issue", "Issue"),
        ("Return", "Return"),
        ("Adjustment", "Adjustment"),
        ("Transfer", "Transfer"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_date = models.DateField()

    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Purchase Order, Production Cycle, Invoice, etc."
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="inventory_transactions"
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.product.product_name} ({self.transaction_type})"


class NurseryBatch(models.Model):
    
    STATUS_CHOICES = [
        ("Seeded", "Seeded"),
        ("Germinating", "Germinating"),
        ("Ready", "Ready for Transplant"),
        ("Completed", "Completed"),
    ]

    batch_number = models.CharField(
        max_length=30,
        unique=True
    )

    crop_variety = models.ForeignKey(
        CropVariety,
        on_delete=models.PROTECT,
        related_name="nursery_batches"
    )

    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="nursery_batches"
    )

    sowing_date = models.DateField()

    expected_germination_date = models.DateField()

    expected_transplant_date = models.DateField()

    seeds_sown = models.PositiveIntegerField()

    trays_used = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Seeded"
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-sowing_date"]

    def __str__(self):
        return self.batch_number

class NurseryInspection(models.Model):
    
    nursery_batch = models.ForeignKey(
        NurseryBatch,
        on_delete=models.CASCADE,
        related_name="inspections"
    )

    inspection_date = models.DateField()

    germinated_seedlings = models.PositiveIntegerField()

    healthy_seedlings = models.PositiveIntegerField()

    weak_seedlings = models.PositiveIntegerField(
        default=0
    )

    dead_seedlings = models.PositiveIntegerField(
        default=0
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["inspection_date"]

    def __str__(self):
        return f"{self.nursery_batch.batch_number} - {self.inspection_date}"


class Bay(models.Model):
    
    greenhouse = models.ForeignKey(
        Greenhouse,
        on_delete=models.CASCADE,
        related_name="bays"
    )

    bay_code = models.CharField(
        max_length=20
    )

    bay_name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["greenhouse", "bay_code"]

        unique_together = (
            "greenhouse",
            "bay_code",
        )

    def __str__(self):
        return f"{self.greenhouse.greenhouse_name} - {self.bay_name}"

    @property
    def number_of_beds(self):
        return self.beds.count()

    number_of_beds.fget.short_description = "Beds"
class Bed(models.Model):
    
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Occupied", "Occupied"),
        ("Maintenance", "Maintenance"),
    ]

    bay = models.ForeignKey(
    Bay,
    on_delete=models.CASCADE,
    related_name="beds", 
    null =True
    
    )

    bed_code = models.CharField(
        max_length=20
    )

    bed_name = models.CharField(
        max_length=100
    )

    length_m = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    width_m = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField(
        help_text="Maximum number of plants this bed can hold."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    created_at = models.DateTimeField(
        default= timezone.now
    )

    class Meta:
        ordering = ["bay", "bed_code"]

        unique_together = (
            "bay",
            "bed_code",
        )

    @property
    def area(self):
        return self.length_m * self.width_m

    def __str__(self):
        if self.bay:
            return f"{self.bay.greenhouse.greenhouse_code} - {self.bay.bay_code} - {self.bed_code}"
        return self.bed_code
class ProductionEvent(models.Model):
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    production_cycle = models.ForeignKey(
        ProductionCycle,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    event_date = models.DateField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="production_events"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        return f"{self.title} ({self.event_date})"

class ProductionSOP(models.Model):
    
    crop_variety = models.OneToOneField(
        CropVariety,
        on_delete=models.CASCADE,
        related_name="production_sop"
    )

    sop_name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    version = models.CharField(
        max_length=20,
        default="1.0"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["crop_variety"]

    def __str__(self):
        return f"{self.crop_variety} SOP"

class SOPActivity(models.Model):
    
    FREQUENCY_CHOICES = [
        ("Once", "Once"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
    ]

    sop = models.ForeignKey(
        ProductionSOP,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    activity_name = models.CharField(
        max_length=150
    )

    maintenance_type = models.ForeignKey(
        OperationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    day_after_sowing = models.PositiveIntegerField()

    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default="Once"
    )

    priority = models.CharField(
        max_length=20,
        choices=ProductionEvent.PRIORITY_CHOICES,
        default="Medium"
    )

    instructions = models.TextField(
        blank=True
    )

    estimated_duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["day_after_sowing"]

    def __str__(self):
        return f"{self.activity_name} - Day {self.day_after_sowing}"

class ActivityResource(models.Model):
    
    RESOURCE_TYPES = [
        ("Product", "Product"),
        ("Labour", "Labour"),
        ("Equipment", "Equipment"),
    ]

    sop_activity = models.ForeignKey(
        SOPActivity,
        on_delete=models.CASCADE,
        related_name="resources"
    )

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="activity_resources"
    )

    resource_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Used for labour or equipment."
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=30
    )

    estimated_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    remarks = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["resource_type"]

    def __str__(self):
        if self.product:
            return f"{self.sop_activity} - {self.product.product_name}"

        return f"{self.sop_activity} - {self.resource_name}"

class Pest(models.Model):
    
    pest_name = models.CharField(
        max_length=100,
        unique=True
    )

    scientific_name = models.CharField(
        max_length=150,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.pest_name

class Disease(models.Model):
    
    disease_name = models.CharField(
        max_length=100,
        unique=True
    )

    scientific_name = models.CharField(
        max_length=150,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.disease_name

class Scouting(models.Model):
    
    SEVERITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    production_cycle_bed = models.ForeignKey(
        ProductionCycleBed,
        on_delete=models.CASCADE,
        related_name="scouting_records"
    )

    scouting_date = models.DateField()

    pest = models.ForeignKey(
        Pest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    disease = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    affected_plants = models.PositiveIntegerField(
        default=0
    )

    observed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    recommendation = models.TextField(
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-scouting_date"]

    def __str__(self):
        return f"{self.production_cycle_bed} - {self.scouting_date}"

class PackingBatch(models.Model):
    
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Completed", "Completed"),
    ]

    harvest = models.ForeignKey(
        Harvest,
        on_delete=models.CASCADE,
        related_name="packing_batches"
    )

    packing_date = models.DateField()

    packed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    package_type = models.CharField(
        max_length=100
    )

    number_of_packages = models.PositiveIntegerField()

    weight_per_package = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    total_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-packing_date"]

    @property
    def total_weight(self):
        return self.number_of_packages * self.weight_per_package

    def __str__(self):
        return f"Packing {self.id}"

class ProductionCycleSummary(models.Model):
    
    production_cycle = models.OneToOneField(
        ProductionCycle,
        on_delete=models.CASCADE,
        related_name="summary"
    )

    total_seedlings = models.PositiveIntegerField(default=0)

    total_harvest_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_crates = models.PositiveIntegerField(default=0)

    marketable_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    rejected_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    expected_yield_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    actual_yield_per_plant = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    actual_yield_per_bed = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.production_cycle.cycle_number

class Supplier(models.Model):
    
    supplier_code = models.CharField(
        max_length=20,
        unique=True
    )

    supplier_name = models.CharField(
        max_length=200
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["supplier_name"]

    def __str__(self):
        return f"{self.supplier_code} - {self.supplier_name}"

class StockReceipt(models.Model):
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_receipts"
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="stock_receipts",
        null=True,
        blank=True
    )

    received_date = models.DateField()

    received_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    

    class Meta:
        ordering = ["-received_date"]

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        with transaction.atomic():

            super().save(*args, **kwargs)

            if is_new:

                self.product.current_stock += self.quantity
                self.product.save(update_fields=["current_stock"])

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity} {self.product.unit})"

