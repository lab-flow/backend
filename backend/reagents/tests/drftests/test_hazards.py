"""This file tests Pictogram, ClpClassification, HazardStatement and PrecautionaryStatement."""

import json

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status

from reagents.models import Pictogram, ClpClassification, HazardStatement, PrecautionaryStatement
from reagents.tests.drftests.conftest import assert_timezone_now_gte_datetime, model_to_dict


@pytest.mark.django_db
def test_list_hazards(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                      api_client_anon, clp_classifications, pictograms, hazard_statements, precautionary_statements):
    # CLP classifications
    clp_classification1, clp_classification2 = clp_classifications

    client, _ = api_client_admin
    url = reverse("clpclassification-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification1.id,
            "classification": "Substancje łatwopalne",
            "clp_classification": "GHS02",
            "hazard_group": "PHY",
        },
        {
            "id": clp_classification2.id,
            "classification": "Substancje drażniące",
            "clp_classification": "GHS07",
            "hazard_group": "HEA",
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

    # Ordering
    # `id`
    url = f"{reverse('clpclassification-list')}?ordering=id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification1.id,
            "classification": "Substancje łatwopalne",
            "clp_classification": "GHS02",
            "hazard_group": "PHY",
        },
        {
            "id": clp_classification2.id,
            "classification": "Substancje drażniące",
            "clp_classification": "GHS07",
            "hazard_group": "HEA",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('clpclassification-list')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `clp_classification`
    url = f"{reverse('clpclassification-list')}?ordering=clp_classification"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification1.id,
            "classification": "Substancje łatwopalne",
            "clp_classification": "GHS02",
            "hazard_group": "PHY",
        },
        {
            "id": clp_classification2.id,
            "classification": "Substancje drażniące",
            "clp_classification": "GHS07",
            "hazard_group": "HEA",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('clpclassification-list')}?ordering=-clp_classification"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `clp_classification`
    url = f"{reverse('clpclassification-list')}?search=2"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification1.id,
            "classification": "Substancje łatwopalne",
            "clp_classification": "GHS02",
            "hazard_group": "PHY",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Pictograms
    pictogram1, pictogram2 = pictograms

    client, _ = api_client_admin
    url = reverse("pictogram-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Dropping filenames because they get random suffixes
    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected = [
        {
            "id": pictogram1.id,
        },
        {
            "id": pictogram2.id,
        },
    ]
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('pictogram-list')}?ordering=id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected = [
        {
            "id": pictogram1.id,
        },
        {
            "id": pictogram2.id,
        },
    ]
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('pictogram-list')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS07")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS02")
    assert pictogram2_filename.endswith(".png")

    expected.reverse()
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `pictogram` (filename)
    url = f"{reverse('pictogram-list')}?ordering=pictogram"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected = [
        {
            "id": pictogram1.id,
        },
        {
            "id": pictogram2.id,
        },
    ]
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('pictogram-list')}?ordering=-pictogram"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]

    pictogram1_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    pictogram2_filename = response_data_results[1].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS07")
    assert pictogram1_filename.endswith(".png")
    assert pictogram2_filename.startswith("GHS02")
    assert pictogram2_filename.endswith(".png")

    expected.reverse()
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Searching
    # `pictogram` (filename)
    url = f"{reverse('pictogram-list')}?search=GHS07"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": pictogram2.id,
        },
    ]

    response_data_results = response.data["results"]

    pictogram2_filename = response_data_results[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Hazard statements
    hazard_statement1, hazard_statement2 = hazard_statements

    client, _ = api_client_admin
    url = reverse("hazardstatement-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": hazard_statement1.id,
            "hazard_class": "Gazy łatwopalne",
            "clp_classification": {
                "id": clp_classification1.id,
                "repr": clp_classification1.clp_classification,
            },
            "pictogram": {
                "id": pictogram1.id,
            },
            "hazard_category": "Niestabilne materiały wybuchowe",
            "hazard_and_category_code": "Unst. Expl",
            "signal_word": "DGR",
            "code": "H200",
            "phrase": "Materiały wybuchowe niestabilne.",
            "is_usage_record_required": False,
        },
        {
            "id": hazard_statement2.id,
            "hazard_class": "Toksyczność ostra - Droga pokarmowa",
            "clp_classification": {
                "id": clp_classification2.id,
                "repr": clp_classification2.clp_classification,
            },
            "pictogram": {
                "id": pictogram2.id
            },
            "hazard_category": "kategoria 4",
            "hazard_and_category_code": "Acute Tox. 4",
            "signal_word": "WRN",
            "code": "H302",
            "phrase": "Działa szkodliwie po połknięciu.",
            "is_usage_record_required": False,
        },
    ]

    # Dropping pictogram representations because they get random suffixes
    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('hazardstatement-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected = [
        {
            "id": hazard_statement1.id,
            "hazard_class": "Gazy łatwopalne",
            "clp_classification": {
                "id": clp_classification1.id,
                "repr": clp_classification1.clp_classification,
            },
            "pictogram": {
                "id": pictogram1.id,
            },
            "hazard_category": "Niestabilne materiały wybuchowe",
            "hazard_and_category_code": "Unst. Expl",
            "signal_word": "DGR",
            "code": "H200",
            "phrase": "Materiały wybuchowe niestabilne.",
            "is_usage_record_required": False,
        },
        {
            "id": hazard_statement2.id,
            "hazard_class": "Toksyczność ostra - Droga pokarmowa",
            "clp_classification": {
                "id": clp_classification2.id,
                "repr": clp_classification2.clp_classification,
            },
            "pictogram": {
                "id": pictogram2.id
            },
            "hazard_category": "kategoria 4",
            "hazard_and_category_code": "Acute Tox. 4",
            "signal_word": "WRN",
            "code": "H302",
            "phrase": "Działa szkodliwie po połknięciu.",
            "is_usage_record_required": False,
        },
    ]
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('hazardstatement-list')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected.reverse()
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `code`
    url = f"{reverse('hazardstatement-list')}?ordering=code"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected = [
        {
            "id": hazard_statement1.id,
            "hazard_class": "Gazy łatwopalne",
            "clp_classification": {
                "id": clp_classification1.id,
                "repr": clp_classification1.clp_classification,
            },
            "pictogram": {
                "id": pictogram1.id,
            },
            "hazard_category": "Niestabilne materiały wybuchowe",
            "hazard_and_category_code": "Unst. Expl",
            "signal_word": "DGR",
            "code": "H200",
            "phrase": "Materiały wybuchowe niestabilne.",
            "is_usage_record_required": False,
        },
        {
            "id": hazard_statement2.id,
            "hazard_class": "Toksyczność ostra - Droga pokarmowa",
            "clp_classification": {
                "id": clp_classification2.id,
                "repr": clp_classification2.clp_classification,
            },
            "pictogram": {
                "id": pictogram2.id
            },
            "hazard_category": "kategoria 4",
            "hazard_and_category_code": "Acute Tox. 4",
            "signal_word": "WRN",
            "code": "H302",
            "phrase": "Działa szkodliwie po połknięciu.",
            "is_usage_record_required": False,
        },
    ]
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('hazardstatement-list')}?ordering=-code"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected.reverse()
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `phrase`
    url = f"{reverse('hazardstatement-list')}?ordering=phrase"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected = [
        {
            "id": hazard_statement2.id,
            "hazard_class": "Toksyczność ostra - Droga pokarmowa",
            "clp_classification": {
                "id": clp_classification2.id,
                "repr": clp_classification2.clp_classification,
            },
            "pictogram": {
                "id": pictogram2.id
            },
            "hazard_category": "kategoria 4",
            "hazard_and_category_code": "Acute Tox. 4",
            "signal_word": "WRN",
            "code": "H302",
            "phrase": "Działa szkodliwie po połknięciu.",
            "is_usage_record_required": False,
        },
        {
            "id": hazard_statement1.id,
            "hazard_class": "Gazy łatwopalne",
            "clp_classification": {
                "id": clp_classification1.id,
                "repr": clp_classification1.clp_classification,
            },
            "pictogram": {
                "id": pictogram1.id,
            },
            "hazard_category": "Niestabilne materiały wybuchowe",
            "hazard_and_category_code": "Unst. Expl",
            "signal_word": "DGR",
            "code": "H200",
            "phrase": "Materiały wybuchowe niestabilne.",
            "is_usage_record_required": False,
        },
    ]
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    url = f"{reverse('hazardstatement-list')}?ordering=-phrase"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    pictogram2_filename = response_data_results[1]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")

    expected.reverse()
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Searching
    # `code`
    url = f"{reverse('hazardstatement-list')}?search=30"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": hazard_statement2.id,
            "hazard_class": "Toksyczność ostra - Droga pokarmowa",
            "clp_classification": {
                "id": clp_classification2.id,
                "repr": clp_classification2.clp_classification,
            },
            "pictogram": {
                "id": pictogram2.id
            },
            "hazard_category": "kategoria 4",
            "hazard_and_category_code": "Acute Tox. 4",
            "signal_word": "WRN",
            "code": "H302",
            "phrase": "Działa szkodliwie po połknięciu.",
            "is_usage_record_required": False,
        },
    ]

    response_data_results = response.data["results"]
    pictogram2_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram2_filename.startswith("GHS07")
    assert pictogram2_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `phrase`
    url = f"{reverse('hazardstatement-list')}?search=wybuch"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": hazard_statement1.id,
            "hazard_class": "Gazy łatwopalne",
            "clp_classification": {
                "id": clp_classification1.id,
                "repr": clp_classification1.clp_classification,
            },
            "pictogram": {
                "id": pictogram1.id,
            },
            "hazard_category": "Niestabilne materiały wybuchowe",
            "hazard_and_category_code": "Unst. Expl",
            "signal_word": "DGR",
            "code": "H200",
            "phrase": "Materiały wybuchowe niestabilne.",
            "is_usage_record_required": False,
        },
    ]

    response_data_results = response.data["results"]
    pictogram1_filename = response_data_results[0]["pictogram"].pop("repr").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")
    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Precautionary statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    client, _ = api_client_admin
    url = reverse("precautionarystatement-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": precautionary_statement1.id,
            "code": "P201",
            "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
        },
        {
            "id": precautionary_statement2.id,
            "code": "P250",
            "phrase": "Nie poddawać szlifowaniu/wstrząsom/tarciu/….",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Ordering
    # `id`
    url = f"{reverse('precautionarystatement-list')}?ordering=id"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": precautionary_statement1.id,
            "code": "P201",
            "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
        },
        {
            "id": precautionary_statement2.id,
            "code": "P250",
            "phrase": "Nie poddawać szlifowaniu/wstrząsom/tarciu/….",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('precautionarystatement-list')}?ordering=-id"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `code`
    url = f"{reverse('precautionarystatement-list')}?ordering=code"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": precautionary_statement1.id,
            "code": "P201",
            "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
        },
        {
            "id": precautionary_statement2.id,
            "code": "P250",
            "phrase": "Nie poddawać szlifowaniu/wstrząsom/tarciu/….",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('precautionarystatement-list')}?ordering=-code"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `phrase`
    url = f"{reverse('precautionarystatement-list')}?ordering=phrase"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": precautionary_statement2.id,
            "code": "P250",
            "phrase": "Nie poddawać szlifowaniu/wstrząsom/tarciu/….",
        },
        {
            "id": precautionary_statement1.id,
            "code": "P201",
            "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    url = f"{reverse('precautionarystatement-list')}?ordering=-phrase"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # Searching
    # `code`
    url = f"{reverse('precautionarystatement-list')}?search=25"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": precautionary_statement2.id,
            "code": "P250",
            "phrase": "Nie poddawać szlifowaniu/wstrząsom/tarciu/….",
        },
    ]
    actual = json.loads(json.dumps(response.data["results"]))

    assert expected == actual

    # `phrase`
    url = f"{reverse('precautionarystatement-list')}?search=ostrożności"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": precautionary_statement1.id,
            "code": "P201",
            "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
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


@pytest.mark.django_db
def test_create_hazards(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                        api_client_anon, mock_files):
    # pylint: disable=no-member
    ClpClassification.history.all().delete()
    Pictogram.history.all().delete()
    HazardStatement.history.all().delete()
    PrecautionaryStatement.history.all().delete()
    # pylint: enable=no-member

    image_bytes, _ = mock_files

    # CLP classification
    client, admin = api_client_admin
    url = reverse("clpclassification-list")

    post_data = {
        "classification": "Substancje utleniające",
        "clp_classification": "GHS03",
        "hazard_group": "PHY",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    clp_classification_id = response.data["id"]
    db_clp_classification = ClpClassification.objects.get(pk=clp_classification_id)
    db_clp_classification_dict = model_to_dict(db_clp_classification)

    assert db_clp_classification_dict.pop("id") == clp_classification_id
    assert post_data == db_clp_classification_dict

    # Check history
    expected = [post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_clp_classification.id,
    }]

    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Pictograms
    client, _ = api_client_admin
    url = reverse("pictogram-list")

    post_data = {
        "pictogram": SimpleUploadedFile("GHS03.png", image_bytes),
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    pictogram_id = response.data["id"]
    db_pictogram = Pictogram.objects.get(pk=pictogram_id)

    assert db_pictogram.id == pictogram_id

    # Check history
    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_pictogram.id,
    }]

    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))
    pictogram_filename = actual[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS03")
    assert pictogram_filename.endswith(".png")
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Hazard statement
    client, _ = api_client_admin
    url = reverse("hazardstatement-list")
    post_data = {
        "hazard_class": "Gazy utleniające",
        "clp_classification": db_clp_classification.id,
        "pictogram": db_pictogram.id,
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Ox. Gas 1",
        "signal_word": "DGR",
        "code": "H270",
        "phrase": "Może spowodować lub intensyfikować pożar; utleniacz.",
        "is_usage_record_required": False,
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    hazard_statement_id = response.data["id"]
    db_hazard_statement = HazardStatement.objects.get(pk=hazard_statement_id)
    db_hazard_statement_dict = model_to_dict(db_hazard_statement)

    assert db_hazard_statement_dict.pop("id") == hazard_statement_id
    assert post_data == db_hazard_statement_dict

    # Check history
    history_data = post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_hazard_statement.id,
    }
    history_data["clp_classification"] = {
        "id": history_data["clp_classification"],
        "repr": db_clp_classification.clp_classification,
    }
    history_data["pictogram"] = {
        "id": history_data["pictogram"],
    }
    expected = [history_data]

    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))

    pictogram_actual_repr = actual[0]["pictogram"].pop("repr")
    pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS03")
    assert pictogram_filename.endswith(".png")

    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Precautionary statement
    client, _ = api_client_admin
    url = reverse("precautionarystatement-list")
    post_data = {
            "code": "P202",
            "phrase": "Nie używać przed zapoznaniem się i zrozumieniem wszystkich środków bezpieczeństwa.",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    precautionary_statement_id = response.data["id"]
    db_precautionary_statement = PrecautionaryStatement.objects.get(pk=precautionary_statement_id)
    db_precautionary_statement_dict = model_to_dict(db_precautionary_statement)

    assert db_precautionary_statement_dict.pop("id") == precautionary_statement_id
    assert post_data == db_precautionary_statement_dict

    # Check history
    expected = [post_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "+",
        "pk": db_precautionary_statement.id,
    }]

    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_hazards(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                          api_client_anon, clp_classifications, pictograms, hazard_statements,
                          precautionary_statements):
    # CLP classifications
    clp_classification1, _ = clp_classifications

    client, _ = api_client_admin
    url = reverse("clpclassification-detail", args=[clp_classification1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": clp_classification1.id,
        "classification": "Substancje łatwopalne",
        "clp_classification": "GHS02",
        "hazard_group": "PHY",
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

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual

    # Pictograms
    pictogram1, _ = pictograms

    client, _ = api_client_admin
    url = reverse("pictogram-detail", args=[pictogram1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Dropping filenames because they get random suffixes
    reponse_data = response.data

    pictogram1_filename = reponse_data.pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")

    expected = {
        "id": pictogram1.id,
    }
    actual = json.loads(json.dumps(reponse_data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    reponse_data = response.data

    pictogram1_filename = reponse_data.pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")

    actual = json.loads(json.dumps(reponse_data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    reponse_data = response.data

    pictogram1_filename = reponse_data.pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")

    actual = json.loads(json.dumps(reponse_data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    reponse_data = response.data

    pictogram1_filename = reponse_data.pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")

    actual = json.loads(json.dumps(reponse_data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    reponse_data = response.data

    pictogram1_filename = reponse_data.pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram1_filename.startswith("GHS02")
    assert pictogram1_filename.endswith(".png")

    actual = json.loads(json.dumps(reponse_data))

    assert expected == actual

    # Hazard statements
    hazard_statement1, _ = hazard_statements

    client, _ = api_client_admin
    url = reverse("hazardstatement-detail", args=[hazard_statement1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": hazard_statement1.id,
        "hazard_class": "Gazy łatwopalne",
        "clp_classification": {
            "id": clp_classification1.id,
            "repr": clp_classification1.clp_classification
        },
        "pictogram": {
            "id": pictogram1.id
        },
        "hazard_category": "Niestabilne materiały wybuchowe",
        "hazard_and_category_code": "Unst. Expl",
        "signal_word": "DGR",
        "code": "H200",
        "phrase": "Materiały wybuchowe niestabilne.",
        "is_usage_record_required": False,
    }

    response_data = response.data
    response_data["pictogram"].pop("repr")
    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    response_data["pictogram"].pop("repr")
    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    response_data["pictogram"].pop("repr")
    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    response_data["pictogram"].pop("repr")
    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.data
    response_data["pictogram"].pop("repr")
    actual = json.loads(json.dumps(response_data))

    assert expected == actual

    # Precautionary statements
    precautionary_statement1, _ = precautionary_statements

    client, _ = api_client_admin
    url = reverse("precautionarystatement-detail", args=[precautionary_statement1.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": precautionary_statement1.id,
        "code": "P201",
        "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
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

    assert response.status_code == status.HTTP_200_OK

    actual = json.loads(json.dumps(response.data))

    assert expected == actual


@pytest.mark.django_db
def test_update_hazards(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                        api_client_anon, clp_classifications, pictograms, hazard_statements, precautionary_statements,
                        mock_files):
    # pylint: disable=no-member
    ClpClassification.history.all().delete()
    Pictogram.history.all().delete()
    HazardStatement.history.all().delete()
    PrecautionaryStatement.history.all().delete()
    # pylint: enable=no-member

    image_bytes, _ = mock_files

    # CLP classifications
    clp_classification1, clp_classification2 = clp_classifications

    client, admin = api_client_admin
    url = reverse("clpclassification-detail", args=[clp_classification1.id])

    put_data = {
        "classification": "Substancje korodujące metale",
        "clp_classification": "GHS05",
        "hazard_group": "PHY",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    clp_classification1_id = clp_classification1.id
    db_clp_classification1 = ClpClassification.objects.get(pk=clp_classification1_id)

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_clp_classification1.id,
    }

    put_data["id"] = clp_classification1_id

    assert put_data == model_to_dict(db_clp_classification1)

    url = reverse("clpclassification-detail", args=[clp_classification2.id])

    put_data = {
        "classification": "Substancje rakotwórcze / mutagenne",
        "clp_classification": "GHS08",
        "hazard_group": "HEA",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    clp_classification2_id = clp_classification2.id
    db_clp_classification2 = ClpClassification.objects.get(pk=clp_classification2_id)

    history_data2 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_clp_classification2.id,
    }

    put_data["id"] = clp_classification2_id

    assert put_data == model_to_dict(db_clp_classification2)

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('clpclassification-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('clpclassification-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `clp_classification`
    response = client.get(f"{reverse('clpclassification-get-historical-records')}?ordering=clp_classification")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('clpclassification-get-historical-records')}?ordering=-clp_classification")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `clp_classification`
    response = client.get(f"{reverse('clpclassification-get-historical-records')}?search=08")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Pictograms
    pictogram1, pictogram2 = pictograms

    ghs_names = ["GHS05", "GHS08"]
    client, _ = api_client_admin
    url = reverse("pictogram-detail", args=[pictogram1.id])

    ghs_name = ghs_names[0]
    put_data = {
        "pictogram": SimpleUploadedFile(f"{ghs_name}.png", image_bytes),
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    pictogram1_id = pictogram1.id
    db_pictogram1 = Pictogram.objects.get(pk=pictogram1_id)
    db_pictogram_dict = model_to_dict(db_pictogram1)

    assert pictogram1_id == db_pictogram1.id

    pictogram1_filename = str(db_pictogram_dict.pop("pictogram")).rsplit("/", maxsplit=1)[-1]

    assert pictogram1_filename.startswith(ghs_name)
    assert pictogram1_filename.endswith(".png")

    history_data1 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_pictogram1.id,
    }

    url = reverse("pictogram-detail", args=[pictogram2.id])

    ghs_name = ghs_names[1]
    put_data = {
        "pictogram": SimpleUploadedFile(f"{ghs_name}.png", image_bytes),
    }
    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    pictogram2_id = pictogram2.id
    db_pictogram2 = Pictogram.objects.get(pk=pictogram2_id)
    db_pictogram_dict = model_to_dict(db_pictogram2)

    assert pictogram2_id == db_pictogram2.id

    pictogram2_filename = str(db_pictogram_dict.pop("pictogram")).rsplit("/", maxsplit=1)[-1]

    assert pictogram2_filename.startswith(ghs_name)
    assert pictogram2_filename.endswith(".png")

    history_data2 = {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_pictogram2.id,
    }

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_filename = history_row.pop("pictogram").rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('pictogram-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, ghs_name in zip(actual, ghs_names):
        pictogram_filename = history_row.pop("pictogram").rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('pictogram-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_filename = history_row.pop("pictogram").rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `pictogram` (filename)
    response = client.get(f"{reverse('pictogram-get-historical-records')}?ordering=pictogram")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, ghs_name in zip(actual, ghs_names):
        pictogram_filename = history_row.pop("pictogram").rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('pictogram-get-historical-records')}?ordering=-pictogram")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_filename = history_row.pop("pictogram").rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `pictogram` (filename)
    response = client.get(f"{reverse('pictogram-get-historical-records')}?search=05")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    pictogram_filename = actual[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith(ghs_names[0])
    assert pictogram_filename.endswith(".png")
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Hazard statements
    hazard_statement1, hazard_statement2 = hazard_statements

    client, _ = api_client_admin
    url = reverse("hazardstatement-detail", args=[hazard_statement1.id])

    put_data = {
        "hazard_class": "Substancje i mieszaniny powodujące korozję metali",
        "clp_classification": db_clp_classification1.id,
        "pictogram": db_pictogram1.id,
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Met. Corr. 1",
        "signal_word": "WRN",
        "code": "H290",
        "phrase": "Może powodować korozję metali.",
        "is_usage_record_required": False,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    hazard_statement1_id = response.data["id"]
    db_hazard_statement = HazardStatement.objects.get(pk=hazard_statement1_id)
    db_hazard_statement_dict = model_to_dict(db_hazard_statement)

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_hazard_statement.id,
    }
    history_data1["clp_classification"] = {
        "id": history_data1["clp_classification"],
        "repr": db_clp_classification1.clp_classification,
    }
    history_data1["pictogram"] = {
        "id": history_data1["pictogram"],
    }

    put_data["id"] = hazard_statement1_id
    assert put_data == db_hazard_statement_dict

    url = reverse("hazardstatement-detail", args=[hazard_statement2.id])

    put_data = {
        "hazard_class": "Działanie mutagenne na komórki rozrodcze",
        "clp_classification": db_clp_classification2.id,
        "pictogram": db_pictogram2.id,
        "hazard_category": "kategoria 1A",
        "hazard_and_category_code": "Muta. 1A",
        "signal_word": "DGR",
        "code": "H340",
        "phrase": "Może powodować wady genetyczne (podać drogę narażenia, jeżeli definitywnie udowodniono, "
                  "że inna droga narażenia nie powoduje zagrożenia).",
        "is_usage_record_required": True,
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    hazard_statement2_id = response.data["id"]
    db_hazard_statement = HazardStatement.objects.get(pk=hazard_statement2_id)
    db_hazard_statement_dict = model_to_dict(db_hazard_statement)

    history_data2 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_hazard_statement.id,
    }
    history_data2["clp_classification"] = {
        "id": history_data2["clp_classification"],
        "repr": db_clp_classification2.clp_classification,
    }
    history_data2["pictogram"] = {
        "id": history_data2["pictogram"],
    }

    put_data["id"] = hazard_statement2_id
    assert put_data == db_hazard_statement_dict

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, ghs_names):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `code`
    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?ordering=code")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, ghs_names):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?ordering=-code")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `phrase`
    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?ordering=phrase")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, ghs_names):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?ordering=-phrase")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))

    for history_row, ghs_name in zip(actual, reversed(ghs_names)):
        pictogram_actual_repr = history_row["pictogram"].pop("repr")
        pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
        assert pictogram_filename.startswith(ghs_name)
        assert pictogram_filename.endswith(".png")

        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `code`
    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?search=3")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))

    pictogram_actual_repr = actual[0]["pictogram"].pop("repr")
    pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith(ghs_names[1])
    assert pictogram_filename.endswith(".png")

    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    # `phrase`
    response = client.get(f"{reverse('hazardstatement-get-historical-records')}?search=metal")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))

    pictogram_actual_repr = actual[0]["pictogram"].pop("repr")
    pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith(ghs_names[0])
    assert pictogram_filename.endswith(".png")

    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Precautionary statement
    precautionary_statement1, precautionary_statement2 = precautionary_statements

    client, _ = api_client_admin
    url = reverse("precautionarystatement-detail", args=[precautionary_statement1.id])

    put_data = {
        "code": "P101",
        "phrase": "W razie konieczności zasięgnięcia porady lekarza należy pokazać pojemnik lub etykietę.",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    precautionary_statement1_id = response.data["id"]
    db_precautionary_statement = PrecautionaryStatement.objects.get(pk=precautionary_statement1_id)
    db_precautionary_statement_dict = model_to_dict(db_precautionary_statement)

    history_data1 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_precautionary_statement.id,
    }

    put_data["id"] = precautionary_statement1_id
    assert put_data == db_precautionary_statement_dict

    url = reverse("precautionarystatement-detail", args=[precautionary_statement2.id])

    put_data = {
        "code": "P235 + P410",
        "phrase": "Przechowywać w chłodnym miejscu. Chronić przed światłem słonecznym.",
    }
    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_200_OK

    precautionary_statement2_id = response.data["id"]
    db_precautionary_statement = PrecautionaryStatement.objects.get(pk=precautionary_statement2_id)
    db_precautionary_statement_dict = model_to_dict(db_precautionary_statement)

    history_data2 = put_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_precautionary_statement.id,
    }

    put_data["id"] = precautionary_statement2_id
    assert put_data == db_precautionary_statement_dict

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Ordering
    # `id`
    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?ordering=id")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?ordering=-id")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `code`
    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?ordering=code")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1, history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?ordering=-code")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # `phrase`
    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?ordering=phrase")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2, history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?ordering=-phrase")

    assert response.status_code == status.HTTP_200_OK

    expected.reverse()
    actual = json.loads(json.dumps(response.data["results"]))
    for history_row in actual:
        int(history_row.pop("id"))
        assert_timezone_now_gte_datetime(history_row.pop("history_date"))

    assert expected == actual

    # Searching
    # `code`
    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?search=4")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data2]
    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    # `phrase`
    response = client.get(f"{reverse('precautionarystatement-get-historical-records')}?search=lekarz")

    assert response.status_code == status.HTTP_200_OK

    expected = [history_data1]
    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.put(url, put_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_partial_update_hazards(api_client_admin, api_client_lab_manager, api_client_project_manager,
                                api_client_lab_worker, api_client_anon, clp_classifications, pictograms,
                                hazard_statements, precautionary_statements, mock_files):
    # pylint: disable=no-member
    ClpClassification.history.all().delete()
    Pictogram.history.all().delete()
    HazardStatement.history.all().delete()
    PrecautionaryStatement.history.all().delete()
    # pylint: enable=no-member

    image_bytes, _ = mock_files

    # CLP classifications
    clp_classification1, _ = clp_classifications

    client, admin = api_client_admin
    url = reverse("clpclassification-detail", args=[clp_classification1.id])

    patch_data = {
        "classification": "Substancje toksyczne",
        "clp_classification": "GHS06",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_clp_classification = ClpClassification.objects.get(pk=response.data["id"])

    assert patch_data["classification"] == db_clp_classification.classification
    assert patch_data["clp_classification"] == db_clp_classification.clp_classification

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [patch_data | {
        "hazard_group": "PHY",
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_clp_classification.id,
    }]
    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

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

    # Pictograms
    pictogram1, _ = pictograms

    client, _ = api_client_admin
    url = reverse("pictogram-detail", args=[pictogram1.id])

    patch_data = {
        "pictogram": SimpleUploadedFile("GHS06.png", image_bytes),
    }
    response = client.patch(url, patch_data, format="multipart")

    assert response.status_code == status.HTTP_200_OK

    db_pictogram = Pictogram.objects.get(pk=response.data["id"])
    db_pictogram_dict = model_to_dict(db_pictogram)

    pictogram_filename = str(db_pictogram_dict.pop("pictogram")).rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS06")
    assert pictogram_filename.endswith(".png")

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_pictogram.id,
    }]
    actual = json.loads(json.dumps(response.data["results"]))
    pictogram_filename = actual[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS06")
    assert pictogram_filename.endswith(".png")
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

    response = client.patch(url, patch_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_project_manager

    response = client.patch(url, patch_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client, _ = api_client_lab_worker

    response = client.patch(url, patch_data, format="multipart")

    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = api_client_anon

    response = client.patch(url, patch_data, format="multipart")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Hazard statements
    hazard_statement1, _ = hazard_statements

    client, _ = api_client_admin
    url = reverse("hazardstatement-detail", args=[hazard_statement1.id])

    patch_data = {
        "hazard_class": "Toksyczność ostra - Droga pokarmowa",
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Acute Tox. 1",
        "signal_word": "DGR",
        "code": "H300",
        "phrase": "Połknięcie grozi śmiercią.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_hazard_statement = HazardStatement.objects.get(pk=response.data["id"])

    assert patch_data.items() <= model_to_dict(db_hazard_statement).items()

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    history_data = patch_data | {
        "is_usage_record_required": False,
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_hazard_statement.id,
    }
    history_data["clp_classification"] = {
        "id": db_clp_classification.id,
        "repr": db_clp_classification.clp_classification,
    }
    history_data["pictogram"] = {
        "id": db_pictogram.id,
    }
    expected = [history_data]
    actual = json.loads(json.dumps(response.data["results"]))

    pictogram_actual_repr = actual[0]["pictogram"].pop("repr")
    pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS06")
    assert pictogram_filename.endswith(".png")

    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

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

    # Precautionary statement
    precautionary_statement1, _ = precautionary_statements

    client, _ = api_client_admin
    url = reverse("precautionarystatement-detail", args=[precautionary_statement1.id])

    patch_data = {
        "code": "P102",
        "phrase": "Chronić przed dziećmi.",
    }
    response = client.patch(url, patch_data)

    assert response.status_code == status.HTTP_200_OK

    db_precautionary_statement = PrecautionaryStatement.objects.get(pk=response.data["id"])

    assert patch_data.items() <= model_to_dict(db_precautionary_statement).items()

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [patch_data | {
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "~",
        "pk": db_precautionary_statement.id,
    }]
    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    client, _ = api_client_lab_manager

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


@pytest.mark.django_db
def test_destroy_hazards(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                         api_client_anon, clp_classifications, pictograms, hazard_statements, precautionary_statements):
    # pylint: disable=no-member
    ClpClassification.history.all().delete()
    Pictogram.history.all().delete()
    HazardStatement.history.all().delete()
    PrecautionaryStatement.history.all().delete()
    # pylint: enable=no-member

    # All ForeignKey fields in HazardStatement are protected, so their reference cannot be deleted before they
    # themselves are deleted.

    # CLP classifications
    clp_classification1, clp_classification2 = clp_classifications
    clp_classification_id = clp_classification1.id

    client, admin = api_client_admin
    url = reverse("clpclassification-detail", args=[clp_classification_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Pictograms
    pictogram1, pictogram2 = pictograms
    pictogram_id = pictogram1.id

    url = reverse("pictogram-detail", args=[pictogram_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Hazard statements
    hazard_statement1, hazard_statement2 = hazard_statements
    hazard_statement_id = hazard_statement1.id

    url = reverse("hazardstatement-detail", args=[hazard_statement_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not HazardStatement.objects.filter(pk=hazard_statement_id).exists()

    # Check history
    response = client.get(reverse("hazardstatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": clp_classification1.id,
        "hazard_class": "Gazy łatwopalne",
        "clp_classification": {
            "id": clp_classification1.id,
            "repr": clp_classification1.clp_classification,
        },
        "pictogram": {
            "id": pictogram1.id,
        },
        "hazard_category": "Niestabilne materiały wybuchowe",
        "hazard_and_category_code": "Unst. Expl",
        "signal_word": "DGR",
        "code": "H200",
        "phrase": "Materiały wybuchowe niestabilne.",
        "is_usage_record_required": False,
    }]
    actual = json.loads(json.dumps(response.data["results"]))

    pictogram_actual_repr = actual[0]["pictogram"].pop("repr")
    pictogram_filename = pictogram_actual_repr.rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS02")
    assert pictogram_filename.endswith(".png")

    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    hazard_statement_id = hazard_statement2.id
    url = reverse("hazardstatement-detail", args=[hazard_statement_id])

    client, _ = api_client_lab_manager
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

    # Now we can remove the related fields.

    # CLP classifications
    clp_classification1, clp_classification2 = clp_classifications
    clp_classification_id = clp_classification1.id

    client, _ = api_client_admin
    url = reverse("clpclassification-detail", args=[clp_classification_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not ClpClassification.objects.filter(pk=clp_classification_id).exists()

    # Check history
    response = client.get(reverse("clpclassification-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": clp_classification_id,
        "classification": "Substancje łatwopalne",
        "clp_classification": "GHS02",
        "hazard_group": "PHY",
    }]
    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    clp_classification_id = clp_classification2.id
    url = reverse("clpclassification-detail", args=[clp_classification_id])

    client, _ = api_client_lab_manager
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

    # Pictograms
    pictogram1, pictogram2 = pictograms
    pictogram_id = pictogram1.id

    client, _ = api_client_admin
    url = reverse("pictogram-detail", args=[pictogram_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Pictogram.objects.filter(pk=pictogram_id).exists()

    # Check history
    response = client.get(reverse("pictogram-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "pk": pictogram_id,
    }]
    actual = json.loads(json.dumps(response.data["results"]))
    pictogram_filename = actual[0].pop("pictogram").rsplit('/', maxsplit=1)[-1]
    assert pictogram_filename.startswith("GHS02")
    assert pictogram_filename.endswith(".png")
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    pictogram_id = pictogram2.id
    url = reverse("pictogram-detail", args=[pictogram_id])

    client, _ = api_client_lab_manager
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

    # Precautionary statements
    precautionary_statement1, precautionary_statement2 = precautionary_statements
    precautionary_statement_id = precautionary_statement1.id

    client, _ = api_client_admin
    url = reverse("precautionarystatement-detail", args=[precautionary_statement_id])
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not PrecautionaryStatement.objects.filter(pk=precautionary_statement_id).exists()

    # Check history
    response = client.get(reverse("precautionarystatement-get-historical-records"))

    assert response.status_code == status.HTTP_200_OK

    expected = [{
        "history_user": admin.id,
        "history_change_reason": None,
        "history_type": "-",
        "code": "P201",
        "phrase": "Przed użyciem zapoznać się ze specjalnymi środkami ostrożności.",
        "pk": precautionary_statement_id,
    }]
    actual = json.loads(json.dumps(response.data["results"]))
    int(actual[0].pop("id"))
    assert_timezone_now_gte_datetime(actual[0].pop("history_date"))

    assert expected == actual

    precautionary_statement_id = precautionary_statement2.id
    url = reverse("precautionarystatement-detail", args=[precautionary_statement_id])

    client, _ = api_client_lab_manager
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
def test_get_ghs_pictograms(api_client_admin, api_client_lab_manager, api_client_project_manager, api_client_lab_worker,
                            api_client_anon, mock_files):
    image_bytes, _ = mock_files

    client, _ = api_client_admin

    # Create a pictogram which sits in two hazard groups
    url = reverse("clpclassification-list")

    post_data = {
        "classification": "Substancje rakotwórcze / mutagenne",
        "clp_classification": "GHS08",
        "hazard_group": "HEA",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    clp_classification1 = ClpClassification.objects.get(pk=response.data["id"])

    post_data = {
        "classification": "Substancje szkodliwe dla środowiska",
        "clp_classification": "GHS09",
        "hazard_group": "ENV",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    clp_classification2 = ClpClassification.objects.get(pk=response.data["id"])

    post_data = {
        "classification": "Substancje korodujące metale",
        "clp_classification": "GHS05",
        "hazard_group": "PHY",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    clp_classification3 = ClpClassification.objects.get(pk=response.data["id"])

    post_data = {
        "classification": "Substancje żrące",
        "clp_classification": "GHS05",
        "hazard_group": "HEA",
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    clp_classification4 = ClpClassification.objects.get(pk=response.data["id"])

    url = reverse("pictogram-list")

    post_data = {
        "pictogram": SimpleUploadedFile("GHS08.png", image_bytes),
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    pictogram1 = Pictogram.objects.get(pk=response.data["id"])

    post_data = {
        "pictogram": SimpleUploadedFile("GHS09.png", image_bytes),
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    pictogram2 = Pictogram.objects.get(pk=response.data["id"])

    post_data = {
        "pictogram": SimpleUploadedFile("GHS05.png", image_bytes),
    }
    response = client.post(url, post_data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED

    pictogram3 = Pictogram.objects.get(pk=response.data["id"])

    url = reverse("hazardstatement-list")

    # Standard hazard statement
    post_data = {
        "hazard_class": "Zagrożenie spowodowane aspiracją",
        "clp_classification": clp_classification1.id,
        "pictogram": pictogram1.id,
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Asp. Tox. 1",
        "signal_word": "DGR",
        "code": "H304",
        "phrase": "Połknięcie i dostanie się przez drogi oddechowe może grozić śmiercią.",
        "is_usage_record_required": False,
    }

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    # Hazard statement without a pictogram
    post_data = {
        "hazard_class": "Wpływ na laktację lub oddziaływanie szkodliwe na dzieci karmione piersią",
        "clp_classification": clp_classification1.id,
        "hazard_category": "laktacja",
        "hazard_and_category_code": "Lact.",
        "signal_word": "",
        "code": "H362",
        "phrase": "Może działać szkodliwie na dzieci karmione piersią.",
        "is_usage_record_required": True,
    }

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    # Two hazard statements with the same pictogram
    post_data = {
        "hazard_class": "Ostre zagrożenie dla środowiska dla środowiska wodnego",
        "clp_classification": clp_classification2.id,
        "pictogram": pictogram2.id,
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Acuatic Acute 1",
        "signal_word": "DGR",
        "code": "H400",
        "phrase": "Działa bardzo toksycznie na organizmy wodne.",
        "is_usage_record_required": False,
    }

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    post_data = {
        "hazard_class": "Przewlekłe (długotrwałe) zagrożenie dla środowiska wodnego",
        "clp_classification": clp_classification2.id,
        "pictogram": pictogram2.id,
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Acuatic Chronic 1",
        "signal_word": "WRN",
        "code": "H410",
        "phrase": "Działa bardzo toksycznie na organizmy wodne, powodując długotrwałe skutki.",
        "is_usage_record_required": False,
    }

    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    # Hazard statements with the same pictogram but in different hazard groups
    post_data = {
        "hazard_class": "Substancje i mieszaniny powodujące korozję metali",
        "clp_classification": clp_classification3.id,
        "pictogram": pictogram3.id,
        "hazard_category": "kategoria 1",
        "hazard_and_category_code": "Met. Corr. 1",
        "signal_word": "WRN",
        "code": "H290",
        "phrase": "Może powodować korozję metali.",
        "is_usage_record_required": False,
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    post_data = {
        "hazard_class": "Substancje żrące na skórę",
        "clp_classification": clp_classification4.id,
        "pictogram": pictogram3.id,
        "hazard_category": "kategoria 1A",
        "hazard_and_category_code": "Skin Corr. 1A",
        "signal_word": "DGR",
        "code": "H314",
        "phrase": "Powoduje poważne oparzenia skóry oraz uszkodzenia oczu.",
        "is_usage_record_required": True,
    }
    response = client.post(url, post_data)

    assert response.status_code == status.HTTP_201_CREATED

    url = reverse("hazardstatement-get-ghs-pictograms")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification3.id,
            "clp_classification": 'GHS05',
            "classification": "Substancje korodujące metale",
        },
        {
            "id": clp_classification4.id,
            "clp_classification": "GHS05",
            "classification": "Substancje żrące",
        },
        {
            "id": clp_classification1.id,
            "clp_classification": "GHS08",
            "classification": "Substancje rakotwórcze / mutagenne",
        },
        {
            "id": clp_classification2.id,
            "clp_classification": "GHS09",
            "classification": "Substancje szkodliwe dla środowiska",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification3.id,
            "clp_classification": 'GHS05',
            "classification": "Substancje korodujące metale",
        },
        {
            "id": clp_classification4.id,
            "clp_classification": "GHS05",
            "classification": "Substancje żrące",
        },
        {
            "id": clp_classification1.id,
            "clp_classification": "GHS08",
            "classification": "Substancje rakotwórcze / mutagenne",
        },
        {
            "id": clp_classification2.id,
            "clp_classification": "GHS09",
            "classification": "Substancje szkodliwe dla środowiska",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_project_manager
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification3.id,
            "clp_classification": 'GHS05',
            "classification": "Substancje korodujące metale",
        },
        {
            "id": clp_classification4.id,
            "clp_classification": "GHS05",
            "classification": "Substancje żrące",
        },
        {
            "id": clp_classification1.id,
            "clp_classification": "GHS08",
            "classification": "Substancje rakotwórcze / mutagenne",
        },
        {
            "id": clp_classification2.id,
            "clp_classification": "GHS09",
            "classification": "Substancje szkodliwe dla środowiska",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client, _ = api_client_lab_worker
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification3.id,
            "clp_classification": 'GHS05',
            "classification": "Substancje korodujące metale",
        },
        {
            "id": clp_classification4.id,
            "clp_classification": "GHS05",
            "classification": "Substancje żrące",
        },
        {
            "id": clp_classification1.id,
            "clp_classification": "GHS08",
            "classification": "Substancje rakotwórcze / mutagenne",
        },
        {
            "id": clp_classification2.id,
            "clp_classification": "GHS09",
            "classification": "Substancje szkodliwe dla środowiska",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    client = api_client_anon
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification3.id,
            "clp_classification": 'GHS05',
            "classification": "Substancje korodujące metale",
        },
        {
            "id": clp_classification4.id,
            "clp_classification": "GHS05",
            "classification": "Substancje żrące",
        },
        {
            "id": clp_classification1.id,
            "clp_classification": "GHS08",
            "classification": "Substancje rakotwórcze / mutagenne",
        },
        {
            "id": clp_classification2.id,
            "clp_classification": "GHS09",
            "classification": "Substancje szkodliwe dla środowiska",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # Search
    # `clp_classification`
    url = f"{reverse('hazardstatement-get-ghs-pictograms')}?search=05"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification3.id,
            "clp_classification": 'GHS05',
            "classification": "Substancje korodujące metale",
        },
        {
            "id": clp_classification4.id,
            "clp_classification": "GHS05",
            "classification": "Substancje żrące",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual

    # `classification`
    url = f"{reverse('hazardstatement-get-ghs-pictograms')}?search=rak"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected = [
        {
            "id": clp_classification1.id,
            "clp_classification": "GHS08",
            "classification": "Substancje rakotwórcze / mutagenne",
        },
    ]

    response_data_results = response.data["results"]
    for i, ghs_pictogram in enumerate(response_data_results):
        pictogram_filename = str(ghs_pictogram.pop("pictogram")).rsplit("/", maxsplit=1)[-1]
        assert pictogram_filename.startswith(expected[i]["clp_classification"])
        assert pictogram_filename.endswith(".png")

    actual = json.loads(json.dumps(response_data_results))

    assert expected == actual
