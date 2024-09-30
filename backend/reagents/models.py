from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from reagents import validators


class User(AbstractUser):
    username_validator = validators.PolishAlphabetUsernameValidator()
    username = models.CharField(
        "nazwa użytkownika (inicjały)",
        max_length=4,
        unique=True,
        help_text="Wymagane. 2 to 4 liter. Tylko wielkie litery z polskiego alfabetu.",
        validators=[username_validator],
        error_messages={
            "unique": "Użytkownik z taką nazwą już istnieje.",
        },
    )
    email = models.EmailField(unique=True)

    LAB_MANAGER = "LM"
    PROJECT_MANAGER = "PM"
    LAB_WORKER = "LW"
    LAB_ROLES = [
        (LAB_MANAGER, "Kierownik laboratorium"),
        (PROJECT_MANAGER, "Kierownik projektu (procedury)"),
        (LAB_WORKER, "Pracownik laboratorium"),
    ]
    LAB_ROLES_VALUES = set(map(lambda x: x[0], LAB_ROLES))
    lab_roles = ArrayField(
        models.CharField(
            max_length=2,
            choices=LAB_ROLES,
        ),
        default=list,
        blank=True,
    )
    history = HistoricalRecords(excluded_fields=["password"], user_db_constraint=False)

    class Meta(AbstractUser.Meta):
        ordering = ["id"]


class ReagentType(models.Model):
    type = models.CharField(max_length=50, unique=True)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.type

    class Meta:
        db_table = "reagents_reagent_type"
        ordering = ["id"]


class Producer(models.Model):
    producer_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=25)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return f"[{self.abbreviation}] [{self.brand_name}] {self.producer_name}"

    class Meta:
        ordering = ["id"]


class Concentration(models.Model):
    concentration = models.CharField(max_length=20, unique=True)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.concentration


class Unit(models.Model):
    unit = models.CharField(max_length=5, unique=True)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.unit

    class Meta:
        ordering = ["id"]


class PurityQuality(models.Model):
    purity_quality = models.CharField(max_length=30, unique=True)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.purity_quality

    class Meta:
        db_table = "reagents_purity_quality"
        ordering = ["id"]


class StorageCondition(models.Model):
    storage_condition = models.CharField(max_length=30, unique=True)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.storage_condition

    class Meta:
        db_table = "reagents_storage_condition"
        ordering = ["id"]


class ClpClassification(models.Model):
    classification = models.CharField(max_length=40, blank=True)
    clp_classification_validator = validators.ClpClassificationValidator()
    clp_classification = models.CharField(max_length=5, validators=[clp_classification_validator])

    PHYSICAL = "PHY"
    HEALTH = "HEA"
    ENVIRONMENTAL = "ENV"
    ADDITIONAL = "ADD"
    HAZARD_GROUPS = [
        (PHYSICAL, "Zagrożenia fizyczne"),
        (HEALTH, "Zagrożenia dla zdrowia"),
        (ENVIRONMENTAL, "Zagrożenia dla środowiska"),
        (ADDITIONAL, "Dodatkowe zagrożenia")
    ]
    HAZARD_GROUPS_VALUES = set(map(lambda x: x[0], HAZARD_GROUPS))
    hazard_group = models.CharField(max_length=3, choices=HAZARD_GROUPS)
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.clp_classification

    class Meta:
        db_table = "reagents_clp_classification"
        ordering = ["id"]


class Pictogram(models.Model):
    pictogram = models.ImageField(upload_to="Pictograms", unique=True)
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return str(self.pictogram)

    class Meta:
        ordering = ["id"]


class HazardStatement(models.Model):
    hazard_class = models.CharField(max_length=100)
    clp_classification = models.ForeignKey(ClpClassification, on_delete=models.PROTECT, null=True, blank=True)
    pictogram = models.ForeignKey(Pictogram, on_delete=models.PROTECT, null=True, blank=True)
    hazard_category = models.CharField(max_length=50)
    hazard_and_category_code = models.CharField(max_length=30)

    DANGER = "DGR"
    WARNING = "WRN"
    SIGNAL_WORDS = [
        (DANGER, "Niebezpieczeństwo (danger)"),
        (WARNING, "Uwaga"),
    ]
    signal_word = models.CharField(max_length=3, choices=SIGNAL_WORDS, blank=True)

    code_validator = validators.HazardStatementCodeValidator()
    code = models.CharField(max_length=30, blank=True, validators=[code_validator])
    phrase = models.CharField(max_length=200, blank=True)
    is_usage_record_required = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.code

    class Meta:
        db_table = "reagents_hazard_statement"
        ordering = ["id"]


class PrecautionaryStatement(models.Model):
    code_validator = validators.PrecautionaryStatementCodeValidator()
    code = models.CharField(max_length=30, blank=True, validators=[code_validator])
    phrase = models.CharField(max_length=200, blank=True)
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.code

    class Meta:
        db_table = "reagents_precautionary_statement"
        ordering = ["id"]


class SafetyDataSheet(models.Model):
    safety_data_sheet = models.FileField(upload_to="SafetyDataSheets")

    name_validator = validators.SafetyDataSheetNameValidator()
    name = models.CharField(max_length=7, validators=[name_validator])

    reagent_name = models.CharField(max_length=100)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "reagents_safety_data_sheet"
        ordering = ["id"]


class SafetyInstruction(models.Model):
    safety_instruction = models.FileField(upload_to="SafetyInstructions")

    name_validator = validators.SafetyInstructionNameValidator()
    name = models.CharField(max_length=6, validators=[name_validator])

    reagent_name = models.CharField(max_length=100)
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "reagents_safety_instruction"
        ordering = ["id"]


class Reagent(models.Model):
    type = models.ForeignKey(ReagentType, on_delete=models.PROTECT)
    producer = models.ForeignKey(Producer, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    catalog_no = models.CharField(max_length=50)
    concentration = models.ForeignKey(Concentration, on_delete=models.PROTECT, null=True, blank=True)
    volume = models.PositiveIntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    purity_quality = models.ForeignKey(PurityQuality, on_delete=models.PROTECT, null=True, blank=True)
    storage_conditions = models.ManyToManyField(StorageCondition)
    hazard_statements = models.ManyToManyField(HazardStatement, blank=True)
    precautionary_statements = models.ManyToManyField(PrecautionaryStatement, blank=True)
    safety_data_sheet = models.ForeignKey(SafetyDataSheet, on_delete=models.PROTECT)
    safety_instruction = models.ForeignKey(SafetyInstruction, on_delete=models.PROTECT, null=True, blank=True)
    cas_no = models.CharField(max_length=50, blank=True)
    other_info = models.CharField(max_length=200, blank=True)
    kit_contents = models.CharField(max_length=300, blank=True)
    is_usage_record_required = models.BooleanField()
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(
        m2m_fields=[storage_conditions, hazard_statements, precautionary_statements],
        user_db_constraint=False,
    )

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.name

    class Meta:
        ordering = ["id"]


class ProjectProcedure(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="manager_project_procedure_set",
    )
    workers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="workers_project_procedure_set",
    )
    is_validated_by_admin = models.BooleanField()
    history = HistoricalRecords(m2m_fields=[workers], user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.name

    class Meta:
        db_table = "reagents_project_procedure"
        ordering = ["id"]


class Laboratory(models.Model):
    laboratory = models.CharField(max_length=30, unique=True)
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.laboratory

    class Meta:
        ordering = ["id"]


class PersonalReagent(models.Model):
    reagent = models.ForeignKey(Reagent, on_delete=models.PROTECT)
    project_procedure = models.ForeignKey(ProjectProcedure, on_delete=models.PROTECT, null=True, blank=True)
    is_critical = models.BooleanField()
    main_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    lot_no = models.CharField(max_length=20)
    receipt_purchase_date = models.DateField()
    opening_date = models.DateField(null=True, blank=True, default=None)
    expiration_date = models.DateField()
    disposal_utilization_date = models.DateField(null=True, blank=True, default=None)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.PROTECT)
    room = models.CharField(max_length=8)
    detailed_location = models.CharField(max_length=20, blank=True)
    is_usage_record_generated = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    user_comment = models.CharField(max_length=200, blank=True)
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return f"[{self.main_owner}] {self.reagent}"

    class Meta:
        db_table = "reagents_personal_reagent"
        ordering = ["id"]


class ReagentRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    personal_reagent = models.ForeignKey(PersonalReagent, on_delete=models.PROTECT)
    AWAITING_APPROVAL = "AA"
    APPROVED = "AP"
    REJECTED = "RE"
    INITIAL_STATUS_CHOICE = (AWAITING_APPROVAL, "Oczekiwanie na akceptację")
    FINAL_STATUS_CHOICES = [
        (APPROVED, "Zaakceptowano"),
        (REJECTED, "Odrzucono")
    ]
    STATUS_CHOICES = [INITIAL_STATUS_CHOICE] + FINAL_STATUS_CHOICES
    STATUS_CHOICES_VALUES = set(map(lambda x: x[0], STATUS_CHOICES))
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=INITIAL_STATUS_CHOICE[0],
    )
    change_status_date = models.DateTimeField(default=timezone.now)
    requester_comment = models.CharField(max_length=200, blank=True)
    responder_comment = models.CharField(max_length=200, blank=True)
    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return f"[{self.change_status_date}] {self.status}"

    class Meta:
        db_table = "reagents_reagent_request"
        ordering = ["id"]
