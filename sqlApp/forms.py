from django import forms

from .models import OperationLog


# class OperationLogForm(forms.ModelForm):

    # class Meta:

    #     model = OperationLog

    #     fields = [
    #         "activity_date",
    #         "maintenance_type",
    #         "product",
    #         "quantity",
    #         "unit",
    #         "labour_cost",
    #         "remarks",
    #     ]

    #     widgets = {

    #         "activity_date": forms.DateInput(
    #             attrs={
    #                 "type": "date",
    #                 "class": "form-control"
    #             }
    #         ),

    #         "maintenance_type": forms.Select(
    #             attrs={
    #                 "class": "form-select"
    #             }
    #         ),

    #         "product": forms.Select(
    #             attrs={
    #                 "class": "form-select"
    #             }
    #         ),

    #         "quantity": forms.NumberInput(
    #             attrs={
    #                 "class": "form-control"
    #             }
    #         ),

    #         "unit": forms.TextInput(
    #             attrs={
    #                 "class": "form-control"
    #             }
    #         ),

    #         "labour_cost": forms.NumberInput(
    #             attrs={
    #                 "class": "form-control"
    #             }
    #         ),

    #         "remarks": forms.Textarea(
    #             attrs={
    #                 "class": "form-control",
    #                 "rows": 3
    #             }
    #         ),
    #     }

class OperationLogForm(forms.ModelForm):

    class Meta:

        model = OperationLog

        fields = [
            "activity_date",
            "maintenance_type",
            "product",
            "quantity",
            "unit",
            "labour_cost",
            "remarks",
        ]

        widgets = {

            "activity_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "maintenance_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "product": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "unit": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "labour_cost": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
        }