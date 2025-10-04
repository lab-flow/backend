import datetime

from io import BytesIO
from itertools import chain
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

import pytest

from reportlab.pdfgen import canvas

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from reagents import models

# Mock the current date(time)
mock_timezone_now = timezone.now()
mock_datetime_date_today = datetime.date.today()


@pytest.fixture(autouse=True)
def media_settings(settings):  # pylint: disable=redefined-outer-name
    """Changing media settings for easier cleanup after test invocations."""
    settings.MEDIA_ROOT = settings.BASE_DIR / "reagents" / "tests" / "media"
    settings.MEDIA_URL = 'media/'


def assert_timezone_now_gte_datetime(date_time):
    assert date_time is not None
    if isinstance(date_time, str):
        assert timezone.localtime(timezone.now()).strftime(settings.REST_FRAMEWORK["DATETIME_FORMAT"]) >= date_time
    else:
        assert timezone.now() >= date_time


def compare_expected_actual(expected, actual):
    assert isinstance(expected, dict)
    assert isinstance(actual, dict)

    longer_keys = expected.keys() if len(expected) >= len(actual) else actual.keys()
    missing_expected_values = []
    missing_actual_values = []
    not_equal_fields = []
    for k in longer_keys:
        print(f"Key: {k}")
        try:
            expected_value = expected[k]
        except KeyError:
            missing_expected_values.append(k)
            expected_value = "NO_EXPECTED_VALUE"
        try:
            actual_value = actual[k]
        except KeyError:
            missing_actual_values.append(k)
            actual_value = "NO_ACTUAL_VALUE"

        print(f"E type: {type(expected_value)}")
        print(f"A type: {type(actual_value)}")
        print(f"E: {expected_value}")
        print(f"A: {actual_value}")
        are_fields_equal = expected_value == actual_value
        print(f"Equal: {are_fields_equal}\n")
        if not are_fields_equal:
            not_equal_fields.append(k)

    print(f"Missing {len(missing_expected_values)} expected values: {missing_expected_values}")
    print(f"Missing {len(missing_actual_values)} actual values: {missing_actual_values}\n")
    print(
        "All fields values are equal!" if len(not_equal_fields) == 0 else f"Fields values mismatch: {not_equal_fields}"
    )

@pytest.fixture
def mock_files():
    # Mock a pictogram
    image = Image.new("RGB", (250, 250))
    image_buffer = BytesIO()
    image.save(image_buffer, "PNG")
    image_bytes = image_buffer.getvalue()

    # Mock a PDF file
    pdf_buffer = BytesIO()
    p = canvas.Canvas(pdf_buffer)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    p.save()
    pdf_buffer.seek(0)
    pdf_bytes = pdf_buffer.getvalue()

    return image_bytes, pdf_bytes


def model_to_dict(instance, fields=None, exclude=None):
    """A modified version of the django.forms.models.model_to_dict function.
    Allows to retrieve primary keys of both ForeignKey and ManyToMany fields.
    Also, it doesn't remove non-editable fields.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


@pytest.fixture
def api_client_admin():
    admin = models.User.objects.create_superuser(
        username="IŁ",
        email="il@il.pl",
        password="MKZPQL9J",
        first_name="Ignacy",
        last_name="Łukasiewicz",
    )
    client = APIClient()
    refresh = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client, admin


@pytest.fixture
def api_client_lab_manager():
    lab_manager = models.User.objects.create_user(
        username="MSC",
        email="msc@msc.pl",
        password="JU8YP2LJ",
        first_name="Maria",
        last_name="Skłodowska-Curie",
        lab_roles=[models.User.LAB_MANAGER],
    )
    client = APIClient()
    refresh = RefreshToken.for_user(lab_manager)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client, lab_manager


@pytest.fixture
def api_client_project_manager():
    project_manager = models.User.objects.create_user(
        username="KO",
        email="ko@ko.pl",
        password="THC1HBY3",
        first_name="Karol",
        last_name="Olszewski",
        lab_roles=[models.User.PROJECT_MANAGER],
    )
    client = APIClient()
    refresh = RefreshToken.for_user(project_manager)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client, project_manager


@pytest.fixture
def api_client_lab_worker():
    lab_worker = models.User.objects.create_user(
        username="ZW",
        email="zw@zw.pl",
        password="WT4F8LI9",
        first_name="Zygmunt",
        last_name="Wróblewski",
        lab_roles=[models.User.LAB_WORKER],
    )
    client = APIClient()
    refresh = RefreshToken.for_user(lab_worker)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client, lab_worker


@pytest.fixture
def api_client_anon():
    client = APIClient()

    return client


@pytest.fixture
def reagent_types():
    type1 = models.ReagentType.objects.create(
        type="odczynnik chemiczny",
        is_validated_by_admin=False,
    )
    type2 = models.ReagentType.objects.create(
        type="zestaw odczynników",
        is_validated_by_admin=True,
    )
    type3 = models.ReagentType.objects.create(
        type="preparat dezynfekcyjny",
        is_validated_by_admin=True,
    )

    return type1, type2, type3


@pytest.fixture
def producers():
    producer1 = models.Producer.objects.create(
        producer_name="AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
        brand_name="POCH",
        abbreviation="POCH",
        is_validated_by_admin=False,
    )

    producer2 = models.Producer.objects.create(
        producer_name="THERMO FISHER SCIENTIFIC",
        brand_name="THERMO FISHER SCIENTIFIC",
        abbreviation="THERMO",
        is_validated_by_admin=True,
    )

    return producer1, producer2


@pytest.fixture
def concentrations():
    concentration1 = models.Concentration.objects.create(
        concentration="99,80%",
        is_validated_by_admin=False,
    )
    concentration2 = models.Concentration.objects.create(
        concentration="0,1 M",
        is_validated_by_admin=True,
    )

    return concentration1, concentration2


@pytest.fixture
def safety_instructions(mock_files):  # pylint: disable=redefined-outer-name
    _, pdf_bytes = mock_files
    safety_instruction1 = models.SafetyInstruction.objects.create(
        safety_instruction=SimpleUploadedFile("si1.pdf", pdf_bytes),
        name="IB0001",
        reagent_name="alkohol",
        is_validated_by_admin=True,
    )
    safety_instruction2 = models.SafetyInstruction.objects.create(
        safety_instruction=SimpleUploadedFile("si2.pdf", pdf_bytes),
        name="IB0002",
        reagent_name="Decontaminant",
        is_validated_by_admin=True,
    )

    return safety_instruction1, safety_instruction2


@pytest.fixture
def safety_data_sheets(mock_files):  # pylint: disable=redefined-outer-name
    _, pdf_bytes = mock_files
    safety_data_sheet1 = models.SafetyDataSheet.objects.create(
        safety_data_sheet=SimpleUploadedFile("sds1.pdf", pdf_bytes),
        name="SDS0001",
        reagent_name="alkohol",
        is_validated_by_admin=True,
    )
    safety_data_sheet2 = models.SafetyDataSheet.objects.create(
        safety_data_sheet=SimpleUploadedFile("sds2.pdf", pdf_bytes),
        name="SDS0002",
        reagent_name="Decontaminant",
        is_validated_by_admin=True,
    )

    return safety_data_sheet1, safety_data_sheet2


@pytest.fixture
def units():
    unit1 = models.Unit.objects.create(
        unit="preps",
        is_validated_by_admin=False,
    )
    unit2 = models.Unit.objects.create(
        unit="mL",
        is_validated_by_admin=True,
    )

    return unit1, unit2


@pytest.fixture
def purities_qualities():
    purity_quality1 = models.PurityQuality.objects.create(
        purity_quality="CZDA basic",
        is_validated_by_admin=False,
    )
    purity_quality2 = models.PurityQuality.objects.create(
        purity_quality="molecular biology grade",
        is_validated_by_admin=True,
    )

    return purity_quality1, purity_quality2


@pytest.fixture
def storage_conditions():
    storage_condition1 = models.StorageCondition.objects.create(
        storage_condition="RT",
        is_validated_by_admin=False,
    )
    storage_condition2 = models.StorageCondition.objects.create(
        storage_condition="chronić przed światłem",
        is_validated_by_admin=True,
    )

    return storage_condition1, storage_condition2


@pytest.fixture
def clp_classifications():
    clp_classification1 = models.ClpClassification.objects.create(
        classification="Substancje łatwopalne",
        clp_classification="GHS02",
        hazard_group="PHY",
    )
    clp_classification2 = models.ClpClassification.objects.create(
        classification="Substancje drażniące",
        clp_classification="GHS07",
        hazard_group="HEA",
    )

    return clp_classification1, clp_classification2


@pytest.fixture
def pictograms(mock_files):  # pylint: disable=redefined-outer-name
    image_bytes, _ = mock_files

    pictogram1 = models.Pictogram.objects.create(
        pictogram=SimpleUploadedFile("GHS02.png", image_bytes),
    )
    pictogram2 = models.Pictogram.objects.create(
        pictogram=SimpleUploadedFile("GHS07.png", image_bytes),
    )

    return pictogram1, pictogram2


@pytest.fixture
def hazard_statements(clp_classifications, pictograms):  # pylint: disable=redefined-outer-name
    clp_classification1, clp_classification2 = clp_classifications
    pictogram1, pictogram2 = pictograms

    hazard_statement1 = models.HazardStatement.objects.create(
        hazard_class="Gazy łatwopalne",
        clp_classification=clp_classification1,
        pictogram=pictogram1,
        hazard_category="Niestabilne materiały wybuchowe",
        hazard_and_category_code="Unst. Expl",
        signal_word="DGR",
        code="H200",
        phrase="Materiały wybuchowe niestabilne.",
        is_usage_record_required=False,
    )
    hazard_statement2 = models.HazardStatement.objects.create(
        hazard_class="Toksyczność ostra - Droga pokarmowa",
        clp_classification=clp_classification2,
        pictogram=pictogram2,
        hazard_category="kategoria 4",
        hazard_and_category_code="Acute Tox. 4",
        signal_word="WRN",
        code="H302",
        phrase="Działa szkodliwie po połknięciu.",
        is_usage_record_required=False,
    )

    return hazard_statement1, hazard_statement2


@pytest.fixture
def precautionary_statements():
    precautionary_statement1 = models.PrecautionaryStatement.objects.create(
        code="P201",
        phrase="Przed użyciem zapoznać się ze specjalnymi środkami ostrożności."
    )
    precautionary_statement2 = models.PrecautionaryStatement.objects.create(
        code="P250",
        phrase="Nie poddawać szlifowaniu/wstrząsom/tarciu/….",
    )

    return precautionary_statement1, precautionary_statement2


@pytest.fixture
# pylint: disable=redefined-outer-name
def reagents(reagent_types, producers, concentrations, safety_instructions, safety_data_sheets, units,
             purities_qualities, storage_conditions, hazard_statements, precautionary_statements):
# pylint: enable=redefined-outer-name
    type1, type2, _ = reagent_types
    producer1, producer2 = producers
    concentration1, _ = concentrations
    safety_instruction1, safety_instruction2 = safety_instructions
    safety_data_sheet1, safety_data_sheet2 = safety_data_sheets
    concentration1, _ = concentrations
    unit1, unit2 = units
    purity_quality1, _ = purities_qualities
    storage_condition1, storage_condition2 = storage_conditions
    hazard_statement1, hazard_statement2 = hazard_statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    reagent1 = models.Reagent.objects.create(
        type=type1,
        producer=producer1,
        name="alkohol etylowy bezwodny",
        catalog_no="BA6480111",
        concentration=concentration1,
        volume=1,
        unit=unit1,
        purity_quality=purity_quality1,
        safety_instruction=safety_instruction1,
        safety_data_sheet=safety_data_sheet1,
        is_usage_record_required=True,
        is_validated_by_admin=True,
    )
    reagent1.storage_conditions.add(storage_condition1.id)
    reagent1.hazard_statements.add(hazard_statement1.id, hazard_statement2.id)
    reagent1.precautionary_statements.add(precautionary_statement1.id, precautionary_statement2.id)

    reagent2 = models.Reagent.objects.create(
        type=type2,
        producer=producer2,
        name="DNA AWAY™ Surface Decontaminant",
        catalog_no="7010PK",
        volume=1,
        unit=unit2,
        safety_instruction=safety_instruction2,
        safety_data_sheet=safety_data_sheet2,
        is_usage_record_required=False,
        is_validated_by_admin=False,
    )
    reagent2.storage_conditions.add(storage_condition2.id)
    reagent2.hazard_statements.add(hazard_statement2.id)

    return reagent1, reagent2


@pytest.fixture
# pylint: disable=redefined-outer-name
def projects_procedures(api_client_lab_manager, api_client_project_manager, api_client_lab_worker):
# pylint: enable=redefined-outer-name
    _, lab_manager = api_client_lab_manager
    _, project_manager = api_client_project_manager
    _, lab_worker = api_client_lab_worker

    project_procedure1 = models.ProjectProcedure.objects.create(
        name="PB01 - psy i koty",
        manager=project_manager,
        is_validated_by_admin=True,
    )
    project_procedure1.workers.add(project_manager.id, lab_worker.id)

    project_procedure2 = models.ProjectProcedure.objects.create(
        name="PB02 - owce",
        manager=project_manager,
        is_validated_by_admin=False,
    )
    project_procedure2.workers.add(project_manager.id, lab_worker.id, lab_manager.id)

    return project_procedure1, project_procedure2


@pytest.fixture
# pylint: disable=redefined-outer-name
def laboratories():
# pylint: enable=redefined-outer-name
    laboratory1 = models.Laboratory.objects.create(
        laboratory="LGM",
    )
    laboratory2 = models.Laboratory.objects.create(
        laboratory="LG",
    )

    return laboratory1, laboratory2


@pytest.fixture
# pylint: disable=redefined-outer-name
def personal_reagents(api_client_admin, api_client_lab_manager, api_client_lab_worker, reagents, projects_procedures,
                      laboratories, mock_files):
# pylint: enable=redefined-outer-name
    _, _ = mock_files
    _, admin = api_client_admin
    _, lab_manager = api_client_lab_manager
    _, lab_worker = api_client_lab_worker
    reagent1, reagent2 = reagents
    project_procedure1, _ = projects_procedures
    laboratory1, laboratory2 = laboratories

    personal_reagent1 = models.PersonalReagent.objects.create(
        reagent=reagent1,
        project_procedure=project_procedure1,
        is_critical=True,
        main_owner=lab_worker,
        lot_no="2000/02/03",
        receipt_purchase_date=mock_datetime_date_today,
        opening_date=mock_datetime_date_today + datetime.timedelta(days=1),
        expiration_date=mock_datetime_date_today + datetime.timedelta(days=3),
        laboratory=laboratory1,
        room="315",
        detailed_location="Lodówka D17",
        user_comment="Bardzo ważny odczynnik.",
        is_usage_record_generated=False,
    )
    personal_reagent2 = models.PersonalReagent.objects.create(
        reagent=reagent1,
        is_critical=False,
        main_owner=lab_worker,
        lot_no="1000/01/01",
        receipt_purchase_date=mock_datetime_date_today - datetime.timedelta(days=30),
        expiration_date=mock_datetime_date_today + datetime.timedelta(days=6),
        laboratory=laboratory2,
        room="314",
        detailed_location="Lodówka A0",
        user_comment="",
        is_usage_record_generated=False,
    )
    personal_reagent3 = models.PersonalReagent.objects.create(
        reagent=reagent2,
        is_critical=True,
        main_owner=admin,
        lot_no="4000/01/30",
        receipt_purchase_date=mock_datetime_date_today - datetime.timedelta(days=15),
        expiration_date=mock_datetime_date_today + datetime.timedelta(days=20),
        laboratory=laboratory2,
        room="314",
        detailed_location="Lodówka C3",
        user_comment="",
        is_usage_record_generated=False,
    )
    personal_reagent4 = models.PersonalReagent.objects.create(
        reagent=reagent2,
        project_procedure=project_procedure1,
        is_critical=False,
        main_owner=lab_manager,
        lot_no="1000/01/01",
        receipt_purchase_date=mock_datetime_date_today - datetime.timedelta(days=60),
        expiration_date=mock_datetime_date_today - datetime.timedelta(days=45),
        disposal_utilization_date=mock_datetime_date_today - datetime.timedelta(days=46),
        laboratory=laboratory1,
        room="315",
        detailed_location="Lodówka D17",
        is_archived=True,
        user_comment="Mało ważny odczynnik.",
        is_usage_record_generated=False,
    )

    return personal_reagent1, personal_reagent2, personal_reagent3, personal_reagent4
