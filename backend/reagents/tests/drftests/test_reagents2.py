"""This file tests Producer, ReagentType, Concentration, Unit, PurityQuality, StorageCondition and Reagent."""

import json

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status

from reagents.models import Producer, ReagentType, Concentration, Unit, PurityQuality, StorageCondition, Reagent
from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, model_to_dict


@pytest.mark.django_db
def test_retrieve_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                           api_client_anon, reagent_types, producers, concentrations, units, purities_qualities,
                           storage_conditions, hazard_statements, precautionary_statements, reagents):
    # Reagent types
    reagent_type1, _, _ = reagent_types

    client, _ = api_client_admin
    url = reverse("reagenttype-detail", args=[reagent_type1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent_type1.id,
        "type": "odczynnik chemiczny",
        "is_validated_by_admin": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Producers
    producer1, _ = producers

    client, _ = api_client_admin
    url = reverse("producer-detail", args=[producer1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": producer1.id,
        "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
        "brand_name": "POCH",
        "abbreviation": "POCH",
        "is_validated_by_admin": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Concentrations
    concentration1, _ = concentrations

    client, _ = api_client_admin
    url = reverse("concentration-detail", args=[concentration1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": concentration1.id,
        "concentration": "99,80%",
        "is_validated_by_admin": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Units
    unit1, _ = units

    client, _ = api_client_admin
    url = reverse("unit-detail", args=[unit1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": unit1.id,
        "unit": "preps",
        "is_validated_by_admin": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Purities/Qualities
    purity_quality1, _ = purities_qualities

    client, _ = api_client_admin
    url = reverse("purityquality-detail", args=[purity_quality1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
            "id": purity_quality1.id,
            "purity_quality": "CZDA basic",
            "is_validated_by_admin": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Storage conditions
    storage_condition1, _ = storage_conditions

    client, _ = api_client_admin
    url = reverse("storagecondition-detail", args=[storage_condition1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
            "id": storage_condition1.id,
            "storage_condition": "RT",
            "is_validated_by_admin": False,
    }
    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Reagents
    reagent1, _ = reagents
    hazard_statement1, hazard_statement2 = hazard_statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    client, _ = api_client_admin
    url = reverse("reagent-detail", args=[reagent1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": reagent1.id,
        "type": {
            "id": reagent_type1.id,
            "repr": reagent_type1.type,
        },
        "producer": {
            "id": producer1.id,
            "repr": producer1.abbreviation,
        },
        "name": "alkohol etylowy bezwodny",
        "catalog_no": "BA6480111",
        "concentration": {
            "id": concentration1.id,
            "repr": concentration1.concentration,
        },
        "volume": 1,
        "unit": {
            "id": unit1.id,
            "repr": unit1.unit,
        },
        "purity_quality": {
            "id": purity_quality1.id,
            "repr": purity_quality1.purity_quality,
        },
        "storage_conditions": [
            {
                "id": storage_condition1.id,
                "repr": storage_condition1.storage_condition,
            },
        ],
        "hazard_statements": [
            {
                "id": hazard_statement1.id,
                "repr": hazard_statement1.code,
            },
            {
                "id": hazard_statement2.id,
                "repr": hazard_statement2.code,
            },
        ],
        "precautionary_statements": [
            {
                "id": precautionary_statement1.id,
                "repr": precautionary_statement1.code,
            },
            {
                "id": precautionary_statement2.id,
                "repr": precautionary_statement2.code,
            },
        ],
        "safety_instruction_name": "IB0001",
        "safety_data_sheet_name": "SDS0001",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
        "is_validated_by_admin": True,
    }

    response_data_results = response.data

    safety_instruction_name = response_data_results.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_name = response_data_results.pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")
    assert safety_data_sheet_name.startswith("sds1")
    assert safety_data_sheet_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data

    safety_instruction_name = response_data_results.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_name = response_data_results.pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")
    assert safety_data_sheet_name.startswith("sds1")
    assert safety_data_sheet_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data

    safety_instruction_name = response_data_results.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_name = response_data_results.pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")
    assert safety_data_sheet_name.startswith("sds1")
    assert safety_data_sheet_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data

    safety_instruction_name = response_data_results.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_name = response_data_results.pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")
    assert safety_data_sheet_name.startswith("sds1")
    assert safety_data_sheet_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                         api_client_anon, reagent_types, producers, concentrations, units, purities_qualities,
                         storage_conditions, hazard_statements, precautionary_statements, reagents, mock_files):
    # pylint: disable=no-member
    ReagentType.history.all().delete()
    Producer.history.all().delete()
    Concentration.history.all().delete()
    Unit.history.all().delete()
    PurityQuality.history.all().delete()
    StorageCondition.history.all().delete()
    Reagent.history.all().delete()
    # pylint: enable=no-member

    _, pdf_bytes = mock_files

    # Reagent types
    reagent_type1, _, _ = reagent_types

    client, admin = api_client_admin
    url = reverse("reagenttype-detail", args=[reagent_type1.id])

    put_data = {
        "type": "odczynnik hiperspecjalny",
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    db_reagent_type = ReagentType.objects.get(pk=response.data["id"])

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_reagent_type.id,
    }

    put_data["id"] = reagent_type1.id

    assert put_data == model_to_dict(db_reagent_type)

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Producers
    producer1, _ = producers

    client, _ = api_client_admin
    url = reverse("producer-detail", args=[producer1.id])

    put_data = {
        "producer_name": "TH GEYER POLSKA Sp. z o.o.",
        "brand_name": "TH GEYER",
        "abbreviation": "TH GEYER",
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    db_producer = Producer.objects.get(pk=response.data["id"])

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_producer.id,
    }

    put_data["id"] = producer1.id

    assert put_data == model_to_dict(db_producer)

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Concentration
    concentration1, _ = concentrations

    client, _ = api_client_admin
    url = reverse("concentration-detail", args=[concentration1.id])

    put_data = {
        "concentration": "100X",
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    db_concentration = Concentration.objects.get(pk=response.data["id"])

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_concentration.id,
    }

    put_data["id"] = concentration1.id

    assert put_data == model_to_dict(db_concentration)

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Units
    unit1, _ = units

    client, _ = api_client_admin
    url = reverse("unit-detail", args=[unit1.id])

    put_data = {
        "unit": "preps",
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    db_unit = Unit.objects.get(pk=response.data["id"])

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_unit.id,
    }

    put_data["id"] = unit1.id

    assert put_data == model_to_dict(db_unit)

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Purities/Qualities
    purity_quality1, _ = purities_qualities

    client, _ = api_client_admin
    url = reverse("purityquality-detail", args=[purity_quality1.id])

    put_data = {
        "purity_quality": "PCR-grade",
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    db_purity_quality = PurityQuality.objects.get(pk=response.data["id"])

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_purity_quality.id,
    }

    put_data["id"] = purity_quality1.id

    assert put_data == model_to_dict(db_purity_quality)

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Storage conditions
    storage_condition1, _ = storage_conditions

    client, _ = api_client_admin
    url = reverse("storagecondition-detail", args=[storage_condition1.id])

    put_data = {
        "storage_condition": "zawsze pionowo",
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    db_storage_condition = StorageCondition.objects.get(pk=response.data["id"])

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_storage_condition.id,
    }

    put_data["id"] = storage_condition1.id

    assert put_data == model_to_dict(db_storage_condition)

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Reagents
    reagent1, _ = reagents
    hazard_statement1, hazard_statement2 = hazard_statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    client, _ = api_client_admin
    url = reverse("reagent-detail", args=[reagent1.id])

    put_data = {
        "type": reagent_type1.id,
        "producer": producer1.id,
        "name": "alkohol etylowy bezwodny",
        "catalog_no": "BA6480111",
        "volume": 1,
        "unit": unit1.id,
        "storage_conditions": [storage_condition1.id],
        "hazard_statements": [hazard_statement1.id, hazard_statement2.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_data_sheet": SimpleUploadedFile("sds1.pdf", pdf_bytes),
        "is_usage_record_required": True,
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    db_reagent = Reagent.objects.get(pk=response.data["id"])

    put_data["concentration"] = reagent1.concentration.id
    put_data["purity_quality"] = reagent1.purity_quality.id
    put_data["safety_instruction_name"] = reagent1.safety_instruction_name
    put_data["safety_data_sheet_name"] = reagent1.safety_data_sheet_name
    put_data["cas_no"] = reagent1.cas_no
    put_data["other_info"] = reagent1.other_info
    put_data["kit_contents"] = reagent1.kit_contents
    # Dropping files due to random suffixes
    put_data.pop("safety_data_sheet")

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_reagent.id,
    }
    history_data1["type"] = {
        "id": db_reagent_type.id,
        "repr": db_reagent_type.type,
    }
    history_data1["producer"] = {
        "id": db_producer.id,
        "repr": db_producer.abbreviation,
    }
    history_data1["concentration"] = {
        "id": db_concentration.id,
        "repr": db_concentration.concentration,
    }
    history_data1["unit"] = {
        "id": db_unit.id,
        "repr": db_unit.unit,
    }
    history_data1["purity_quality"] = {
        "id": db_purity_quality.id,
        "repr": db_purity_quality.purity_quality,
    }
    history_data1["storage_conditions"] = [
        {
            "id": db_storage_condition.id,
            "repr": db_storage_condition.storage_condition,
        },
    ]
    history_data1["hazard_statements"] = [
        {
            "id": hazard_statement1.id,
            "repr": hazard_statement1.code,
        },
        {
            "id": hazard_statement2.id,
            "repr": hazard_statement2.code,
        },
    ]
    history_data1["precautionary_statements"] = [
        {
            "id": precautionary_statement1.id,
            "repr": precautionary_statement1.code,
        },
        {
            "id": precautionary_statement2.id,
            "repr": precautionary_statement2.code,
        },
    ]

    put_data["id"] = reagent1.id

    db_reagent_dict = model_to_dict(db_reagent)
    safety_instruction_filename = str(db_reagent_dict.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = str(db_reagent_dict.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    assert put_data == db_reagent_dict

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = [""]
    safety_data_sheets = ["sds1"]
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, safety_instructions, safety_data_sheets
    ):
        safety_instruction_filename = str(history_row.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
        safety_data_sheet_filename = str(history_row.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

        assert safety_instruction_filename.startswith(safety_instruction)
        assert safety_instruction_filename.endswith(".pdf") or not safety_instruction_filename
        assert safety_data_sheet_filename.startswith(safety_data_sheet)
        assert safety_data_sheet_filename.endswith(".pdf")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # `is_usage_record_required` can't set to False when any of the hazard statements requires it to be set to True
    hazard_statement1.is_usage_record_required = True
    hazard_statement1.save()

    client, _ = api_client_admin

    put_data = {
        "type": reagent_type1.id,
        "producer": producer1.id,
        "name": "alkohol etylowy bezwodny",
        "catalog_no": "BA6480111",
        "volume": 1,
        "unit": unit1.id,
        "storage_conditions": [storage_condition1.id],
        "hazard_statements": [hazard_statement1.id, hazard_statement2.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si1.pdf", pdf_bytes),
        "safety_instruction_name": "IB0001",
        "safety_data_sheet": SimpleUploadedFile("sds1.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0001",
        "is_usage_record_required": False,
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Wrong safety_instruction_name
    put_data = {
        "type": reagent_type1.id,
        "producer": producer1.id,
        "name": "alkohol etylowy bezwodny",
        "catalog_no": "BA6480111",
        "volume": 1,
        "unit": unit1.id,
        "storage_conditions": [storage_condition1.id],
        "hazard_statements": [hazard_statement1.id, hazard_statement2.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si1.pdf", pdf_bytes),
        "safety_instruction_name": "IB001",
        "safety_data_sheet": SimpleUploadedFile("sds1.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0001",
        "is_usage_record_required": False,
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Wrong safety_data_sheet_name
    put_data = {
        "type": reagent_type1.id,
        "producer": producer1.id,
        "name": "alkohol etylowy bezwodny",
        "catalog_no": "BA6480111",
        "volume": 1,
        "unit": unit1.id,
        "storage_conditions": [storage_condition1.id],
        "hazard_statements": [hazard_statement1.id, hazard_statement2.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si1.pdf", pdf_bytes),
        "safety_instruction_name": "IB0001",
        "safety_data_sheet": SimpleUploadedFile("sds1.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS123",
        "is_usage_record_required": False,
        "is_validated_by_admin": True,
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_partial_update_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                 api_client_lab_worker, api_client_anon, reagent_types, producers, concentrations,
                                 units, purities_qualities, storage_conditions, hazard_statements, reagents):
    # pylint: disable=no-member
    ReagentType.history.all().delete()
    Producer.history.all().delete()
    Concentration.history.all().delete()
    Unit.history.all().delete()
    PurityQuality.history.all().delete()
    StorageCondition.history.all().delete()
    Reagent.history.all().delete()
    # pylint: enable=no-member

    # Reagent types
    reagent_type1, reagent_type2, _ = reagent_types

    client, admin = api_client_admin
    url = reverse("reagenttype-detail", args=[reagent_type1.id])

    patch_data = {
        "type": "odczynnik hiperultraspecjalny",
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_reagent_type = ReagentType.objects.get(pk=response.data["id"])

    assert db_reagent_type.type == patch_data["type"]
    assert db_reagent_type.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_reagent_type.id,
    }

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Can't update to a duplicate
    patch_data = {
        "type": "preparat dezynfekcyjny",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    client, _ = api_client_lab_manager

    patch_data = {
        "type": "odczynnik hiperhiperspecjalny",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Producers
    producer1, producer2 = producers

    client, _ = api_client_admin
    url = reverse("producer-detail", args=[producer1.id])

    patch_data = {
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_producer1 = Producer.objects.get(pk=response.data["id"])

    assert db_producer1.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_producer1.id,
        "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
        "brand_name": "POCH",
        "abbreviation": "POCH",
    }

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "is_validated_by_admin": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Concentration
    concentration1, _ = concentrations

    client, _ = api_client_admin
    url = reverse("concentration-detail", args=[concentration1.id])

    patch_data = {
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_concentration1 = Concentration.objects.get(pk=response.data["id"])

    assert db_concentration1.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_concentration1.id,
        "concentration": "99,80%",
    }

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "is_validated_by_admin": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Units
    unit1, unit2 = units

    client, _ = api_client_admin
    url = reverse("unit-detail", args=[unit1.id])

    patch_data = {
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_unit1 = Unit.objects.get(pk=response.data["id"])

    assert db_unit1.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_unit1.id,
        "unit": "preps",
    }

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "is_validated_by_admin": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Purities/Qualities
    purity_quality1, _ = purities_qualities

    client, _ = api_client_admin
    url = reverse("purityquality-detail", args=[purity_quality1.id])

    patch_data = {
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_purity_quality1 = PurityQuality.objects.get(pk=response.data["id"])

    assert db_purity_quality1.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_purity_quality1.id,
        "purity_quality": "CZDA basic",
    }

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "is_validated_by_admin": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Storage conditions
    storage_condition1, storage_condition2 = storage_conditions

    client, _ = api_client_admin
    url = reverse("storagecondition-detail", args=[storage_condition1.id])

    patch_data = {
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_storage_condition1 = PurityQuality.objects.get(pk=response.data["id"])

    assert db_storage_condition1.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_storage_condition1.id,
        "storage_condition": "RT",
    }

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "is_validated_by_admin": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Reagents
    _, reagent2 = reagents
    _, hazard_statement2 = hazard_statements

    client, _ = api_client_admin
    url = reverse("reagent-detail", args=[reagent2.id])

    patch_data = {
        "is_validated_by_admin": True,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_reagent = Reagent.objects.get(pk=response.data["id"])

    assert db_reagent.is_validated_by_admin

    history_data1 = patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_reagent.id,
        "type": {
            "id": reagent_type2.id,
            "repr": reagent_type2.type,
        },
        "producer": {
            "id": producer2.id,
            "repr": producer2.abbreviation,
        },
        "name": "DNA AWAY™ Surface Decontaminant",
        "catalog_no": "7010PK",
        "concentration": None,
        "volume": 1,
        "unit": {
            "id": unit2.id,
            "repr": unit2.unit,
        },
        "purity_quality": None,
        "storage_conditions": [
            {
                "id": storage_condition2.id,
                "repr": storage_condition2.storage_condition,
            },
        ],
        "hazard_statements": [
            {
                "id": hazard_statement2.id,
                "repr": hazard_statement2.code,
            },
        ],
        "precautionary_statements": [],
        "safety_instruction_name": "IB0002",
        "safety_data_sheet_name": "SDS0002",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": False,
        "is_validated_by_admin": True,
    }

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = ["si2"]
    safety_data_sheets = ["sds2"]
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, safety_instructions, safety_data_sheets
    ):
        safety_instruction_filename = str(history_row.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
        safety_data_sheet_filename = str(history_row.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

        assert safety_instruction_filename.startswith(safety_instruction)
        assert safety_instruction_filename.endswith(".pdf") or not safety_instruction_filename
        assert safety_data_sheet_filename.startswith(safety_data_sheet)
        assert safety_data_sheet_filename.endswith(".pdf")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    patch_data = {
        "is_validated_by_admin": False,
    }
    response = client.post(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.post(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.post(url, patch_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, patch_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # `is_usage_record_required` can't set to False when any of the hazard statements requires it to be set to True
    hazard_statement2 = reagent2.hazard_statements.all().first()
    hazard_statement2.is_usage_record_required = True
    hazard_statement2.save()

    client, _ = api_client_admin

    patch_data = {
        "is_usage_record_required": False,
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Wrong safety_instruction_name
    patch_data = {
        "safety_instruction_name": "IB2",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Wrong safety_data_sheet_name
    patch_data = {
        "safety_data_sheet_name": "SDS2",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                         api_client_anon, reagent_types, producers, concentrations, units, purities_qualities,
                         storage_conditions, reagents):
    # pylint: disable=no-member
    ReagentType.history.all().delete()
    Producer.history.all().delete()
    Concentration.history.all().delete()
    Unit.history.all().delete()
    PurityQuality.history.all().delete()
    StorageCondition.history.all().delete()
    Reagent.history.all().delete()
    # pylint: enable=no-member

    # All ForeignKey fields in Reagent are protected, so their reference cannot be deleted before they themselves are
    # deleted.

    # Reagent types
    reagent_type1, reagent_type2, _ = reagent_types

    client, _ = api_client_admin
    reagent_type_id = reagent_type1.id
    url = reverse("reagenttype-detail", args=[reagent_type_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Producers
    producer1, producer2 = producers

    client, _ = api_client_admin

    producer_id = producer1.id
    url = reverse("producer-detail", args=[producer_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Concentrations
    concentration1, concentration2 = concentrations

    client, _ = api_client_admin

    concentration_id = concentration1.id
    url = reverse("concentration-detail", args=[concentration_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Units
    unit1, unit2 = units

    client, _ = api_client_admin

    unit_id = unit1.id
    url = reverse("unit-detail", args=[unit_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Purities/Qualities
    purity_quality1, purity_quality2 = purities_qualities

    client, _ = api_client_admin

    purity_quality_id = purity_quality1.id
    url = reverse("purityquality-detail", args=[purity_quality_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Storage conditions
    storage_condition1, storage_condition2 = storage_conditions

    client, admin = api_client_admin

    storage_condition_id = storage_condition1.id
    url = reverse("storagecondition-detail", args=[storage_condition_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not StorageCondition.objects.filter(pk=storage_condition_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": storage_condition_id,
        "storage_condition": "RT",
        "is_validated_by_admin": False,
    }

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    storage_condition_id = storage_condition2.id
    url = reverse("storagecondition-detail", args=[storage_condition_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Reagents
    reagent1, reagent2 = reagents

    client, _ = api_client_admin

    reagent_id = reagent1.id
    url = reverse("reagent-detail", args=[reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Reagent.objects.filter(pk=reagent_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": reagent_id,
        "type": {
            "id": reagent_type1.id,
            "repr": reagent_type1.type,
        },
        "producer": {
            "id": producer1.id,
            "repr": producer1.abbreviation,
        },
        "name": "alkohol etylowy bezwodny",
        "catalog_no": "BA6480111",
        "concentration": {
            "id": concentration1.id,
            "repr": concentration1.concentration,
        },
        "volume": 1,
        "unit": {
            "id": unit1.id,
            "repr": unit1.unit,
        },
        "purity_quality": {
            "id": purity_quality1.id,
            "repr": purity_quality1.purity_quality,
        },
        "storage_conditions": [],
        "hazard_statements": [],
        "precautionary_statements": [],
        "safety_instruction_name": "IB0001",
        "safety_data_sheet_name": "SDS0001",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
        "is_validated_by_admin": True,
    }

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = ["si1"]
    safety_data_sheets = ["sds1"]
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, safety_instructions, safety_data_sheets
    ):
        safety_instruction_filename = str(history_row.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
        safety_data_sheet_filename = str(history_row.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

        assert safety_instruction_filename.startswith(safety_instruction)
        assert safety_instruction_filename.endswith(".pdf") or not safety_instruction_filename
        assert safety_data_sheet_filename.startswith(safety_data_sheet)
        assert safety_data_sheet_filename.endswith(".pdf")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    reagent_id = reagent2.id
    url = reverse("reagent-detail", args=[reagent_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Now we can remove the ForeignKeys

    # Reagent types
    client, _ = api_client_admin

    url = reverse("reagenttype-detail", args=[reagent_type_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ReagentType.objects.filter(pk=reagent_type_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": reagent_type_id,
        "type": "odczynnik chemiczny",
        "is_validated_by_admin": False,
    }

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    reagent_type_id = reagent_type2
    url = reverse("reagenttype-detail", args=[reagent_type_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Producers
    producer1, producer2 = producers

    client, _ = api_client_admin

    url = reverse("producer-detail", args=[producer_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Producer.objects.filter(pk=producer_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": producer_id,
        "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
        "brand_name": "POCH",
        "abbreviation": "POCH",
        "is_validated_by_admin": False,
    }

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    producer_id = producer2.id
    url = reverse("producer-detail", args=[producer_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Concentrations
    client, _ = api_client_admin

    url = reverse("concentration-detail", args=[concentration_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Concentration.objects.filter(pk=concentration_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": concentration_id,
        "concentration": "99,80%",
        "is_validated_by_admin": False,
    }

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    concentration_id = concentration2.id
    url = reverse("concentration-detail", args=[concentration_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Units
    client, _ = api_client_admin

    url = reverse("unit-detail", args=[unit_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Unit.objects.filter(pk=unit_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": unit_id,
        "unit": "preps",
        "is_validated_by_admin": False,
    }

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    unit_id = unit2.id
    url = reverse("unit-detail", args=[unit_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Purities/Qualities
    client, _ = api_client_admin

    url = reverse("purityquality-detail", args=[purity_quality_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not PurityQuality.objects.filter(pk=purity_quality_id).exists()

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": purity_quality_id,
        "purity_quality": "CZDA basic",
        "is_validated_by_admin": False,
    }

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    purity_quality_id = purity_quality2.id
    url = reverse("purityquality-detail", args=[purity_quality_id])

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_safety_instructions(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                 api_client_lab_worker, api_client_anon, reagents):

    reagent1, reagent2 = reagents

    client, _ = api_client_admin
    url = reverse("reagent-get-safety-instructions")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent1.id,
            "reagent_name": reagent1.name,
            "producer": reagent1.producer.abbreviation,
        },
        {
            "id": reagent2.id,
            "reagent_name": reagent2.name,
            "producer": reagent2.producer.abbreviation,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    url = f"{reverse('reagent-get-safety-instructions')}?search={reagent1.name}"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent1.id,
            "reagent_name": reagent1.name,
            "producer": reagent1.producer.abbreviation,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual


@pytest.mark.django_db
def test_get_safety_instruction(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                api_client_lab_worker, api_client_anon, reagents):

    reagent1, _ = reagents

    client, _ = api_client_admin
    url = reverse("reagent-get-safety-instruction", args=[reagent1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Dropping safety_instruction because it gets a random suffix
    expected = {
        "id": reagent1.id,
    }

    response_data = response.data
    safety_instruction_name = response_data.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    safety_instruction_name = response_data.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    safety_instruction_name = response_data.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    safety_instruction_name = response_data.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    safety_instruction_name = response_data.pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    assert safety_instruction_name.startswith("si1")
    assert safety_instruction_name.endswith(".pdf")

    actual = json.loads(json.dumps(response_data))

    assert expected == actual
