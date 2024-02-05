import datetime
import io
import os

from functools import wraps

from django.core.files.storage import default_storage
from django.db.models import Count, F, Prefetch
from django.http import FileResponse
from django.utils.text import get_valid_filename

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from reagents import exceptions, filters, generators, models, permissions, serializers


def paginate(action_method):
    @wraps(action_method)
    def inner(self, *args, **kwargs):
        """The action method must return a QuerySet or an iterable based on it."""
        queryset = action_method(self, *args, **kwargs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    return inner


def action_paginate(**kwargs):
    decorator2 = action(**kwargs)
    decorator1 = paginate

    def merged_decorator(func):
        return decorator2(decorator1(func))

    return merged_decorator


class ModelViewSetWithHistoricalRecordsAndOptionalPagination(ModelViewSet):
    model = None
    filterset_fields = []

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled (also by a query param)."""
        if self.paginator is None or "no_pagination" in self.request.query_params:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_queryset(self):
        if self.action == "get_historical_records":
            return self.model.history.all()

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "get_historical_records":
            return getattr(serializers, f"{self.model.__name__}HistoricalRecordsSerializer")

        return super().get_serializer_class()

    @action_paginate(
        detail=False,
        url_path="history",
        filterset_fields=[],
    )
    def get_historical_records(self, request):
        history = self.filter_queryset(self.get_queryset().order_by("-history_id"))
        return history


class ReadOnlyModelViewSetWithOptionalPagination(ReadOnlyModelViewSet):
    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled (also by a query param)."""
        if self.paginator is None or "no_pagination" in self.request.query_params:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)


class UserViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.User
    queryset = model.objects.order_by("id")
    serializer_class = serializers.UserReadAsProjectManagerNotOwnLabWorkerNotOwnSerializer
    permission_classes = [permissions.UserPermission]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["id", "username", "first_name", "last_name", "email"]
    search_fields = ["username", "first_name", "last_name", "email"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action in ("create", "update", "partial_update"):
            return serializers.UserWriteSerializer

        if (self.action == "get_current_user_info" or (self.action in ("list", "retrieve")
                and (user.is_staff or models.User.LAB_MANAGER in user.lab_roles))):
            return serializers.UserReadAsAdminLabManagerProjectManagerOwnLabWorkerOwnSerializer

        return super().get_serializer_class()

    @action(
        detail=False,
        url_path="me",
    )
    def get_current_user_info(self, request):
        user = request.user
        current_user_info = self.get_queryset().get(pk=user.id)
        serializer = self.get_serializer(current_user_info)

        return Response(serializer.data)


class PictogramViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.Pictogram
    queryset = model.objects.order_by("id")
    serializer_class = serializers.PictogramSerializer
    permission_classes = [permissions.HazardPermission]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["id", "pictogram"]
    search_fields = ["pictogram"]


class ClpClassificationViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.ClpClassification
    queryset = model.objects.order_by("id")
    serializer_class = serializers.ClpClassificationSerializer
    permission_classes = [permissions.HazardPermission]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["id", "clp_classification"]
    search_fields = ["clp_classification"]


class HazardStatementViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.HazardStatement
    queryset = model.objects.select_related("clp_classification", "pictogram").defer(
        "clp_classification__classification", "clp_classification__hazard_group"
    ).order_by("id")
    serializer_class = serializers.HazardStatementReadSerializer
    permission_classes = [permissions.HazardPermission]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["id", "code", "phrase"]
    search_fields = ["code", "phrase"]

    def get_queryset(self):
        if self.action == "get_historical_records":
            return self.model.history.select_related("clp_classification", "pictogram").defer(  # pylint: disable=no-member
                "clp_classification__classification", "clp_classification__hazard_group"
            )

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.HazardStatementWriteSerializer

        if self.action == "get_ghs_pictograms":
            return serializers.HazardStatementGhsPictogramsSerializer

        return super().get_serializer_class()

    @action_paginate(
        detail=False,
        url_path="ghs-pictograms",
        ordering_fields = [],
        search_fields = ["clp_classification__clp_classification", "clp_classification__classification"],
    )
    def get_ghs_pictograms(self, request):
        ghs_pictograms = self.filter_queryset(self.get_queryset()).filter(pictogram__isnull=False).values(
            "clp_classification_id",
            "clp_classification__clp_classification",
            "pictogram__pictogram",
            "clp_classification__classification",
        ).order_by(
            "clp_classification__clp_classification",
            "clp_classification__classification",
        ).distinct(
            "clp_classification__clp_classification",
            "clp_classification__classification",
        )

        return ghs_pictograms


class PrecautionaryStatementViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.PrecautionaryStatement
    queryset = model.objects.order_by("id")
    serializer_class = serializers.PrecautionaryStatementSerializer
    permission_classes = [permissions.HazardPermission]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["id", "code", "phrase"]
    search_fields = ["code", "phrase"]


class ReagentTypeViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.ReagentType
    queryset = model.objects.order_by("id")
    serializer_class = serializers.ReagentTypeSerializer
    permission_classes = [permissions.ReagentFieldPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "type"]
    search_fields = ["type"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.ReagentTypeCreateAsAdminSerializer
            return serializers.ReagentTypeCreateWithLabRoleSerializer

        return super().get_serializer_class()


class ProducerViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.Producer
    queryset = model.objects.order_by("id")
    serializer_class = serializers.ProducerSerializer
    permission_classes = [permissions.ReagentFieldPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "producer_name", "brand_name", "abbreviation"]
    search_fields = ["producer_name", "brand_name", "abbreviation"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.ProducerCreateAsAdminSerializer
            return serializers.ProducerCreateWithLabRoleSerializer

        return super().get_serializer_class()


class ConcentrationViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.Concentration
    queryset = model.objects.order_by("id")
    serializer_class = serializers.ConcentrationSerializer
    permission_classes = [permissions.ReagentFieldPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "concentration"]
    search_fields = ["concentration"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.ConcentrationCreateAsAdminSerializer
            return serializers.ConcentrationCreateWithLabRoleSerializer

        return super().get_serializer_class()


class UnitViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.Unit
    queryset = model.objects.order_by("id")
    serializer_class = serializers.UnitSerializer
    permission_classes = [permissions.ReagentFieldPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "unit"]
    search_fields = ["unit"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.UnitCreateAsAdminSerializer
            return serializers.UnitCreateWithLabRoleSerializer

        return super().get_serializer_class()


class PurityQualityViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.PurityQuality
    queryset = model.objects.order_by("id")
    serializer_class = serializers.PurityQualitySerializer
    permission_classes = [permissions.ReagentFieldPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "purity_quality"]
    search_fields = ["purity_quality"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.PurityQualityCreateAsAdminSerializer
            return serializers.PurityQualityCreateWithLabRoleSerializer

        return super().get_serializer_class()


class StorageConditionViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.StorageCondition
    queryset = model.objects.order_by("id")
    serializer_class = serializers.StorageConditionSerializer
    permission_classes = [permissions.ReagentFieldPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "storage_condition"]
    search_fields = ["storage_condition"]

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.StorageConditionCreateAsAdminSerializer
            return serializers.StorageConditionCreateWithLabRoleSerializer

        return super().get_serializer_class()


class ReagentViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.Reagent
    queryset = model.objects.select_related(
        "type", "producer", "concentration", "unit", "purity_quality"
    ).prefetch_related(
        Prefetch("storage_conditions", queryset=models.StorageCondition.objects.only("id", "storage_condition")),
        Prefetch("hazard_statements", queryset=models.HazardStatement.objects.only("id", "code")),
        Prefetch("precautionary_statements", queryset=models.PrecautionaryStatement.objects.only("id", "code")),
    ).defer(
        "type__is_validated_by_admin",
        "producer__producer_name",
        "producer__brand_name",
        "producer__is_validated_by_admin",
        "concentration__is_validated_by_admin",
        "unit__is_validated_by_admin",
        "purity_quality__is_validated_by_admin",
    ).order_by("id")
    serializer_class = serializers.ReagentReadSerializer
    permission_classes = [permissions.ReagentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.ReagentFilter
    search_fields = [
        "name",
        "producer__abbreviation",
        "catalog_no",
        "safety_instruction_name",
    ]

    def get_queryset(self):
        if self.action == "get_historical_records":
            return self.model.history.select_related(  # pylint: disable=no-member
                "type", "producer", "concentration", "unit", "purity_quality"
            ).defer(
                "type__is_validated_by_admin",
                "producer__producer_name",
                "producer__brand_name",
                "producer__is_validated_by_admin",
                "concentration__is_validated_by_admin",
                "unit__is_validated_by_admin",
                "purity_quality__is_validated_by_admin",
            )

        return super().get_queryset()

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.ReagentCreateAsAdminSerializer
            return serializers.ReagentCreateWithLabRoleSerializer

        if self.action in ("update", "partial_update"):
            return serializers.ReagentModifySerializer

        if self.action == "get_safety_instructions":
            return serializers.SafetyInstructionSerializer

        if self.action == "get_safety_instruction":
            return serializers.SafetyInstructionDetailSerializer

        return super().get_serializer_class()

    @action_paginate(
        detail=False,
        url_path="history",
        filterset_class=filters.ReagentHistoricalRecordsFilter,
    )
    def get_historical_records(self, request):
        history = self.filter_queryset(self.get_queryset().order_by("-history_id"))
        return history

    @action_paginate(
        detail=False,
        url_path="safety-instructions",
        filterset_class=None,
    )
    def get_safety_instructions(self, request):
        safety_instructions = self.filter_queryset(self.get_queryset().values("id", "name", "producer__abbreviation"))
        return safety_instructions

    @action(
        detail=True,
        url_path="safety-instructions",
    )
    def get_safety_instruction(self, request, pk=None):
        safety_instruction = self.get_queryset().values("id", "safety_instruction").get(pk=pk)
        serializer = self.get_serializer(safety_instruction)
        return Response(serializer.data)


class ProjectProcedureViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.ProjectProcedure
    queryset = model.objects.select_related("manager").prefetch_related(
        Prefetch("workers", queryset=models.User.objects.only("id", "username").order_by("id")),
    ).only(
        "id",
        "name",
        "is_validated_by_admin",
        "manager__id",
        "manager__username",
    ).order_by("id")
    serializer_class = serializers.ProjectProcedureReadSerializer
    permission_classes = [permissions.ProjectProcedurePermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_validated_by_admin"]
    ordering_fields = ["id", "name"]
    search_fields = ["name"]

    def get_queryset(self):
        if self.action == "get_historical_records":
            return self.model.history.select_related("manager").only(  # pylint: disable=no-member
                "history_user",
                "history_date",
                "history_change_reason",
                "history_id",
                "history_type",
                "id",
                "name",
                "is_validated_by_admin",
                "manager__id",
                "manager__username",
            )

        return super().get_queryset()

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff or (user.is_authenticated and models.User.LAB_MANAGER in user.lab_roles):
                return serializers.ProjectProcedureCreateAsAdminAndLabManagerSerializer
            return serializers.ProjectProcedureCreateAsProjectManagerSerializer

        if self.action in ("update", "partial_update"):
            return serializers.ProjectProcedureUpdateSerializer

        return super().get_serializer_class()

    @action_paginate(
        detail=False,
        url_path="history",
        filterset_fields=[],
    )
    def get_historical_records(self, request):
        history = self.filter_queryset(self.get_queryset().order_by("-history_id"))
        return history


class PersonalReagentViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.PersonalReagent
    queryset = model.objects.order_by("id")
    serializer_class = serializers.PersonalReagentReadSerializer
    permission_classes = [permissions.PersonalReagentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.PersonalReagentFilter
    search_fields = [
        "reagent__name",
        "reagent__producer__abbreviation",
        "main_owner__username",
    ]

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            "reagent__producer",
            "main_owner",
        )

        if self.action in ("list", "retrieve", "generate_all_personal_reagents_report"):
            queryset = queryset.select_related(
                "reagent__type",
                "project_procedure",
            ).prefetch_related(
                Prefetch(
                    "reagent__hazard_statements",
                    queryset=models.HazardStatement.objects.select_related(
                        "clp_classification",
                    ).order_by(
                        "clp_classification__clp_classification",
                    ),
                ),
            )

            return queryset

        if self.action == "get_historical_records":
            return self.model.history.select_related(  # pylint: disable=no-member
                "reagent__producer",
                "main_owner",
                "reagent__type",
                "project_procedure",
            ).prefetch_related(
                Prefetch(
                    "reagent__hazard_statements",
                    queryset=models.HazardStatement.objects.select_related(
                        "clp_classification",
                    ).order_by(
                        "clp_classification__clp_classification",
                    ),
                ),
            )

        if self.action in ("get_personal_view", "generate_personal_view_report"):
            return queryset.select_related(
                "reagent__type",
                "project_procedure",
            ).prefetch_related(
                Prefetch(
                    "reagent__hazard_statements",
                    queryset=models.HazardStatement.objects.select_related(
                        "clp_classification",
                    ).order_by(
                        "clp_classification__clp_classification",
                        "code",
                    ),
                ),
                Prefetch(
                    "reagent__precautionary_statements",
                    queryset=models.PrecautionaryStatement.objects.order_by("code"),
                ),
            )

        if self.action == "generate_usage_record":
            return queryset.select_related("reagent__unit")

        if self.action == "generate_sanepid_pip_report":
            return queryset.prefetch_related(
                Prefetch(
                    "reagent__hazard_statements",
                    queryset=models.HazardStatement.objects.select_related(
                        "clp_classification"
                    ).order_by(
                        "clp_classification__clp_classification"
                    ),
                ),
            )

        if self.action == "generate_lab_manager_report":
            return queryset.select_related(
                "reagent__type",
            ).prefetch_related(
                Prefetch(
                    "reagent__hazard_statements",
                    queryset=models.HazardStatement.objects.select_related(
                        "clp_classification"
                    ).order_by(
                        "clp_classification__clp_classification"
                    ),
                ),
            )

        if self.action == "generate_projects_procedures_report":
            return queryset.select_related(
                "reagent__type",
                "project_procedure",
            ).prefetch_related(
                Prefetch(
                    "reagent__hazard_statements",
                    queryset=models.HazardStatement.objects.select_related(
                        "clp_classification"
                    ).order_by(
                        "clp_classification__clp_classification"
                    ),
                ),
            )

        return queryset

    def get_serializer_class(self):
        user = self.request.user
        if self.action == "create":
            if user.is_staff:
                return serializers.PersonalReagentCreateAsAdminSerializer
            return serializers.PersonalReagentCreateWithLabRoleSerializer

        if self.action in ("update", "partial_update"):
            instance = self.get_object()
            if user.is_staff:
                return serializers.PersonalReagentUpdateAsAdminProjectManagerFromProjectSerializer

            if user.is_authenticated:
                if models.User.LAB_MANAGER in user.lab_roles:
                    return (serializers.PersonalReagentUpdateAsLabManagerProjectManagerNotFromProjectLabWorkerSerializer
                                if instance.main_owner == user
                                else serializers.PersonalReagentUpdateAsLabManagerNotOwnSerializer)

                if (models.User.PROJECT_MANAGER in user.lab_roles
                        and instance.project_procedure is not None
                        and instance.project_procedure.manager == user):
                    return serializers.PersonalReagentUpdateAsAdminProjectManagerFromProjectSerializer

                return serializers.PersonalReagentUpdateAsLabManagerProjectManagerNotFromProjectLabWorkerSerializer

        if self.action == "get_personal_view":
            return serializers.PersonalViewSerializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many and len(request.data) > 50:
            raise exceptions.RequestDataError("Maksymalnie można dodać 50 odczynników osobistych.")

        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        request.data.pop("disposal_utilization_date", None)
        is_archived = request.data.get("is_archived")
        if is_archived is not None and instance.is_archived != is_archived:
            if is_archived:
                request.data["disposal_utilization_date"] = datetime.date.today()
            else:
                request.data["disposal_utilization_date"] = None

        return super().update(request=request, *args, **kwargs)

    @action_paginate(
        detail=False,
        url_path="history",
        filterset_class=filters.PersonalReagentHistoricalRecordsFilter,
    )
    def get_historical_records(self, request):
        history = self.filter_queryset(self.get_queryset().order_by("-history_id"))
        return history

    @action_paginate(
        detail=False,
        url_path="me",
    )
    def get_personal_view(self, request):
        user = request.user
        personal_view_reagents = self.filter_queryset(self.get_queryset()).filter(main_owner=user)
        return personal_view_reagents

    @action(
        detail=True,
        url_path="usage-record",
    )
    def generate_usage_record(self, request, pk=None):  # pylint: disable=unused-argument
        personal_reagent = self.get_object()
        num_of_entries = 56  # Number of entries which ideally fit on two pages
        io_buffer = generators.generate_usage_record(personal_reagent, num_of_entries)

        personal_reagent.is_usage_record_generated = True
        personal_reagent.save(update_fields=["is_usage_record_generated"])

        # FileResponse sets the Content-Disposition header so that browsers present the option to save the file.
        io_buffer.seek(0)
        return FileResponse(
            io_buffer,
            as_attachment=True,
            filename=get_valid_filename(
                f"karta_rozchodu_{personal_reagent.main_owner}_{personal_reagent.reagent.name}.pdf"
            ),
        )

    @action(
        detail=False,
        url_path="report/sanepid-pip",
    )
    def generate_sanepid_pip_report(self, request):
        user = request.user

        if (report_header := self.request.query_params.get("report_header")) is None:
            report_header = "SPIS ODCZYNNIKÓW LABORATORIUM"

        report_data = generators.generate_sanepid_pip_report_data(self.filter_queryset(self.get_queryset()))
        io_buffer = generators.generate_report(report_header, user, report_data, data_font_size=6)

        io_buffer.seek(0)
        return FileResponse(
            io_buffer,
            as_attachment=True,
            filename=get_valid_filename(f"raport_sanepid_pip_{user.username}.pdf"),
        )

    @action(
        detail=False,
        url_path="report/lab-manager",
    )
    def generate_lab_manager_report(self, request):
        user = request.user

        if (report_header := self.request.query_params.get("report_header")) is None:
            report_header = "SPIS ODCZYNNIKÓW LABORATORIUM"

        io_buffer = io.BytesIO()

        report_data = generators.generate_lab_manager_report_data(self.filter_queryset(self.get_queryset()))
        io_buffer = generators.generate_report(report_header, user, report_data, data_font_size=5)

        io_buffer.seek(0)
        return FileResponse(
            io_buffer,
            as_attachment=True,
            filename=get_valid_filename(f"raport_kierownika_laboratorium_{user.username}.pdf"),
        )

    @action(
        detail=False,
        url_path="report/projects-procedures",
    )
    def generate_projects_procedures_report(self, request):
        user = request.user

        if (report_header := self.request.query_params.get("report_header")) is None:
            report_header = "SPIS ODCZYNNIKÓW LABORATORIUM"

        report_data = generators.generate_projects_procedures_report_data(self.filter_queryset(self.get_queryset()))
        io_buffer = generators.generate_report(report_header, user, report_data, data_font_size=5)

        io_buffer.seek(0)
        return FileResponse(
            io_buffer,
            as_attachment=True,
            filename=get_valid_filename(f"raport_kierownika_projektu_procedury_{user.username}.pdf"),
        )

    @action(
        detail=False,
        url_path="report/all",
    )
    def generate_all_personal_reagents_report(self, request):
        user = request.user

        if (report_header := self.request.query_params.get("report_header")) is None:
            report_header = "SPIS ODCZYNNIKÓW LABORATORIUM"

        report_data = generators.generate_all_personal_reagents_report_data(
            self.filter_queryset(self.get_queryset())
        )

        io_buffer = generators.generate_report(report_header, user, report_data, data_font_size=3)

        io_buffer.seek(0)
        return FileResponse(
            io_buffer,
            as_attachment=True,
            filename=get_valid_filename(f"raport_wszystkie_odczynniki_osobiste_{user.username}.pdf"),
        )

    @action(
        detail=False,
        url_path="report/personal-view",
    )
    def generate_personal_view_report(self, request):
        user = request.user

        if (report_header := self.request.query_params.get("report_header")) is None:
            report_header = "SPIS ODCZYNNIKÓW LABORATORIUM"

        my_personal_reagents = self.get_queryset().filter(main_owner=user)
        report_data = generators.generate_personal_view_report_data(self.filter_queryset(my_personal_reagents))
        io_buffer = generators.generate_report(report_header, user, report_data, data_font_size=3)

        io_buffer.seek(0)
        return FileResponse(
            io_buffer,
            as_attachment=True,
            filename=get_valid_filename(f"raport_moje_odczynniki_osobiste_{user.username}.pdf"),
        )

    @action(
        detail=False,
        url_path="statistics",
    )
    def generate_statistics(self, request):
        user = request.user
        user_personal_reagents = self.get_queryset().filter(main_owner=user)

        if user.is_staff:
            return Response(
                generators.generate_admin_statistics()
                | generators.generate_lab_manager_statistics()
                | generators.generate_project_manager_statistics()
                | generators.generate_lab_worker_statistics(user_personal_reagents, user)
            )

        if models.User.LAB_MANAGER in user.lab_roles:
            return Response(
                generators.generate_lab_manager_statistics()
                | generators.generate_project_manager_statistics()
                | generators.generate_lab_worker_statistics(user_personal_reagents, user)
            )

        if models.User.PROJECT_MANAGER in user.lab_roles:
            return Response(
                generators.generate_project_manager_statistics()
                | generators.generate_lab_worker_statistics(user_personal_reagents, user)
            )

        if models.User.LAB_WORKER in user.lab_roles:
            return Response(generators.generate_lab_worker_statistics(user_personal_reagents, user))

        raise PermissionDenied()


class NotificationViewSet(ReadOnlyModelViewSetWithOptionalPagination):
    serializer_class = serializers.PersonalReagentReadSerializer
    permission_classes = [permissions.NotificationPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []

    def get_queryset(self):
        if self.action in (
            "get_reagent_fields_with_pending_validation",
            "get_reagents_with_close_expiration_date",
            "get_reagents_with_not_generated_usage_records",
            "get_few_critical_reagents",
        ):
            return models.PersonalReagent.objects.select_related("reagent").order_by("id")
        if self.action == "get_reagent_requests":
            return models.ReagentRequest.objects.select_related("requester", "personal_reagent__reagent").order_by("id")

        raise NotFound("Punkt końcowy /notifications/ nie zawiera danych. Użyj jednej z dostępnych akcji.")

    def get_serializer_class(self):
        if self.action == "get_reagent_fields_with_pending_validation":
            return serializers.ReagentFieldsWithPendingValidationNotificationSerializer

        if self.action == "get_reagents_with_close_expiration_date":
            return serializers.ReagentsWithCloseExpirationDateNotificationSerializer

        if self.action == "get_reagents_with_not_generated_usage_records":
            return serializers.ReagentsWithNotGeneratedUsageRecordsNotificationSerializer

        if self.action == "get_few_critical_reagents":
            return serializers.ReagentsFewCriticalSerializer

        if self.action == "get_reagent_requests":
            return serializers.ReagentRequestsNotificationSerializer

        raise NotFound("Endpoint /notifications/ nie zawiera danych. Użyj jednej z dostępnych akcji.")

    @action_paginate(
        detail=False,
        url_path="reagents/pending-validation-fields",
    )
    def get_reagent_fields_with_pending_validation(self, request):
        reagent_field_models_with_pending_validation = [
            models.ReagentType,
            models.Producer,
            models.Concentration,
            models.Unit,
            models.PurityQuality,
            models.StorageCondition,
            models.Reagent,
        ]

        reagent_fields_with_pending_validation = []

        # Additional field for easier display in the frontend grid
        idx = 1
        for reagent_field_model in reagent_field_models_with_pending_validation:
            reagent_models_with_pending_validation = reagent_field_model.objects.filter(is_validated_by_admin=False)
            for reagent_model in reagent_models_with_pending_validation:
                reagent_fields_with_pending_validation.append(
                    {
                        "id": idx,
                        "pk": reagent_model.id,
                        "table_name": reagent_field_model.__name__,
                        "value": str(reagent_model),
                    },
                )
                idx += 1

        return reagent_fields_with_pending_validation

    @action_paginate(
        detail=False,
        url_path="reagents/close-expiration-date",
    )
    def get_reagents_with_close_expiration_date(self, request):
        user = request.user
        personal_reagents_with_close_expiration_date = self.get_queryset()
        if (month_param := request.query_params.get("month")) is not None:
            wrong_month_exception = exceptions.QueryParamError(
                "Parametr `month` musi być liczbą całkowitą w zakresie od 1 do 12."
            )
            try:
                month = int(month_param)
                if not 1 <= month <= 12:
                    raise wrong_month_exception
                personal_reagents_with_close_expiration_date = personal_reagents_with_close_expiration_date.filter(
                    expiration_date__month=month
                )
            except ValueError as exception:
                raise wrong_month_exception from exception

        if (year_param := request.query_params.get("year")) is not None:
            wrong_year_exception = exceptions.QueryParamError(
                "Parametr `year` musi być liczbą całkowitą większą lub równą od 1899."
            )
            try:
                year = int(year_param)
                if year < 1899:
                    raise wrong_year_exception
                personal_reagents_with_close_expiration_date = personal_reagents_with_close_expiration_date.filter(
                    expiration_date__year=year
                )
            except ValueError as exception:
                raise wrong_year_exception from exception

        personal_reagents_with_close_expiration_date = personal_reagents_with_close_expiration_date.filter(
            main_owner=user,
            is_archived=False,
        )
        return personal_reagents_with_close_expiration_date

    @action_paginate(
        detail=False,
        url_path="reagents/not-generated-usage-records",
    )
    def get_reagents_with_not_generated_usage_records(self, request):
        user = request.user
        reagents_with_usage_record_not_generated = self.get_queryset().filter(
            main_owner=user, reagent__is_usage_record_required=True, is_usage_record_generated=False
        )
        return reagents_with_usage_record_not_generated

    @action_paginate(
        detail=False,
        url_path="reagents/few-critical",
    )
    def get_few_critical_reagents(self, request):
        user = request.user
        few_critical_personal_reagents = self.get_queryset().filter(
            main_owner=user, is_critical=True
        ).values(
            "reagent_id", reagent_name=F("reagent__name")
        ).annotate(
            count=Count("reagent_id")
        ).filter(
            count__lt=3
        ).order_by("reagent_id")
        return few_critical_personal_reagents

    @action_paginate(
        detail=False,
        url_path="reagent-requests",
        filterset_fields=["status"],
    )
    def get_reagent_requests(self, request):
        responder = request.user
        reagent_requests = self.filter_queryset(self.get_queryset()).filter(
            personal_reagent__main_owner=responder
        )

        return reagent_requests


class ReagentRequestViewSet(ModelViewSetWithHistoricalRecordsAndOptionalPagination):
    model = models.ReagentRequest
    queryset = model.objects.select_related(
        "requester",
        "personal_reagent__reagent",
        "personal_reagent__main_owner",
    ).order_by("id")
    serializer_class = serializers.ReagentRequestListSerializer
    permission_classes = [permissions.ReagentRequestPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["status"]
    ordering_fields = ["id", "change_status_date"]
    search_fields = [
        "requester__username",
        "personal_reagent__reagent__name",
    ]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.ReagentRequestCreateSerializer

        if self.action in ("update", "partial_update"):
            return serializers.ReagentRequestUpdateSerializer

        if self.action == "get_current_user_reagent_requests":
            return serializers.ReagentRequestCurrentUserListSerializer

        if self.action == "change_reagent_request_status":
            return serializers.ReagentRequestStatusChangeSerializer

        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.action == "create":
            personal_reagents_with_aa_status = models.ReagentRequest.objects.filter(
                status=models.ReagentRequest.AWAITING_APPROVAL
            ).values_list("personal_reagent__id", flat=True)

            context["personal_reagents_with_aa_status"] = personal_reagents_with_aa_status

        return context

    @action_paginate(
        detail=False,
        url_path="me",
        search_fields=["personal_reagent__reagent__name"],
    )
    def get_current_user_reagent_requests(self, request):
        requester = request.user
        current_user_reagent_requests = self.filter_queryset(self.get_queryset()).filter(requester=requester)
        return current_user_reagent_requests

    @action(
        detail=True,
        url_path="status",
        methods=["patch"],
    )
    def change_reagent_request_status(self, request, pk=None):  # pylint: disable=unused-argument
        reagent_request = self.get_object()
        serializer = self.get_serializer(reagent_request, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UserManualView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.UserManualPermission]

    user_manual_path = os.path.join("UserManuals", "user_manual.pdf")

    def get(self, request, *args, **kwargs):
        if default_storage.exists(self.user_manual_path):
            user_manual_url = request.build_absolute_uri(default_storage.url(self.user_manual_path))
            serializer = serializers.UserManualGetSerializer({"user_manual": user_manual_url})
            return Response(serializer.data)

        raise NotFound("Brak instrukcji użytkownika.")

    def put(self, request, *args, **kwargs):
        serializer = serializers.UserManualPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            default_storage.delete(self.user_manual_path)
        except FileNotFoundError:
            pass

        serializer.save(user_manual_path=self.user_manual_path)
        return Response(serializer.data)
