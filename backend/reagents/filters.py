from django_filters import rest_framework as filters

from reagents import models


class ReagentFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("name", "name"),
            ("producer__abbreviation", "producer"),
            ("catalog_no", "catalog_no"),
            ("safety_instruction_name", "safety_instruction_name"),
            ("safety_data_sheet_name", "safety_data_sheet_name"),
        ),
    )

    class Meta:
        model = models.Reagent
        fields = [
            "is_validated_by_admin",
        ]


class ReagentHistoricalRecordsFilter(ReagentFilter):
    class Meta:
        model = models.Reagent.history.model  # pylint: disable=no-member
        fields = []


class PersonalReagentFilter(filters.FilterSet):
    laboratory = filters.ModelMultipleChoiceFilter(queryset=models.Laboratory.objects.all())
    project_procedure = filters.ModelMultipleChoiceFilter(queryset=models.ProjectProcedure.objects.all())
    main_owner = filters.ModelMultipleChoiceFilter(queryset=models.User.objects.all())
    reagent = filters.ModelMultipleChoiceFilter(queryset=models.Reagent.objects.all())
    room = filters.AllValuesMultipleFilter()
    detailed_location = filters.AllValuesMultipleFilter()
    type = filters.ModelMultipleChoiceFilter(field_name="reagent__type", queryset=models.ReagentType.objects.all())
    producer = filters.ModelMultipleChoiceFilter(field_name="reagent__producer", queryset=models.Producer.objects.all())
    clp_classification = filters.ModelMultipleChoiceFilter(
        field_name="reagent__hazard_statements__clp_classification",
        queryset=models.ClpClassification.objects.all()
    )
    cas_no = filters.AllValuesMultipleFilter(field_name="reagent__cas_no")
    is_usage_record_required = filters.BooleanFilter(field_name="reagent__is_usage_record_required")
    is_validated_by_admin = filters.BooleanFilter(field_name="reagent__is_validated_by_admin")

    receipt_purchase_date_lt = filters.DateFilter(field_name="receipt_purchase_date", lookup_expr="lt")
    receipt_purchase_date_lte = filters.DateFilter(field_name="receipt_purchase_date", lookup_expr="lte")
    receipt_purchase_date_gt = filters.DateFilter(field_name="receipt_purchase_date", lookup_expr="gt")
    receipt_purchase_date_gte = filters.DateFilter(field_name="receipt_purchase_date", lookup_expr="gte")
    expiration_date_lt = filters.DateFilter(field_name="expiration_date", lookup_expr="lt")
    expiration_date_lte = filters.DateFilter(field_name="expiration_date", lookup_expr="lte")
    expiration_date_gt = filters.DateFilter(field_name="expiration_date", lookup_expr="gt")
    expiration_date_gte = filters.DateFilter(field_name="expiration_date", lookup_expr="gte")
    disposal_utilization_date_lt = filters.DateFilter(field_name="disposal_utilization_date", lookup_expr="lt")
    disposal_utilization_date_lte = filters.DateFilter(field_name="disposal_utilization_date", lookup_expr="lte")
    disposal_utilization_date_gt = filters.DateFilter(field_name="disposal_utilization_date", lookup_expr="gt")
    disposal_utilization_date_gte = filters.DateFilter(field_name="disposal_utilization_date", lookup_expr="gte")

    ordering = filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("reagent__name", "reagent"),
            ("reagent__producer__abbreviation", "producer"),
            ("main_owner", "main_owner"),
            ("reagent__catalog_no", "catalog_no"),
            ("lot_no", "lot_no"),
            ("receipt_purchase_date", "receipt_purchase_date"),
            ("expiration_date", "expiration_date"),
            ("disposal_utilization_date", "disposal_utilization_date"),
            ("room", "room"),
            ("detailed_location", "detailed_location"),
        ),
    )

    class Meta:
        model = models.PersonalReagent
        fields = [
            "is_critical",
            "receipt_purchase_date",
            "expiration_date",
            "disposal_utilization_date",
            "is_usage_record_generated",
            "is_archived",
        ]


class PersonalReagentHistoricalRecordsFilter(PersonalReagentFilter):
    class Meta(PersonalReagentFilter.Meta):
        model = models.PersonalReagent.history.model  # pylint: disable=no-member
        fields = []
