from django.urls import path
from . views import *

urlpatterns = [
    path('', dashboard, name = 'dashboard'),
    path('harvests', harvest_list, name = 'harvest_list'),
    path(
    "harvest/<int:pk>/",
    harvest_detail,
    name="harvest_detail",
),
    path("reports/", reports, name="reports"),
    path('farmers/', farmer_list, name='farmers'),
    path('export-harvest/', export_harvest_excel,name='export_harvest_excel'),

    path(
        "production/",
        production_cycle_list,
        name="production_cycle_list"
    ),

    path(
        "production/<int:pk>/",
        production_cycle_detail,
        name="production_cycle_detail"
    ),

    path(
    "api/operation-type/<int:pk>/",
    operation_type_detail_api,
    name="operation_type_api",
    ),
    path(
        "inventory/",
        inventory_dashboard,
        name="inventory_dashboard",
    ),
    path(
        "reports/",
        reports_dashboard,
        name="reports_dashboard",
    ),
    path(
    "inventory/ledger/",
    stock_ledger,
    name="stock_ledger",
    ),
    path(
    "greenhouses/",
    greenhouse_list,
    name="greenhouse_list",
    ),
    path(
    "greenhouse_detail/<int:pk>/",
    greenhouse_detail,
    name="greenhouse_detail",
    ),
    path(
    "greenhouse/<int:pk>/performance/",
    greenhouse_performance,
    name="greenhouse_performance",
    ),
    path(
    "operations/",
    operation_list,
    name="operation_list",
    ),
    path(
    "production-cycle/<int:pk>/performance/",
    production_cycle_performance,
    name="production_cycle_performance",
    ),
    path(
    "beds/<int:pk>/performance/",
    bed_performance,
    name="bed_performance",
    ),
    path(
        "operation-type/<int:pk>/fields/",
        operation_type_fields,
        name="operation_type_fields",
    ),
    path(
    "operation/<int:pk>/",
    operation_detail,
    name="operation_detail",
    ),
    path(
    "nursery/",
    nursery_batch_list,
    name="nursery_batch_list",
    ),
    path(
    "nursery/<int:pk>/",
    nursery_batch_detail,
    name="nursery_batch_detail",
    ),
    path(
    "reports/harvest/",
    harvest_report,
    name="harvest_report",
    ),
    path(
    "reports/inventory/",
    inventory_report,
    name="inventory_report",
    ),

    path(
        "reports/production",
        production_report,
        name="production_report",
    ),

    # path(
    #     "operations/<int:pk>/",
    #     operation_detail,
    #     name="operation_detail",
    # ),

    # path(
    #     "operations/<int:pk>/edit/",
    #     operation_update,
    #     name="operation_update",
    # ),

    # path(
    #     "operations/<int:pk>/delete/",
    #     operation_delete,
    #     name="operation_delete",
    # ),

]
