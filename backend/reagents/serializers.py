# Pylint for some reason doesn't consider metaclasses which are used in serializers.Serializer,
# so we silent the warning for the whole module.
# pylint: disable=abstract-method

from django.contrib.auth.password_validation import validate_password
from django.core.files.storage import default_storage
from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.validators import UniqueTogetherValidator

from reagents import models


def get_attr_value_for_validation(serializer, attrs, attr_name):
    """This function helps with the problem of doing validation on full (POST, PUT) and partial (PATCH) data."""
    return (attrs.get(attr_name)
                if not (serializer.partial and serializer.instance)
                else attrs.get(attr_name, getattr(serializer.instance, attr_name)))


class UserReadAsAdminLabManagerProjectManagerOwnLabWorkerOwnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "lab_roles", "last_login"]


class UserReadAsProjectManagerNotOwnLabWorkerNotOwnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "lab_roles"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        """Check that:
            1. The password meets all validator requirements.
            2. If the user is not an admin (is_staff == False), `lab_roles` can't be empty.
            3. If the project manager role is removed, the user isn't a manager in any of them.
        """
        lab_roles = get_attr_value_for_validation(self, attrs, "lab_roles")
        is_staff = get_attr_value_for_validation(self, attrs, "is_staff")

        if self.instance:
            user = self.instance
            if (models.User.PROJECT_MANAGER in user.lab_roles and
                    lab_roles is not None and models.User.PROJECT_MANAGER not in lab_roles):
                managed_projects_procedures = models.ProjectProcedure.objects.filter(manager=user)
                if managed_projects_procedures:
                    raise serializers.ValidationError(detail={
                        "lab_roles": "Nie można usunąć roli kierownika projektu/procedury, gdyż użytkownik jest "
                                     "kierownikiem następujących projektów/procedur: "
                                    f"{', '.join(map(str, managed_projects_procedures))}."
                    })
        else:
            user = models.User(**attrs)

        if (password := attrs.get("password")) is not None:
            validate_password(password, user)

        if not lab_roles and not is_staff:
            raise serializers.ValidationError(detail={
                "lab_roles": "Użytkownik, który nie jest administratorem, musi mieć nadaną co najmniej jedną rolę."
            })

        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes("update", self, validated_data)
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UserHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.User.history.model  # pylint: disable=no-member
        exclude = ["is_superuser", "is_active", "date_joined", "history_id"]


class ReagentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReagentType
        fields = "__all__"


class ReagentTypeCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.ReagentType
        fields = "__all__"


class ReagentTypeCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.ReagentType
        fields = "__all__"


class ReagentTypeHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.ReagentType.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Producer
        fields = "__all__"


class ProducerCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.Producer
        fields = "__all__"


class ProducerCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.Producer
        fields = "__all__"


class ProducerHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.Producer.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class ConcentrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Concentration
        fields = "__all__"


class ConcentrationCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.Concentration
        fields = "__all__"


class ConcentrationCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.Concentration
        fields = "__all__"


class ConcentrationHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.Concentration.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = "__all__"


class UnitCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.Unit
        fields = "__all__"


class UnitCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.Unit
        fields = "__all__"


class UnitHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.Unit.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class PurityQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurityQuality
        fields = "__all__"


class PurityQualityCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.PurityQuality
        fields = "__all__"


class PurityQualityCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.PurityQuality
        fields = "__all__"


class PurityQualityHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.PurityQuality.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class StorageConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StorageCondition
        fields = "__all__"


class StorageConditionCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.StorageCondition
        fields = "__all__"


class StorageConditionCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.StorageCondition
        fields = "__all__"


class StorageConditionHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.StorageCondition.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class ClpClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClpClassification
        fields = "__all__"


class ClpClassificationHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.ClpClassification.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class PictogramSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pictogram
        fields = "__all__"


class PictogramHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)
    pictogram = serializers.SerializerMethodField()

    class Meta:
        model = models.Pictogram.history.model  # pylint: disable=no-member
        exclude = ["history_id"]

    def get_pictogram(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(default_storage.url(obj.pictogram))


class HazardStatementPictogramSerializer(serializers.ModelSerializer):
    repr = serializers.FileField(source="pictogram", read_only=True)

    class Meta:
        model = models.Pictogram
        fields = ["id", "repr"]


class HazardStatementClpClassificationSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="clp_classification", read_only=True)

    class Meta:
        model = models.ClpClassification
        fields = ["id", "repr"]


class HazardStatementReadSerializer(serializers.ModelSerializer):
    pictogram = HazardStatementPictogramSerializer(read_only=True)
    clp_classification = HazardStatementClpClassificationSerializer(read_only=True)
    class Meta:
        model = models.HazardStatement
        fields = "__all__"


class HazardStatementWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HazardStatement
        fields = "__all__"

    def validate(self, attrs):
        """Check that:
            1. The CLP classification isn't empty when the code starts with "H".
        """
        code = get_attr_value_for_validation(self, attrs, "code")
        clp_classification = get_attr_value_for_validation(self, attrs, "clp_classification")

        if code.startswith("H") and clp_classification is None:
            raise serializers.ValidationError(
                detail={"clp_classification": "Klasyfikcja CLP jest wymagana w przypadku kodów H."}
            )
        return attrs


class HazardStatementGhsPictogramsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="clp_classification_id", read_only=True)
    clp_classification = serializers.CharField(source="clp_classification__clp_classification", read_only=True)
    pictogram = serializers.SerializerMethodField(read_only=True)
    classification = serializers.CharField(source="clp_classification__classification", read_only=True)

    def get_pictogram(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(default_storage.url(obj["pictogram__pictogram"]))


class HazardStatementHistoricalRecordsSerializer(HazardStatementReadSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.HazardStatement.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class PrecautionaryStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrecautionaryStatement
        fields = "__all__"


class PrecautionaryStatementHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.PrecautionaryStatement.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class SafetyDataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SafetyDataSheet
        fields = "__all__"


class SafetyDataSheetCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.SafetyDataSheet
        fields = "__all__"


class SafetyDataSheetCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.SafetyDataSheet
        fields = "__all__"


class SafetyDataSheetHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)
    safety_data_sheet = serializers.SerializerMethodField()

    class Meta:
        model = models.SafetyDataSheet.history.model  # pylint: disable=no-member
        exclude = ["history_id"]

    def get_safety_data_sheet(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(default_storage.url(obj.safety_data_sheet))


class SafetyInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SafetyInstruction
        fields = "__all__"


class SafetyInstructionCreateAsAdminSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta:
        model = models.SafetyInstruction
        fields = "__all__"


class SafetyInstructionCreateWithLabRoleSerializer(serializers.ModelSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta:
        model = models.SafetyInstruction
        fields = "__all__"


class SafetyInstructionHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)
    safety_instruction = serializers.SerializerMethodField()

    class Meta:
        model = models.SafetyInstruction.history.model  # pylint: disable=no-member
        exclude = ["history_id"]

    def get_safety_instruction(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(default_storage.url(obj.safety_instruction))


class ReagentFieldProducerSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="abbreviation", read_only=True)

    class Meta:
        model = models.Producer
        fields = ["id", "repr"]


class ReagentFieldReagentTypeSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="type", read_only=True)

    class Meta:
        model = models.ReagentType
        fields = ["id", "repr"]


class ReagentFieldConcentrationSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="concentration", read_only=True)

    class Meta:
        model = models.Concentration
        fields = ["id", "repr"]


class ReagentFieldUnitSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="unit", read_only=True)

    class Meta:
        model = models.Unit
        fields = ["id", "repr"]


class ReagentFieldPurityQualitySerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="purity_quality", read_only=True)

    class Meta:
        model = models.PurityQuality
        fields = ["id", "repr"]


class ReagentFieldStorageConditionSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="storage_condition", read_only=True)

    class Meta:
        model = models.StorageCondition
        fields = ["id", "repr"]


class ReagentFieldHazardStatementReadSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="code", read_only=True)

    class Meta:
        model = models.HazardStatement
        fields = ["id", "repr"]


class ReagentFieldPrecautionaryStatementSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="code", read_only=True)

    class Meta:
        model = models.PrecautionaryStatement
        fields = ["id", "repr"]


class ReagentFieldSafetyDataSheetSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = models.SafetyDataSheet
        fields = ["id", "repr"]


class ReagentFieldSafetyInstructionSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = models.SafetyInstruction
        fields = ["id", "repr"]


class ReagentReadSerializer(serializers.ModelSerializer):
    type = ReagentFieldReagentTypeSerializer(read_only=True)
    producer = ReagentFieldProducerSerializer(read_only=True)
    concentration = ReagentFieldConcentrationSerializer(read_only=True)
    unit = ReagentFieldUnitSerializer(read_only=True)
    purity_quality = ReagentFieldPurityQualitySerializer(read_only=True)
    storage_conditions = ReagentFieldStorageConditionSerializer(read_only=True, many=True)
    hazard_statements = ReagentFieldHazardStatementReadSerializer(read_only=True, many=True)
    precautionary_statements = ReagentFieldPrecautionaryStatementSerializer(read_only=True, many=True)
    safety_data_sheet = ReagentFieldSafetyDataSheetSerializer(read_only=True)
    safety_instruction = ReagentFieldSafetyInstructionSerializer(read_only=True)

    class Meta:
        model = models.Reagent
        fields = "__all__"


class ReagentModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reagent
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=["producer", "catalog_no"],
                message="Pola Producent oraz Numer katalogowy muszą tworzyć unikatową parę."
            ),
        ]

    def validate(self, attrs):
        """Check that:
            1. Usage record is required for the reagent if any of its hazard statements indicate that.
        """
        is_usage_record_required = get_attr_value_for_validation(self, attrs, "is_usage_record_required")
        hazard_statements = get_attr_value_for_validation(self, attrs, "hazard_statements")

        if not is_usage_record_required:
            if ((isinstance(hazard_statements, list)
                        and any(map(lambda x: x.is_usage_record_required, hazard_statements)))
                    or (not isinstance(hazard_statements, list)
                        and hazard_statements.all().filter(is_usage_record_required=True).exists())):
                raise serializers.ValidationError(detail={
                    "is_usage_record_required": "Karta rozchodu jest wymagana ze względu na jeden z kodów H "
                                                "tego odczynnika."
                })
        return attrs


class ReagentCreateAsAdminSerializer(ReagentModifySerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta(ReagentModifySerializer.Meta):
        pass


class ReagentCreateWithLabRoleSerializer(ReagentModifySerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta(ReagentModifySerializer.Meta):
        pass


class ReagentHistoricalRecordsSerializer(ReagentReadSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)
    storage_conditions = serializers.SerializerMethodField()
    hazard_statements = serializers.SerializerMethodField()
    precautionary_statements = serializers.SerializerMethodField()

    class Meta:
        model = models.Reagent.history.model  # pylint: disable=no-member
        exclude = ["history_id"]

    def get_storage_conditions(self, obj):
        storage_conditions = obj.storage_conditions.filter(
            history_id=obj.history_id
        ).order_by(
            "storagecondition__id"
        ).values(
            "storagecondition__id", "storagecondition__storage_condition"
        )
        return [
            {
                "id": storage_condition["storagecondition__id"],
                "repr": storage_condition["storagecondition__storage_condition"],
            } for storage_condition in storage_conditions
        ]

    def get_hazard_statements(self, obj):
        hazard_statements = obj.hazard_statements.filter(
            history_id=obj.history_id
        ).order_by(
            "hazardstatement__id"
        ).values(
            "hazardstatement__id", "hazardstatement__code"
        )
        return [
            {
                "id": hazard_statement["hazardstatement__id"],
                "repr": hazard_statement["hazardstatement__code"],
            } for hazard_statement in hazard_statements
        ]

    def get_precautionary_statements(self, obj):
        precautionary_statements = obj.precautionary_statements.filter(
            history_id=obj.history_id
        ).order_by(
            "precautionarystatement__id"
        ).values(
            "precautionarystatement__id", "precautionarystatement__code"
        )
        return [
            {
                "id": precautionary_statement["precautionarystatement__id"],
                "repr": precautionary_statement["precautionarystatement__code"],
            } for precautionary_statement in precautionary_statements
        ]


class ReagentFieldUserSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="username", read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "repr"]


class ProjectProcedureReadSerializer(serializers.ModelSerializer):
    manager = ReagentFieldUserSerializer(read_only=True)
    workers = ReagentFieldUserSerializer(read_only=True, many=True)

    class Meta:
        model = models.ProjectProcedure
        fields = "__all__"


class ProjectProcedureUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectProcedure
        fields = "__all__"

    def validate_manager(self, value):
        """Check that:
            1. The manager has the project manager role.
        """
        if models.User.PROJECT_MANAGER not in value.lab_roles:
            raise serializers.ValidationError(
                detail="Kierownik projektu/procedury musi mieć przypisaną odpowiednią rolę."
            )
        return value

    def validate(self, attrs):
        """Check that:
            1. The manager belongs to the workers field as well.
        """
        manager = get_attr_value_for_validation(self, attrs, "manager")
        workers = get_attr_value_for_validation(self, attrs, "workers")
        if not isinstance(workers, list):
            workers = workers.all()

        if manager not in workers:
            raise serializers.ValidationError(
                detail={"workers": "Kierownik projektu/procedury musi być wybrany jako pracownik."}
            )
        return attrs


class ProjectProcedureCreateAsAdminAndLabManagerSerializer(ProjectProcedureUpdateSerializer):
    is_validated_by_admin = serializers.HiddenField(default=True)

    class Meta(ProjectProcedureUpdateSerializer.Meta):
        pass


class ProjectProcedureCreateAsProjectManagerSerializer(ProjectProcedureUpdateSerializer):
    is_validated_by_admin = serializers.HiddenField(default=False)

    class Meta(ProjectProcedureUpdateSerializer.Meta):
        pass


class ProjectProcedureHistoricalRecordsSerializer(ProjectProcedureReadSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)
    workers = serializers.SerializerMethodField()

    class Meta:
        model = models.ProjectProcedure.history.model  # pylint: disable=no-member
        exclude = ["history_id"]

    def get_workers(self, obj):
        workers = obj.workers.filter(
            history_id=obj.history_id
        ).order_by(
            "user__id"
        ).values(
            "user__id", "user__username"
        )
        return [
            {
                "id": worker["user__id"],
                "repr": worker["user__username"],
            } for worker in workers
        ]


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Laboratory
        fields = "__all__"


class LaboratoryHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.Laboratory.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class ReagentFieldReagentSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = models.Reagent
        fields = ["id", "repr"]


class ReagentFieldProjectProcedureSerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = models.ProjectProcedure
        fields = ["id", "repr"]


class ReagentFieldLaboratorySerializer(serializers.ModelSerializer):
    repr = serializers.CharField(source="laboratory", read_only=True)

    class Meta:
        model = models.Laboratory
        fields = ["id", "repr"]


class PersonalReagentReadSerializer(serializers.ModelSerializer):
    reagent = ReagentFieldReagentSerializer(read_only=True)
    producer = ReagentFieldProducerSerializer(source="reagent.producer", read_only=True)
    catalog_no = serializers.CharField(source="reagent.catalog_no", read_only=True)
    main_owner = ReagentFieldUserSerializer(read_only=True)
    project_procedure = ReagentFieldProjectProcedureSerializer(read_only=True)
    project_procedure_manager_id = serializers.IntegerField(
        source="project_procedure.manager_id",
        read_only=True,
        allow_null=True,
    )
    laboratory = ReagentFieldLaboratorySerializer(read_only=True)
    clp_classifications = serializers.SerializerMethodField()
    is_usage_record_required = serializers.BooleanField(source="reagent.is_usage_record_required", read_only=True)

    class Meta:
        model = models.PersonalReagent
        fields = "__all__"

    def get_clp_classifications(self, obj):
        clp_classifications = {}
        for hazard_statement in obj.reagent.hazard_statements.all():
            clp_classifications[hazard_statement.clp_classification_id] = {
                "id": hazard_statement.clp_classification_id,
                "repr": str(hazard_statement.clp_classification),
            }
        return list(clp_classifications.values())


class PersonalReagentCreateAsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonalReagent
        exclude = ["disposal_utilization_date", "is_usage_record_generated", "is_archived"]

    def validate(self, attrs):
        """Check that:
            1. When the main owner wants to add a personal reagent to a project/procedure, they must belong to it.
            2. Detailed location is present if the project/procedure name starts with "PB".
        """
        project_procedure = get_attr_value_for_validation(self, attrs, "project_procedure")
        main_owner = get_attr_value_for_validation(self, attrs, "main_owner")
        detailed_location = get_attr_value_for_validation(self, attrs, "detailed_location")

        if project_procedure is not None:
            if main_owner not in project_procedure.workers.all():
                raise serializers.ValidationError(detail={
                    "project_procedure": "Użytkownik musi być pracownikiem projektu/procedury, "
                                         "aby dodać lub modyfikować należący tam odczynnik osobisty."
                })
            if not detailed_location and project_procedure.name.startswith("PB"):
                raise serializers.ValidationError(detail={
                    "detailed_location": "Lokalizacja szczegółowa jest wymagana dla odczynników, "
                                         "które przypisane są do procedur badawczych, których nazwa zaczyna się na PB."
                })
        return attrs


class PersonalReagentCreateWithLabRoleSerializer(PersonalReagentCreateAsAdminSerializer):
    main_owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(PersonalReagentCreateAsAdminSerializer.Meta):
        pass


class PersonalReagentUpdateAsAdminProjectManagerFromProjectSerializer(
    PersonalReagentCreateAsAdminSerializer,
):
    class Meta:
        model = models.PersonalReagent
        fields = "__all__"


class PersonalReagentUpdateAsLabManagerNotOwnSerializer(PersonalReagentCreateAsAdminSerializer):
    class Meta:
        model = models.PersonalReagent
        fields = ["id", "main_owner", "is_archived", "disposal_utilization_date"]


class PersonalReagentUpdateAsLabManagerProjectManagerNotFromProjectLabWorkerSerializer(
    PersonalReagentUpdateAsAdminProjectManagerFromProjectSerializer,
):
    main_owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(PersonalReagentUpdateAsAdminProjectManagerFromProjectSerializer.Meta):
        pass


class PersonalViewSerializer(serializers.ModelSerializer):
    reagent = ReagentFieldReagentSerializer(read_only=True)
    producer = ReagentFieldProducerSerializer(source="reagent.producer", read_only=True)
    concentration = ReagentFieldConcentrationSerializer(source="reagent.concentration", read_only=True)
    purity_quality = ReagentFieldPurityQualitySerializer(source="reagent.purity_quality", read_only=True)
    catalog_no = serializers.CharField(source="reagent.catalog_no", read_only=True)
    is_usage_record_required = serializers.BooleanField(source="reagent.is_usage_record_required", read_only=True)
    project_procedure = ReagentFieldProjectProcedureSerializer(read_only=True)
    laboratory = ReagentFieldLaboratorySerializer(read_only=True)
    hazard_statements = ReagentFieldHazardStatementReadSerializer(
        source="reagent.hazard_statements", read_only=True, many=True
    )
    precautionary_statements = ReagentFieldPrecautionaryStatementSerializer(
        source="reagent.precautionary_statements", read_only=True, many=True
    )
    clp_classifications = serializers.SerializerMethodField()
    signal_word = serializers.SerializerMethodField()

    class Meta:
        model = models.PersonalReagent
        exclude = ["main_owner"]

    def get_clp_classifications(self, obj):
        clp_classifications = {}
        for hazard_statement in obj.reagent.hazard_statements.all():
            clp_classifications[hazard_statement.clp_classification_id] = {
                "id": hazard_statement.clp_classification_id,
                "repr": str(hazard_statement.clp_classification),
            }
        return list(clp_classifications.values())

    def get_signal_word(self, obj):
        # DANGER takes precedence over WARNING
        signal_word = ""
        signal_words = map(lambda x: x.signal_word, obj.reagent.hazard_statements.all())
        for sw in signal_words:
            if sw == models.HazardStatement.DANGER:
                return sw
            if sw == models.HazardStatement.WARNING:
                signal_word = sw

        return signal_word


class PersonalReagentHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)
    reagent = ReagentFieldReagentSerializer(read_only=True)
    main_owner = ReagentFieldUserSerializer(read_only=True)
    project_procedure = ReagentFieldProjectProcedureSerializer(read_only=True)
    laboratory = ReagentFieldLaboratorySerializer(read_only=True)

    class Meta:
        model = models.PersonalReagent.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class ReagentFieldsWithPendingValidationNotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    pk = serializers.IntegerField(read_only=True)
    table_name = serializers.CharField(read_only=True)
    value = serializers.CharField(read_only=True)


class ReagentsWithCloseExpirationDateNotificationSerializer(serializers.ModelSerializer):
    reagent_name = serializers.CharField(source="reagent.name", read_only=True)

    class Meta:
        model = models.PersonalReagent
        fields = ["id", "reagent_name", "expiration_date"]


class ReagentsWithNotGeneratedUsageRecordsNotificationSerializer(serializers.ModelSerializer):
    reagent_name = serializers.CharField(source="reagent.name", read_only=True)

    class Meta:
        model = models.PersonalReagent
        fields = ["id", "reagent_name"]


class ReagentsFewCriticalSerializer(serializers.Serializer):
    reagent_id = serializers.IntegerField(read_only=True)
    reagent_name = serializers.CharField(read_only=True)
    count = serializers.IntegerField(read_only=True)


class ReagentRequestsNotificationSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source="requester.username", read_only=True)
    reagent_name = serializers.CharField(source="personal_reagent.reagent.name", read_only=True)

    class Meta:
        model = models.ReagentRequest
        fields = ["id", "change_status_date", "requester_comment", "requester_name", "reagent_name"]


class ReagentRequestListSerializer(serializers.ModelSerializer):
    reagent_name = serializers.CharField(source="personal_reagent.reagent.name", read_only=True)
    class Meta:
        model = models.ReagentRequest
        fields = "__all__"


class ReagentRequestCurrentUserListSerializer(serializers.ModelSerializer):
    reagent_name = serializers.CharField(source="personal_reagent.reagent.name", read_only=True)
    class Meta:
        model = models.ReagentRequest
        exclude = ["requester"]


class ReagentRequestCreateSerializer(serializers.ModelSerializer):
    requester = serializers.HiddenField(default=serializers.CurrentUserDefault())
    change_status_date = serializers.HiddenField(default=timezone.now)

    class Meta:
        model = models.ReagentRequest
        fields = ["id", "requester", "personal_reagent", "change_status_date", "requester_comment"]
        extra_kwargs = {
            "personal_reagent": {"write_only": True},
            "requester_comment": {"write_only": True},
        }

    def validate(self, attrs):
        """Check that:
            1. The personal reagent doesn't belong to the requester and it's not already being requested (AA).
        """
        if attrs["requester"] == attrs["personal_reagent"].main_owner:
            raise serializers.ValidationError(detail={
                "personal_reagent": "Nie można wysłać zapytania o własny odczynnik."
            })
        if attrs["personal_reagent"].id in self.context["personal_reagents_with_aa_status"]:
            raise serializers.ValidationError(detail={
                "personal_reagent": "Ktoś wysłał już zapytanie o ten odczynnik."
            })
        return attrs


class ReagentRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReagentRequest
        fields = ["id", "requester_comment"]
        extra_kwargs = {
            "requester_comment": {"write_only": True},
        }


class ReagentRequestStatusChangeSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(models.ReagentRequest.FINAL_STATUS_CHOICES)
    change_status_date = serializers.HiddenField(default=timezone.now)

    class Meta:
        model = models.ReagentRequest
        fields = ["id", "status", "change_status_date", "responder_comment"]
        extra_kwargs = {
            "status": {"write_only": True},
            "responder_comment": {"write_only": True},
        }

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status == models.ReagentRequest.APPROVED:
            personal_reagent = instance.personal_reagent
            personal_reagent.main_owner = instance.requester
            personal_reagent.save(update_fields=["main_owner"])

        return instance


class ReagentRequestHistoricalRecordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="history_id", read_only=True)
    pk = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = models.ReagentRequest.history.model  # pylint: disable=no-member
        exclude = ["history_id"]


class UserManualGetSerializer(serializers.Serializer):
    user_manual = serializers.CharField(read_only=True)


class UserManualPutSerializer(serializers.Serializer):
    user_manual = serializers.FileField(write_only=True)

    def save(self, **kwargs):
        user_manual_path = kwargs["user_manual_path"]
        user_manual = self.validated_data["user_manual"]
        default_storage.save(user_manual_path, user_manual)
