"""This file tests Producer, ReagentType, Concentration, Unit, PurityQuality, StorageCondition and Reagent."""

import json

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status

from reagents.models import Producer, ReagentType, Concentration, Unit, PurityQuality, StorageCondition, Reagent
from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, model_to_dict


@pytest.mark.django_db
def test_list_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                       api_client_anon, reagent_types, producers, concentrations, units, purities_qualities,
                       storage_conditions, hazard_statements, precautionary_statements, reagents):
    # Reagent types
    reagent_type1, reagent_type2, reagent_type3 = reagent_types

    client, _ = api_client_admin
    url = reverse("reagenttype-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type1.id,
            "type": "odczynnik chemiczny",
            "is_validated_by_admin": False,
        },
        {
            "id": reagent_type2.id,
            "type": "zestaw odczynników",
            "is_validated_by_admin": True,
        },
        {
            "id": reagent_type3.id,
            "type": "preparat dezynfekcyjny",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('reagenttype-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type1.id,
            "type": "odczynnik chemiczny",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('reagenttype-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type2.id,
            "type": "zestaw odczynników",
            "is_validated_by_admin": True,
        },
        {
            "id": reagent_type3.id,
            "type": "preparat dezynfekcyjny",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('reagenttype-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type1.id,
            "type": "odczynnik chemiczny",
            "is_validated_by_admin": False,
        },
        {
            "id": reagent_type2.id,
            "type": "zestaw odczynników",
            "is_validated_by_admin": True,
        },
        {
            "id": reagent_type3.id,
            "type": "preparat dezynfekcyjny",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('reagenttype-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `type`
    url = f"{reverse('reagenttype-list')}?ordering=type"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type1.id,
            "type": "odczynnik chemiczny",
            "is_validated_by_admin": False,
        },
        {
            "id": reagent_type3.id,
            "type": "preparat dezynfekcyjny",
            "is_validated_by_admin": True,
        },
        {
            "id": reagent_type2.id,
            "type": "zestaw odczynników",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('reagenttype-list')}?ordering=-type"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `type`
    url = f"{reverse('reagenttype-list')}?search=zestaw"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type2.id,
            "type": "zestaw odczynników",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("reagenttype-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent_type1.id,
            "type": "odczynnik chemiczny",
            "is_validated_by_admin": False,
        },
        {
            "id": reagent_type2.id,
            "type": "zestaw odczynników",
            "is_validated_by_admin": True,
        },
        {
            "id": reagent_type3.id,
            "type": "preparat dezynfekcyjny",
            "is_validated_by_admin": True,
        },
    ]
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

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Producers
    producer1, producer2 = producers

    client, _ = api_client_admin
    url = reverse("producer-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('producer-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('producer-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('producer-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('producer-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `producer_name`
    url = f"{reverse('producer-list')}?ordering=producer_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('producer-list')}?ordering=-producer_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `brand_name`
    url = f"{reverse('producer-list')}?ordering=brand_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('producer-list')}?ordering=-brand_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `abbreviation`
    url = f"{reverse('producer-list')}?ordering=abbreviation"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('producer-list')}?ordering=-abbreviation"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `producer_name`
    url = f"{reverse('producer-list')}?search=av"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `brand_name`
    producer1.brand_name = "TEST"
    producer1.save()
    url = f"{reverse('producer-list')}?search=test"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "TEST",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `abbreviation`
    url = f"{reverse('producer-list')}?search=poch"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "TEST",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    producer1.brand_name = "POCH"
    producer1.save()

    client, _ = api_client_lab_manager

    url = reverse("producer-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": producer1.id,
            "producer_name": "AVANTOR PERFORMANCE MATERIALS POLAND S.A.",
            "brand_name": "POCH",
            "abbreviation": "POCH",
            "is_validated_by_admin": False,
        },
        {
            "id": producer2.id,
            "producer_name": "THERMO FISHER SCIENTIFIC",
            "brand_name": "THERMO FISHER SCIENTIFIC",
            "abbreviation": "THERMO",
            "is_validated_by_admin": True,
        },
    ]
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

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Concentrations
    concentration1, concentration2 = concentrations

    client, _ = api_client_admin
    url = reverse("concentration-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration1.id,
            "concentration": "99,80%",
            "is_validated_by_admin": False,
        },
        {
            "id": concentration2.id,
            "concentration": "0,1 M",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('concentration-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration1.id,
            "concentration": "99,80%",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('concentration-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration2.id,
            "concentration": "0,1 M",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('concentration-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration1.id,
            "concentration": "99,80%",
            "is_validated_by_admin": False,
        },
        {
            "id": concentration2.id,
            "concentration": "0,1 M",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('concentration-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `concentration`
    url = f"{reverse('concentration-list')}?ordering=concentration"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration2.id,
            "concentration": "0,1 M",
            "is_validated_by_admin": True,
        },
        {
            "id": concentration1.id,
            "concentration": "99,80%",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('concentration-list')}?ordering=-concentration"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `concentration`
    url = f"{reverse('concentration-list')}?search=M"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration2.id,
            "concentration": "0,1 M",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("concentration-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": concentration1.id,
            "concentration": "99,80%",
            "is_validated_by_admin": False,
        },
        {
            "id": concentration2.id,
            "concentration": "0,1 M",
            "is_validated_by_admin": True,
        },
    ]
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

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Units
    unit1, unit2 = units

    client, _ = api_client_admin
    url = reverse("unit-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit1.id,
            "unit": "preps",
            "is_validated_by_admin": False,
        },
        {
            "id": unit2.id,
            "unit": "mL",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('unit-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit1.id,
            "unit": "preps",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('unit-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit2.id,
            "unit": "mL",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('unit-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit1.id,
            "unit": "preps",
            "is_validated_by_admin": False,
        },
        {
            "id": unit2.id,
            "unit": "mL",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('unit-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `unit`
    url = f"{reverse('unit-list')}?ordering=unit"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit2.id,
            "unit": "mL",
            "is_validated_by_admin": True,
        },
        {
            "id": unit1.id,
            "unit": "preps",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('unit-list')}?ordering=-unit"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `unit`
    url = f"{reverse('unit-list')}?search=ml"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit2.id,
            "unit": "mL",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("unit-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": unit1.id,
            "unit": "preps",
            "is_validated_by_admin": False,
        },
        {
            "id": unit2.id,
            "unit": "mL",
            "is_validated_by_admin": True,
        },
    ]
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

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Purities/Qualities
    purity_quality1, purity_quality2 = purities_qualities

    client, _ = api_client_admin
    url = reverse("purityquality-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality1.id,
            "purity_quality": "CZDA basic",
            "is_validated_by_admin": False,
        },
        {
            "id": purity_quality2.id,
            "purity_quality": "molecular biology grade",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('purityquality-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality1.id,
            "purity_quality": "CZDA basic",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('purityquality-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality2.id,
            "purity_quality": "molecular biology grade",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('purityquality-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality1.id,
            "purity_quality": "CZDA basic",
            "is_validated_by_admin": False,
        },
        {
            "id": purity_quality2.id,
            "purity_quality": "molecular biology grade",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('purityquality-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `purity_quality`
    url = f"{reverse('purityquality-list')}?ordering=purity_quality"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality1.id,
            "purity_quality": "CZDA basic",
            "is_validated_by_admin": False,
        },
        {
            "id": purity_quality2.id,
            "purity_quality": "molecular biology grade",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('purityquality-list')}?ordering=-purity_quality"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `purity_quality`
    url = f"{reverse('purityquality-list')}?search=grade"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality2.id,
            "purity_quality": "molecular biology grade",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("purityquality-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": purity_quality1.id,
            "purity_quality": "CZDA basic",
            "is_validated_by_admin": False,
        },
        {
            "id": purity_quality2.id,
            "purity_quality": "molecular biology grade",
            "is_validated_by_admin": True,
        },
    ]
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

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Storage conditions
    storage_condition1, storage_condition2 = storage_conditions

    client, _ = api_client_admin
    url = reverse("storagecondition-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition1.id,
            "storage_condition": "RT",
            "is_validated_by_admin": False,
        },
        {
            "id": storage_condition2.id,
            "storage_condition": "chronić przed światłem",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('storagecondition-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition1.id,
            "storage_condition": "RT",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('storagecondition-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition2.id,
            "storage_condition": "chronić przed światłem",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('storagecondition-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition1.id,
            "storage_condition": "RT",
            "is_validated_by_admin": False,
        },
        {
            "id": storage_condition2.id,
            "storage_condition": "chronić przed światłem",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('storagecondition-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `storage_condition`
    url = f"{reverse('storagecondition-list')}?ordering=storage_condition"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition2.id,
            "storage_condition": "chronić przed światłem",
            "is_validated_by_admin": True,
        },
        {
            "id": storage_condition1.id,
            "storage_condition": "RT",
            "is_validated_by_admin": False,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('storagecondition-list')}?ordering=-storage_condition"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `storage_condition`
    url = f"{reverse('storagecondition-list')}?search=chronić"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition2.id,
            "storage_condition": "chronić przed światłem",
            "is_validated_by_admin": True,
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    client, _ = api_client_lab_manager
    url = reverse("storagecondition-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": storage_condition1.id,
            "storage_condition": "RT",
            "is_validated_by_admin": False,
        },
        {
            "id": storage_condition2.id,
            "storage_condition": "chronić przed światłem",
            "is_validated_by_admin": True,
        },
    ]
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

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Reagents
    reagent1, reagent2 = reagents
    hazard_statement1, hazard_statement2 = hazard_statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    client, _ = api_client_admin
    url = reverse("reagent-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    # Dropping filenames because they get random suffixes
    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Filtering
    # `is_validated_by_admin`
    url = f"{reverse('reagent-list')}?is_validated_by_admin=False"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?is_validated_by_admin=True"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('reagent-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?ordering=-id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `name`
    url = f"{reverse('reagent-list')}?ordering=name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?ordering=-name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `producer__abbreviation`
    url = f"{reverse('reagent-list')}?ordering=producer"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?ordering=-producer"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `catalog_no`
    url = f"{reverse('reagent-list')}?ordering=catalog_no"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
        {
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
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?ordering=-catalog_no"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `safety_instruction_name`
    url = f"{reverse('reagent-list')}?ordering=safety_instruction_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?ordering=-safety_instruction_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `safety_data_sheet_name`
    url = f"{reverse('reagent-list')}?ordering=safety_data_sheet_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('reagent-list')}?ordering=-safety_data_sheet_name"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[1].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[1].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Searching
    # `name`
    url = f"{reverse('reagent-list')}?search=bezwodny"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `producer__abbreviation`
    url = f"{reverse('reagent-list')}?search=therm"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `catalog_no`
    url = f"{reverse('reagent-list')}?search=701"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": reagent2.id,
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
            "is_validated_by_admin": False,
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si2")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds2")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `safety_instruction_name`
    url = f"{reverse('reagent-list')}?search=IB0001"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
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
        },
    ]

    response_data_results = response.data["results"]

    safety_instruction_filename = response_data_results[0].pop("safety_instruction").rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = response_data_results[0].pop("safety_data_sheet").rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si1")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds1")
    assert safety_data_sheet_filename.endswith(".pdf")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client = api_client_anon
    url = reverse("reagent-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_reagents(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                         api_client_anon, hazard_statements, precautionary_statements, mock_files):
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
    client, admin = api_client_admin
    url = reverse("reagenttype-list")

    # Admins always POST with `is_validated_by_admin` set to True
    post_data = {
        "type": "odczynnik specjalny",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    reagent_type_id = response.data["id"]
    db_reagent_type = ReagentType.objects.get(pk=reagent_type_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_reagent_type.id,
    }

    post_data["id"] = reagent_type_id
    assert post_data == model_to_dict(db_reagent_type)

    client, lab_manager = api_client_lab_manager

    post_data = {
        "type": "odczynnik ultraultraspecjalny",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    reagent_type_id = response.data["id"]
    db_reagent_type = ReagentType.objects.get(pk=reagent_type_id)
    post_data["is_validated_by_admin"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_reagent_type.id,
    }

    post_data["id"] = reagent_type_id
    assert post_data == model_to_dict(db_reagent_type)

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('reagenttype-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('reagenttype-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `type`
    response = client.get(f"{reverse('reagenttype-get-historical-records')}?ordering=type")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('reagenttype-get-historical-records')}?ordering=-type")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `type`
    response = client.get(f"{reverse('reagenttype-get-historical-records')}?search=ultra")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "type": "odczynnik hiperultraekstraspecjalny",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    reagent_type_id = response.data["id"]
    db_reagent_type = ReagentType.objects.get(pk=reagent_type_id)
    post_data["id"] = reagent_type_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_reagent_type)

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "type": "odczynnik ekstraspecjalny",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    reagent_type_id = response.data["id"]
    db_reagent_type = ReagentType.objects.get(pk=reagent_type_id)
    post_data["id"] = reagent_type_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_reagent_type)

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "type": "odczynnik hiperekstraspecjalny",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("reagenttype-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Producers
    client, _ = api_client_admin
    url = reverse("producer-list")

    post_data = {
        "producer_name": "TEST0",
        "brand_name": "TEST1",
        "abbreviation": "TEST2",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    producer_id = response.data["id"]
    db_producer1 = Producer.objects.get(pk=producer_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_producer1.id,
    }

    post_data["id"] = producer_id
    assert post_data == model_to_dict(db_producer1)

    # The rest POST with `is_validated_by_admin` set to False
    client, _ = api_client_lab_manager

    post_data = {
        "producer_name": "BECTON DICKINSON CANADA INC",
        "brand_name": "BECTON DICKINSON CANADA INC",
        "abbreviation": "BECTON",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    producer_id = response.data["id"]
    db_producer2 = Producer.objects.get(pk=producer_id)
    post_data["is_validated_by_admin"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_producer2.id,
    }

    post_data["id"] = producer_id
    assert post_data == model_to_dict(db_producer2)

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `producer_name`
    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=producer_name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=-producer_name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `brand_name`
    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=brand_name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=-brand_name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `abbreviation`
    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=abbreviation")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('producer-get-historical-records')}?ordering=-abbreviation")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `producer_name`
    response = client.get(f"{reverse('producer-get-historical-records')}?search=TeST0")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `brand_name`
    response = client.get(f"{reverse('producer-get-historical-records')}?search=test1")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `abbreviation`
    response = client.get(f"{reverse('producer-get-historical-records')}?search=test2")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "producer_name": "BIO-RAD LABORATORIES INC",
        "brand_name": "BIO-RAD LABORATORIES INC",
        "abbreviation": "BIO-RAD",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    producer_id = response.data["id"]
    db_producer3 = Producer.objects.get(pk=producer_id)
    post_data["id"] = producer_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_producer3)

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "producer_name": "BIOSHOP",
        "brand_name": "BIOSHOP",
        "abbreviation": "BIOSHOP",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    producer_id = response.data["id"]
    db_producer4 = Producer.objects.get(pk=producer_id)
    post_data["id"] = producer_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_producer4)

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "producer_name": "BLIRT SA",
        "brand_name": "BLIRT",
        "abbreviation": "BLIRT",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("producer-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Concentration
    client, _ = api_client_admin
    url = reverse("concentration-list")

    post_data = {
        "concentration": "0,25%",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    concentration_id = response.data["id"]
    db_concentration1 = Concentration.objects.get(pk=concentration_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_concentration1.id,
    }

    post_data["id"] = concentration_id
    assert post_data == model_to_dict(db_concentration1)

    client, _ = api_client_lab_manager

    post_data = {
        "concentration": "5%",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    concentration_id = response.data["id"]
    db_concentration2 = Concentration.objects.get(pk=concentration_id)
    post_data["is_validated_by_admin"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_concentration2.id,
    }

    post_data["id"] = concentration_id
    assert post_data == model_to_dict(db_concentration2)

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('concentration-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('concentration-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `concentration`
    response = client.get(f"{reverse('concentration-get-historical-records')}?ordering=concentration")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('concentration-get-historical-records')}?ordering=-concentration")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `concentration`
    response = client.get(f"{reverse('concentration-get-historical-records')}?search=0,")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "concentration": "10%",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    concentration_id = response.data["id"]
    db_concentration3 = Concentration.objects.get(pk=concentration_id)
    post_data["id"] = concentration_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_concentration3)

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "concentration": "16%",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    concentration_id = response.data["id"]
    db_concentration4 = Concentration.objects.get(pk=concentration_id)
    post_data["id"] = concentration_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_concentration4)

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "concentration": "30%",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("concentration-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Units
    client, _ = api_client_admin
    url = reverse("unit-list")

    post_data = {
        "unit": "L",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    unit_id = response.data["id"]
    db_unit1 = Unit.objects.get(pk=unit_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_unit1.id,
    }

    post_data["id"] = unit_id
    assert post_data == model_to_dict(db_unit1)

    client, _ = api_client_lab_manager

    post_data = {
        "unit": "mg",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    unit_id = response.data["id"]
    db_unit2 = Unit.objects.get(pk=unit_id)
    post_data["is_validated_by_admin"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_unit2.id,
    }

    post_data["id"] = unit_id
    assert post_data == model_to_dict(db_unit2)

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('unit-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('unit-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `unit`
    response = client.get(f"{reverse('unit-get-historical-records')}?ordering=unit")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('unit-get-historical-records')}?ordering=-unit")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `unit`
    response = client.get(f"{reverse('unit-get-historical-records')}?search=m")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "unit": "g",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    unit_id = response.data["id"]
    db_unit3 = Unit.objects.get(pk=unit_id)
    post_data["id"] = unit_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_unit3)

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "unit": "kg",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    unit_id = response.data["id"]
    db_unit4 = Unit.objects.get(pk=unit_id)
    post_data["id"] = unit_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_unit4)

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "unit": "rxn",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("unit-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Purities/Qualities
    client, _ = api_client_admin
    url = reverse("purityquality-list")

    post_data = {
        "purity_quality": "CZDA ODCZ. FP",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    purity_quality_id = response.data["id"]
    db_purity_quality1 = PurityQuality.objects.get(pk=purity_quality_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_purity_quality1.id,
    }

    post_data["id"] = purity_quality_id
    assert post_data == model_to_dict(db_purity_quality1)

    client, _ = api_client_lab_manager

    post_data = {
        "purity_quality": "ODCZ. FP",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    purity_quality_id = response.data["id"]
    db_purity_quality2 = PurityQuality.objects.get(pk=purity_quality_id)
    post_data["is_validated_by_admin"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_purity_quality2.id,
    }

    post_data["id"] = purity_quality_id
    assert post_data == model_to_dict(db_purity_quality2)

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('purityquality-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('purityquality-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `purity_quality`
    response = client.get(f"{reverse('purityquality-get-historical-records')}?ordering=purity_quality")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('purityquality-get-historical-records')}?ordering=-purity_quality")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `purity_quality`
    response = client.get(f"{reverse('purityquality-get-historical-records')}?search=czda")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "purity_quality": "Ultra Pure",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    purity_quality_id = response.data["id"]
    db_purity_quality3 = PurityQuality.objects.get(pk=purity_quality_id)
    post_data["id"] = purity_quality_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_purity_quality3)

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "purity_quality": "CZDA basic",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    purity_quality_id = response.data["id"]
    db_purity_quality4 = PurityQuality.objects.get(pk=purity_quality_id)
    post_data["id"] = purity_quality_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_purity_quality4)

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "purity_quality": "CZDA pure p.a.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("purityquality-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Storage conditions
    client, _ = api_client_admin
    url = reverse("storagecondition-list")

    post_data = {
        "storage_condition": "2 do 8°C",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    storage_condition_id = response.data["id"]
    db_storage_condition1 = StorageCondition.objects.get(pk=storage_condition_id)
    post_data["is_validated_by_admin"] = True

    history_data1 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_storage_condition1.id,
    }

    post_data["id"] = storage_condition_id
    assert post_data == model_to_dict(db_storage_condition1)

    client, _ = api_client_lab_manager

    post_data = {
        "storage_condition": "-15 do -25°C",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    storage_condition_id = response.data["id"]
    db_storage_condition2 = StorageCondition.objects.get(pk=storage_condition_id)
    post_data["is_validated_by_admin"] = False

    history_data2 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_storage_condition2.id,
    }

    post_data["id"] = storage_condition_id
    assert post_data == model_to_dict(db_storage_condition2)

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('storagecondition-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('storagecondition-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `storage_condition`
    response = client.get(f"{reverse('storagecondition-get-historical-records')}?ordering=storage_condition")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('storagecondition-get-historical-records')}?ordering=-storage_condition")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `storage_condition`
    response = client.get(f"{reverse('storagecondition-get-historical-records')}?search=-")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_project_manager

    post_data = {
        "storage_condition": "-15 do -30°C",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    storage_condition_id = response.data["id"]
    db_storage_condition3 = StorageCondition.objects.get(pk=storage_condition_id)
    post_data["id"] = storage_condition_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_storage_condition3)

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "storage_condition": "RT - szafa wentylowana",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    storage_condition_id = response.data["id"]
    db_storage_condition4 = StorageCondition.objects.get(pk=storage_condition_id)
    post_data["id"] = storage_condition_id
    post_data["is_validated_by_admin"] = False

    assert post_data == model_to_dict(db_storage_condition4)

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "storage_condition": "4 do 8°C",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("storagecondition-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Reagents
    hazard_statement1, hazard_statement2 = hazard_statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    client, _ = api_client_admin
    url = reverse("reagent-list")

    safety_instructions = ["", "", "", "si4", "si4", "si4"]
    safety_data_sheets = ["sds3", "sds3", "sds3", "sds4", "sds4", "sds4"]

    # Minimal dataset consisting of only required fields
    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer1.id,
        "name": r"Pierce™ 16% Formaldehyde (w/v), Methanol-free",
        "catalog_no": "28908",
        "volume": 100,
        "unit": db_unit1.id,
        "storage_conditions": [db_storage_condition1.id, db_storage_condition2.id],
        "safety_data_sheet": SimpleUploadedFile(f"{safety_data_sheets[0]}.pdf", pdf_bytes),
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    reagent_id = response.data["id"]
    db_reagent = Reagent.objects.get(pk=reagent_id)

    post_data["concentration"] = None
    post_data["purity_quality"] = None
    post_data["hazard_statements"] = []
    post_data["precautionary_statements"] = []
    post_data["safety_instruction_name"] = ""
    post_data["safety_data_sheet_name"] = ""
    post_data["cas_no"] = ""
    post_data["other_info"] = ""
    post_data["kit_contents"] = ""
    post_data["is_validated_by_admin"] = True
    post_data.pop("safety_data_sheet")

    history_data2 = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_reagent.id,
    }
    history_data2["type"] = {
        "id": db_reagent_type.id,
        "repr": db_reagent_type.type,
    }
    history_data2["producer"] = {
        "id": db_producer1.id,
        "repr": db_producer1.abbreviation,
    }
    history_data2["concentration"] = None
    history_data2["unit"] = {
        "id": db_unit1.id,
        "repr": db_unit1.unit,
    }
    history_data2["purity_quality"] = None
    history_data2["storage_conditions"] = [
        {
            "id": db_storage_condition1.id,
            "repr": db_storage_condition1.storage_condition,
        },
        {
            "id": db_storage_condition2.id,
            "repr": db_storage_condition2.storage_condition,
        },
    ]
    history_data2["hazard_statements"] = []
    history_data2["precautionary_statements"] = []
    history_data1 = history_data2.copy()
    history_data1["history_type"] = "+"
    history_data1["storage_conditions"] = []

    post_data["id"] = reagent_id
    db_reagent_dict = model_to_dict(db_reagent)

    safety_data_sheet_filename = str(db_reagent_dict.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

    assert safety_data_sheet_filename.startswith(safety_data_sheets[0])
    assert safety_data_sheet_filename.endswith(".pdf")

    assert not db_reagent_dict.pop("safety_instruction")

    assert post_data == db_reagent_dict

    client, _ = api_client_lab_manager

    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer2.id,
        "name": "1-Bromo-3-chloropropane",
        "catalog_no": "106862500",
        "concentration": db_concentration2.id,
        "volume": 250,
        "unit": db_unit2.id,
        "purity_quality": db_purity_quality2.id,
        "storage_conditions": [db_storage_condition1.id],
        "hazard_statements": [hazard_statement2.id],
        "precautionary_statements": [],
        "safety_instruction": SimpleUploadedFile(f"{safety_instructions[3]}.pdf", pdf_bytes),
        "safety_instruction_name": "IB0004",
        "safety_data_sheet": SimpleUploadedFile(f"{safety_data_sheets[3]}.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0004",
        "cas_no": "109-70-6",
        "other_info": "ciecz",
        "kit_contents": "",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    reagent_id = response.data["id"]
    db_reagent = Reagent.objects.get(pk=reagent_id)

    post_data["is_validated_by_admin"] = False
    post_data.pop("safety_instruction")
    post_data.pop("safety_data_sheet")

    history_data5 = post_data | {
        "history_user": lab_manager.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_reagent.id,
    }
    history_data5["type"] = {
        "id": db_reagent_type.id,
        "repr": db_reagent_type.type,
    }
    history_data5["producer"] = {
        "id": db_producer2.id,
        "repr": db_producer2.abbreviation,
    }
    history_data5["concentration"] = {
        "id": db_concentration2.id,
        "repr": db_concentration2.concentration,
    }
    history_data5["unit"] = {
        "id": db_unit2.id,
        "repr": db_unit2.unit,
    }
    history_data5["purity_quality"] = {
        "id": db_purity_quality2.id,
        "repr": db_purity_quality2.purity_quality,
    }
    history_data5["storage_conditions"] = [
        {
            "id": db_storage_condition1.id,
            "repr": db_storage_condition1.storage_condition,
        },
    ]
    history_data5["hazard_statements"] = [
        {
            "id": hazard_statement2.id,
            "repr": hazard_statement2.code,
        },
    ]
    history_data5["precautionary_statements"] = []
    history_data4 = history_data5.copy()
    history_data4["hazard_statements"] = []
    history_data3 = history_data4.copy()
    history_data3["history_type"] = "+"
    history_data3["storage_conditions"] = []

    post_data["id"] = reagent_id
    db_reagent_dict = model_to_dict(db_reagent)

    safety_instruction_filename = str(db_reagent_dict.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = str(db_reagent_dict.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith(safety_instructions[3])
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith(safety_data_sheets[3])
    assert safety_data_sheet_filename.endswith(".pdf")

    assert post_data == db_reagent_dict

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    client, _ = api_client_admin

    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data5, history_data4, history_data3, history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    # History associated with M2M fields is going to make it more difficult to check filters,
    # so we're going to remove it.
    reagent_history = Reagent.history.all()  # pylint: disable=no-member
    reagent_history[0].delete()
    reagent_history[0].delete()
    reagent_history[1].delete()
    safety_instructions = ["", "si4"]
    safety_data_sheets = ["sds3", "sds4"]

    # Ordering
    # `id`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
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

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    # `name`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=-name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
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

    # `producer__abbreviation`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=producer")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=-producer")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
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

    # `catalog_no`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=catalog_no")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=-catalog_no")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
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

    # `safety_instruction_name`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=safety_instruction_name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
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

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=-safety_instruction_name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    # `safety_data_sheet_name`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=safety_data_sheet_name")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
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

    response = client.get(f"{reverse('reagent-get-historical-records')}?ordering=-safety_data_sheet_name")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, safety_instruction, safety_data_sheet in zip(
        actual, reversed(safety_instructions), reversed(safety_data_sheets)
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

    # Searching
    # `name`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?search=pierce")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = [""]
    safety_data_sheets = ["sds3"]
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

    # `producer__abbreviation`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?search=becton")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = ["si4"]
    safety_data_sheets = ["sds4"]
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

    # `catalog_no`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?search=6862")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = ["si4"]
    safety_data_sheets = ["sds4"]
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

    # `safety_instruction_name`
    client, _ = api_client_admin

    response = client.get(f"{reverse('reagent-get-historical-records')}?search=IB0004")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data3]
    actual = json.loads(json.dumps(response.data["results"]))
    safety_instructions = ["si4"]
    safety_data_sheets = ["sds4"]
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

    client, _ = api_client_project_manager

    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer3.id,
        "name": "BigDye XTerminator™ Purification Kit",
        "catalog_no": "4376486",
        "concentration": db_concentration3.id,
        "volume": 100,
        "unit": db_unit3.id,
        "purity_quality": db_purity_quality3.id,
        "storage_conditions": [db_storage_condition3.id],
        "hazard_statements": [hazard_statement1.id, hazard_statement2.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si5.pdf", pdf_bytes),
        "safety_instruction_name": "IB0005",
        "safety_data_sheet": SimpleUploadedFile("sds5.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0005",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    reagent_id = response.data["id"]
    db_reagent = Reagent.objects.get(pk=reagent_id)

    post_data["id"] = reagent_id
    post_data["is_validated_by_admin"] = False
    post_data.pop("safety_instruction")
    post_data.pop("safety_data_sheet")

    db_reagent_dict = model_to_dict(db_reagent)

    safety_instruction_filename = str(db_reagent_dict.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = str(db_reagent_dict.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si5")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds5")
    assert safety_data_sheet_filename.endswith(".pdf")

    assert post_data == db_reagent_dict

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer4.id,
        "name": "RNaseZap Wipes",
        "catalog_no": "AM9786",
        "concentration": db_concentration4.id,
        "volume": 1,
        "unit": db_unit4.id,
        "purity_quality": db_purity_quality4.id,
        "storage_conditions": [db_storage_condition1.id, db_storage_condition4.id],
        "hazard_statements": [],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si6.pdf", pdf_bytes),
        "safety_instruction_name": "IB0006",
        "safety_data_sheet": SimpleUploadedFile("sds6.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0006",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    reagent_id = response.data["id"]
    db_reagent = Reagent.objects.get(pk=reagent_id)

    post_data["id"] = reagent_id
    post_data["is_validated_by_admin"] = False
    post_data.pop("safety_instruction")
    post_data.pop("safety_data_sheet")

    db_reagent_dict = model_to_dict(db_reagent)

    safety_instruction_filename = str(db_reagent_dict.pop("safety_instruction")).rsplit("/", maxsplit=1)[-1]
    safety_data_sheet_filename = str(db_reagent_dict.pop("safety_data_sheet")).rsplit("/", maxsplit=1)[-1]

    assert safety_instruction_filename.startswith("si6")
    assert safety_instruction_filename.endswith(".pdf")
    assert safety_data_sheet_filename.startswith("sds6")
    assert safety_data_sheet_filename.endswith(".pdf")

    assert post_data == db_reagent_dict

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer4.id,
        "name": "Rotiphorese 10x TBE Buffer",
        "catalog_no": "3061.2",
        "concentration": db_concentration4.id,
        "volume": 1,
        "unit": db_unit4.id,
        "purity_quality": db_purity_quality4.id,
        "storage_conditions": [db_storage_condition1.id, db_storage_condition4.id],
        "hazard_statements": [],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si7.pdf", pdf_bytes),
        "safety_instruction_name": "IB0007",
        "safety_data_sheet": SimpleUploadedFile("sds7.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0007",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("reagent-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # `is_usage_record_required` can't set to False when any of the hazard statements requires it to be set to True
    hazard_statement1.is_usage_record_required = True
    hazard_statement1.save()

    client, _ = api_client_lab_worker
    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer4.id,
        "name": "Rotiphorese 10x TBE Buffer",
        "catalog_no": "3061.2",
        "concentration": db_concentration4.id,
        "volume": 1,
        "unit": db_unit4.id,
        "purity_quality": db_purity_quality4.id,
        "storage_conditions": [db_storage_condition1.id, db_storage_condition4.id],
        "hazard_statements": [hazard_statement1.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si7.pdf", pdf_bytes),
        "safety_instruction_name": "IB0007",
        "safety_data_sheet": SimpleUploadedFile("sds7.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0007",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": False,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Wrong safety_instruction_name
    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer4.id,
        "name": "Rotiphorese 10x TBE Buffer",
        "catalog_no": "3061.2",
        "concentration": db_concentration4.id,
        "volume": 1,
        "unit": db_unit4.id,
        "purity_quality": db_purity_quality4.id,
        "storage_conditions": [db_storage_condition1.id, db_storage_condition4.id],
        "hazard_statements": [hazard_statement1.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si7.pdf", pdf_bytes),
        "safety_instruction_name": "IB7",
        "safety_data_sheet": SimpleUploadedFile("sds7.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS0007",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Wrong safety_data_sheet_name
    post_data = {
        "type": db_reagent_type.id,
        "producer": db_producer4.id,
        "name": "Rotiphorese 10x TBE Buffer",
        "catalog_no": "3061.2",
        "concentration": db_concentration4.id,
        "volume": 1,
        "unit": db_unit4.id,
        "purity_quality": db_purity_quality4.id,
        "storage_conditions": [db_storage_condition1.id, db_storage_condition4.id],
        "hazard_statements": [hazard_statement1.id],
        "precautionary_statements": [precautionary_statement1.id, precautionary_statement2.id],
        "safety_instruction": SimpleUploadedFile("si7.pdf", pdf_bytes),
        "safety_instruction_name": "IB0007",
        "safety_data_sheet": SimpleUploadedFile("sds7.pdf", pdf_bytes),
        "safety_data_sheet_name": "SDS007",
        "cas_no": "",
        "other_info": "",
        "kit_contents": "",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
