import os
import io

from collections import defaultdict

from django.db.models import Count, F
from django.db.models.functions import ExtractYear
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from reagents.models import HazardStatement, PersonalReagent

REGULAR_FONT = "REGULAR_FONT"
pdfmetrics.registerFont(TTFont(REGULAR_FONT, os.environ[REGULAR_FONT]))
BOLD_FONT = "BOLD_FONT"
pdfmetrics.registerFont(TTFont(BOLD_FONT, os.environ[BOLD_FONT]))
ITALIC_FONT = "ITALIC_FONT"
pdfmetrics.registerFont(TTFont(ITALIC_FONT, os.environ[ITALIC_FONT]))

STYLES = getSampleStyleSheet()

# In the template the margin was 0.98" (0.49" for the bottom one).
# We use 0.98" for every margin here. The footer is going to be lowered by 0.49" accordingly.
MARGIN = 0.98 * inch
HEADER_AND_FOOTER_HEIGHT = 0.49 * inch


# REPORTS

class UsageRecordCanvas(Canvas):  # pylint: disable=abstract-method
    """http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    http://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    https://stackoverflow.com/a/59882495
    Modified for more footer information.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        """On a page break, add information to the list."""
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Add the footer to each page."""
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_footer(page_count)
            super().showPage()

        super().save()

    def draw_footer(self, page_count):
        """Add the footer."""

        # In the template these two are not horizontally aligned. We change that here for better visual effect.
        # The font size stays the same.
        self.setFont(REGULAR_FONT, 10)
        self.drawRightString(A4[0] - MARGIN, HEADER_AND_FOOTER_HEIGHT, f"Strona {self._pageNumber} z {page_count}")

        self.setFont(ITALIC_FONT, 11)
        self.drawString(MARGIN, HEADER_AND_FOOTER_HEIGHT, "* Niepotrzebne skreślić")


def generate_usage_record_data(personal_reagent):
    reagent = personal_reagent.reagent
    clp_classifications = reagent.hazard_statements.distinct(
        "clp_classification__id", "clp_classification__clp_classification"
    ).order_by(
        "clp_classification__clp_classification"
    ).values_list(
        "clp_classification__clp_classification",
        flat=True
    )
    clp_classifications = ", ".join(clp_classifications)
    storage_conditions = ", ".join(map(lambda x: x.storage_condition, reagent.storage_conditions.all()))
    reagent_data = [
        ["Nazwa odczynnika", reagent.name],
        ["Producent", reagent.producer.abbreviation],
        ["Nr katalogowy", reagent.catalog_no],
        ["Jednostka miary", f"{reagent.volume} {reagent.unit}"],
        ["Lot/Batch/Nr serii", personal_reagent.lot_no],
        ["Data przysłania", personal_reagent.receipt_purchase_date],
        ["Data ważności", personal_reagent.expiration_date],
        ["Warunki przechowywania", storage_conditions],
        ["Kupujący", personal_reagent.main_owner],
        ["Pracownia/Pokój", personal_reagent.room],
        ["Lokalizacja", personal_reagent.detailed_location],
        ["Klasyfikacja zagrożenia", clp_classifications],
        ["Data otwarcia i sprawdzenia", ""],
        ["Osoba sprawdzająca (podpis)", ""],
        ["Uwagi / porcjonowanie", ""],
    ]

    return reagent_data


def generate_usage_record(personal_reagent, num_of_entries):
    io_buffer = io.BytesIO()
    pdf_doc = SimpleDocTemplate(
        io_buffer,
        pagesize=A4,
        title="Karta rozchodu",
        author=str(personal_reagent.main_owner),
        subject="Pliki dot. odczynników",
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )

    title_style = STYLES["Title"]
    title_style.fontName = REGULAR_FONT
    title_style.fontSize = 15
    title = Paragraph("KARTA ZUŻYCIA/ROZCHODU ODCZYNNIKA", title_style)

    reagent_data = generate_usage_record_data(personal_reagent)

    column_width = (A4[0] - 2 * MARGIN) / 2
    reagent_data_table = Table(reagent_data, colWidths=[column_width, column_width])

    reagent_data_table_style = TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("0xF2F2F2")),  # "Gray" background for the first column
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add a border to all cells
        ("FONTNAME", (0, 0), (0, -1), BOLD_FONT),  # Bold text in the left column
        ("FONTNAME", (1, 0), (1, -1), REGULAR_FONT),  # Standard font in the right column
        ("FONTSIZE", (0, 0), (-1, -1), 10),  # Font size from the template
    ])
    reagent_data_table.setStyle(reagent_data_table_style)

    entries = [["Lp.", "Data", "Ilość [µl/ml/L*]", "Podpis"]]
    for i in range(1, num_of_entries + 1):
        entries.append([str(i), "", "", ""])

    ordinal_numbers_column_width = 30  # Fits 3-digit numbers and leaves some padding for better visual effect
    data_column_width = (A4[0] - 2 * MARGIN - ordinal_numbers_column_width) / 3
    entries_table = Table(
        entries,
        colWidths=[ordinal_numbers_column_width, data_column_width, data_column_width, data_column_width],
        repeatRows=1,
    )

    entries_table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("0xF2F2F2")),  # "Gray" background for the first row
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add a border to all cells
        ("ALIGN", (0, 1), (-1, -1), "RIGHT"),  # Align text right within the column
        ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),  # Bold text in the first row
        ("FONTNAME", (0, 1), (1, -1), REGULAR_FONT),  # Standard font in the rest
        ("FONTSIZE", (0, 0), (-1, -1), 10),  # Font size from the template
    ])
    entries_table.setStyle(entries_table_style)

    pdf_doc.build([title, reagent_data_table, Spacer(1, 15), entries_table], canvasmaker=UsageRecordCanvas)

    return io_buffer


class ReportCanvas(Canvas):  # pylint: disable=abstract-method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        """On a page break, add information to the list."""
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Add the header and the footer to each page."""
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_header_and_footer(page_count)
            super().showPage()

        super().save()

    def draw_header_and_footer(self, page_count):
        """Add the header and the footer."""
        self.setFont(REGULAR_FONT, 5)

        self.drawString(MARGIN, A4[0] - HEADER_AND_FOOTER_HEIGHT, 60 * ".")
        self.drawString(MARGIN, A4[0] - HEADER_AND_FOOTER_HEIGHT - 15, "Podpis")

        self.drawRightString(
            A4[1] - MARGIN,
            A4[0] - HEADER_AND_FOOTER_HEIGHT,
            timezone.localtime(timezone.now()).strftime("%Y-%m-%d, %H:%M:%S")
        )

        self.drawRightString(A4[1] - MARGIN, HEADER_AND_FOOTER_HEIGHT, f"Strona {self._pageNumber} z {page_count}")


def generate_sanepid_pip_report_data(personal_reagents_queryset):
    report_data = [[
        "Lp.",
        "Nazwa odczynnika",
        "Producent (marka)",
        "Laboratorium",
        "Pracownia/pokój",
        "Główny użytkownik",
        "Data przyjęcia/zakupu",
        "Klasyfikacja CLP",
        "Nr instrukcji bezpieczeństwa",
    ]]
    for idx, personal_reagent in enumerate(personal_reagents_queryset, 1):
        reagent = personal_reagent.reagent
        clp_classifications = {}
        for hazard_statement in reagent.hazard_statements.all():
            clp_classifications[str(hazard_statement.clp_classification)] = None
        clp_classifications = ", ".join(clp_classifications.keys())
        report_data.append([
            idx,
            reagent.name,
            reagent.producer.abbreviation,
            personal_reagent.laboratory,
            personal_reagent.room,
            personal_reagent.main_owner,
            personal_reagent.receipt_purchase_date,
            clp_classifications,
            personal_reagent.reagent.safety_instruction_name,
        ])

    return report_data


def generate_lab_manager_report_data(personal_reagents_queryset):
    report_data = [[
        "Lp.",
        "Nazwa odczynnika",
        "Producent (marka)",
        "Laboratorium",
        "Pracownia/pokój",
        "Główny użytkownik",
        "Data przyjęcia/zakupu",
        "Data ważności",
        "Klasyfikacja CLP",
        "Nr instrukcji bezpieczeństwa",
        "Rodzaj odczynnika",
    ]]
    for idx, personal_reagent in enumerate(personal_reagents_queryset, 1):
        reagent = personal_reagent.reagent
        clp_classifications = {}
        for hazard_statement in reagent.hazard_statements.all():
            clp_classifications[str(hazard_statement.clp_classification)] = None
        clp_classifications = ", ".join(clp_classifications.keys())
        report_data.append([
            idx,
            reagent.name,
            reagent.producer.abbreviation,
            personal_reagent.laboratory,
            personal_reagent.room,
            personal_reagent.main_owner,
            personal_reagent.receipt_purchase_date,
            personal_reagent.expiration_date,
            clp_classifications,
            reagent.safety_instruction_name,
            reagent.type,
        ])

    return report_data


def generate_projects_procedures_report_data(personal_reagents_queryset):
    report_data = [[
        "Lp.",
        "Projekt / procedura",
        "Nazwa odczynnika",
        "Producent (marka)",
        "Laboratorium",
        "Pracownia/pokój",
        "Lokalizacja szczegółowa",
        "Główny użytkownik",
        "Data przyjęcia/zakupu",
        "Data ważności",
        "Klasyfikacja CLP",
    ]]
    for idx, personal_reagent in enumerate(personal_reagents_queryset, 1):
        reagent = personal_reagent.reagent
        clp_classifications = {}
        for hazard_statement in reagent.hazard_statements.all():
            clp_classifications[str(hazard_statement.clp_classification)] = None
        clp_classifications = ", ".join(clp_classifications.keys())
        report_data.append([
            idx,
            personal_reagent.project_procedure,
            reagent.name,
            reagent.producer.abbreviation,
            personal_reagent.laboratory,
            personal_reagent.room,
            personal_reagent.detailed_location,
            personal_reagent.main_owner,
            personal_reagent.receipt_purchase_date,
            personal_reagent.expiration_date,
            clp_classifications,
        ])

    return report_data


def generate_all_personal_reagents_report_data(personal_reagents_queryset):
    report_data = [[
        "Lp.",
        "Nazwa\n"
        "odczynnika",
        "Producent\n"
        "(marka)",
        "Nr katologowy",
        "LOT",
        "Główny\n"
        "użytkownik",
        "Projekt/\n"
        "procedura",
        "Odczynnik\n"
        "kluczowy",
        "Klasyfikacja CLP",
        "Data przyjęcia/\n"
        "zakupu",
        "Data ważności",
        "Data zużycia/\n"
        "utylizacji",
        "Laboratorium",
        "Pracownia/pokój",
        "Lokalizacja\n"
        "szczegółowa",
        "Wymagana\n"
        "karta\n"
        "rozchodu",
        "Wygenerowana\n"
        "karta\n"
        "rozchodu",
        "Uwagi użytkownika",
    ]]
    for idx, personal_reagent in enumerate(personal_reagents_queryset, 1):
        reagent = personal_reagent.reagent
        clp_classifications = {}
        for hazard_statement in reagent.hazard_statements.all():
            clp_classifications[str(hazard_statement.clp_classification)] = None
        clp_classifications = ", ".join(clp_classifications.keys())
        is_usage_record_generated = "Nie dotyczy"
        if reagent.is_usage_record_required:
            is_usage_record_generated = "Tak" if personal_reagent.is_usage_record_generated else "Nie"

        report_data.append([
            idx,
            reagent.name,
            reagent.producer.abbreviation,
            reagent.catalog_no,
            personal_reagent.lot_no,
            personal_reagent.main_owner,
            personal_reagent.project_procedure,
            "Tak" if personal_reagent.is_critical else "Nie",
            clp_classifications,
            personal_reagent.receipt_purchase_date,
            personal_reagent.expiration_date,
            personal_reagent.disposal_utilization_date,
            personal_reagent.laboratory,
            personal_reagent.room,
            personal_reagent.detailed_location,
            "Tak" if reagent.is_usage_record_required else "Nie",
            is_usage_record_generated,
            personal_reagent.user_comment,
        ])

    return report_data


def generate_personal_view_report_data(personal_reagents_queryset):
    report_data = [[
        "Lp.",
        "Nazwa\n"
        "odczynnika",
        "Producent\n"
        "(marka)",
        "Stężenie",
        "Czystość",
        "Nr katologowy",
        "LOT",
        "Projekt/\n"
        "procedura",
        "Odczynnik\n"
        "kluczowy",
        "Kody H",
        "Kody P",
        "Klasyfikacja\n"
        "CLP",
        "Ostrzeżenie",
        "Data przyjęcia/\n"
        "zakupu",
        "Data ważności",
        "Data zużycia/\n"
        "utylizacji",
        "Laboratorium",
        "Pracownia/\n"
        "pokój",
        "Lokalizacja\n"
        "szczegółowa",
        "Wymagana\n"
        "karta\n"
        "rozchodu",
        "Wygenerowana\n"
        "karta\n"
        "rozchodu",
        "Uwagi\n"
        "użytkownika",
    ]]
    for idx, personal_reagent in enumerate(personal_reagents_queryset, 1):
        reagent = personal_reagent.reagent
        hazard_statements = reagent.hazard_statements.all()
        h_codes = ",\n".join(map(lambda x: x.code, hazard_statements))
        p_codes = ",\n".join(map(lambda x: x.code, reagent.precautionary_statements.all()))
        clp_classifications = {}
        for hazard_statement in hazard_statements:
            clp_classifications[str(hazard_statement.clp_classification)] = None
        clp_classifications = ", ".join(clp_classifications.keys())

        signal_word = ""
        signal_words = map(lambda x: x.signal_word, hazard_statements)
        for sw in signal_words:
            if sw == HazardStatement.DANGER:
                signal_word = sw
                break
            if sw == HazardStatement.WARNING:
                signal_word = sw

        is_usage_record_generated = "Nie dotyczy"
        if reagent.is_usage_record_required:
            is_usage_record_generated = "Tak" if personal_reagent.is_usage_record_generated else "Nie"

        report_data.append([
            idx,
            reagent.name,
            reagent.producer.abbreviation,
            reagent.concentration,
            reagent.purity_quality,
            reagent.catalog_no,
            personal_reagent.lot_no,
            personal_reagent.project_procedure,
            "Tak" if personal_reagent.is_critical else "Nie",
            h_codes,
            p_codes,
            clp_classifications,
            signal_word,
            personal_reagent.receipt_purchase_date,
            personal_reagent.expiration_date,
            personal_reagent.disposal_utilization_date,
            personal_reagent.laboratory,
            personal_reagent.room,
            personal_reagent.detailed_location,
            "Tak" if reagent.is_usage_record_required else "Nie",
            is_usage_record_generated,
            personal_reagent.user_comment,
        ])

    return report_data


def generate_report(report_header, requester, report_data, data_font_size):
    io_buffer = io.BytesIO()
    pdf_doc = SimpleDocTemplate(
        io_buffer,
        pagesize=(A4[1], A4[0]),
        title=report_header,
        author=str(requester),
        subject="Pliki dot. odczynników",
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )

    title_style = STYLES["Title"]
    title_style.fontName = REGULAR_FONT
    title_style.fontSize = 15
    title = Paragraph(report_header, title_style)

    report_data_table = Table(report_data, repeatRows=1)

    report_data_table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("0xF2F2F2")),  # "Gray" background for the first row
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add a border to all cells
        ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),  # Bold text in the first row
        ("FONTNAME", (0, 1), (-1, -1), REGULAR_FONT),  # Standard font in the rest
        ("FONTSIZE", (0, 0), (-1, -1), data_font_size),  # Font size indicated by `data_font_size`
    ])
    report_data_table.setStyle(report_data_table_style)

    pdf_doc.build([title, report_data_table], canvasmaker=ReportCanvas)

    return io_buffer


# STATISTICS

def generate_lab_worker_statistics(user_personal_reagents, user):
    worker_personal_reagents = user_personal_reagents.values(
        reagent_name=F("reagent__name"), catalog_no=F("reagent__catalog_no")
    ).annotate(count=Count("reagent__catalog_no")).order_by("-count")

    aggregated_worker_personal_reagents = [{
        "agg_fields": {
            "username": user.username,
        },
        "data": [
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            } for personal_reagent in worker_personal_reagents
        ]
    }] if worker_personal_reagents else []

    worker_disposed_utilized_personal_reagents = user_personal_reagents.filter(
            disposal_utilization_date__isnull=False
        ).annotate(year=ExtractYear("disposal_utilization_date")).values(
            "year"
        ).annotate(count=Count("reagent__catalog_no")).values(
            "year", "count", reagent_name=F("reagent__name"), catalog_no=F("reagent__catalog_no")
        ).order_by("-count")

    nested_aggregated_worker_disposed_utilized_personal_reagents = defaultdict(list)
    for personal_reagent in worker_disposed_utilized_personal_reagents:
        nested_aggregated_worker_disposed_utilized_personal_reagents[personal_reagent["year"]].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_worker_disposed_utilized_personal_reagents = []
    for year in nested_aggregated_worker_disposed_utilized_personal_reagents:
        aggregated_worker_disposed_utilized_personal_reagents.append({
            "agg_fields": {
                "year": year,
            },
            "data": nested_aggregated_worker_disposed_utilized_personal_reagents[year],
        })

    return {
        "worker_personal_reagents": aggregated_worker_personal_reagents,
        "worker_disposed_utilized_personal_reagents": aggregated_worker_disposed_utilized_personal_reagents,
    }


def generate_project_manager_statistics():
    project_procedure_personal_reagents = PersonalReagent.objects.filter(
        project_procedure__isnull=False
    ).values(
        project_procedure_name=F("project_procedure__name"),
        reagent_name=F("reagent__name"),
        catalog_no=F("reagent__catalog_no"),
    ).annotate(count=Count("project_procedure")).order_by("-count")

    nested_aggregated_project_procedure_personal_reagents = defaultdict(list)
    for personal_reagent in project_procedure_personal_reagents:
        nested_aggregated_project_procedure_personal_reagents[personal_reagent["project_procedure_name"]].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_project_procedure_personal_reagents = []
    for project_procedure_name in nested_aggregated_project_procedure_personal_reagents:
        aggregated_project_procedure_personal_reagents.append({
            "agg_fields": {
                "project_procedure_name": project_procedure_name,
            },
            "data": nested_aggregated_project_procedure_personal_reagents[project_procedure_name],
        })

    project_procedure_disposed_utilized_personal_reagents = PersonalReagent.objects.filter(
            disposal_utilization_date__isnull=False, project_procedure__isnull=False
        ).annotate(year=ExtractYear("disposal_utilization_date")).values(
            "year"
        ).annotate(count=Count("reagent__catalog_no")).values(
            "year",
            "count",
            project_procedure_name=F("project_procedure__name"),
            reagent_name=F("reagent__name"),
            catalog_no=F("reagent__catalog_no"),
        ).order_by("-count")

    nested_aggregated_project_procedure_disposed_utilized_personal_reagents = defaultdict(lambda: defaultdict(list))
    for personal_reagent in project_procedure_disposed_utilized_personal_reagents:
        nested_aggregated_project_procedure_disposed_utilized_personal_reagents[
            personal_reagent["project_procedure_name"]
        ][
            personal_reagent["year"]
        ].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_project_procedure_disposed_utilized_personal_reagents = []
    for project_procedure_name in nested_aggregated_project_procedure_disposed_utilized_personal_reagents:
        for year in nested_aggregated_project_procedure_disposed_utilized_personal_reagents[project_procedure_name]:
            aggregated_project_procedure_disposed_utilized_personal_reagents.append({
                "agg_fields": {
                    "project_procedure_name": project_procedure_name,
                    "year": year,
                },
                "data":\
                    nested_aggregated_project_procedure_disposed_utilized_personal_reagents[
                        project_procedure_name
                    ][
                        year
                    ],
            })

    return {
        "project_procedure_personal_reagents": aggregated_project_procedure_personal_reagents,
        "project_procedure_disposed_utilized_personal_reagents":\
            aggregated_project_procedure_disposed_utilized_personal_reagents,
    }


def generate_lab_manager_statistics():
    laboratory_personal_reagents = PersonalReagent.objects.values(
        "laboratory", reagent_name=F("reagent__name"), catalog_no=F("reagent__catalog_no")
    ).annotate(count=Count("laboratory")).order_by("-count")

    nested_aggregated_laboratory_personal_reagents = defaultdict(list)
    for personal_reagent in laboratory_personal_reagents:
        nested_aggregated_laboratory_personal_reagents[personal_reagent["laboratory"]].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_laboratory_personal_reagents = []
    for laboratory in nested_aggregated_laboratory_personal_reagents:
        aggregated_laboratory_personal_reagents.append({
            "agg_fields": {
                "laboratory": laboratory,
            },
            "data": nested_aggregated_laboratory_personal_reagents[laboratory],
        })

    laboratory_disposed_utilized_personal_reagents = PersonalReagent.objects.filter(
            disposal_utilization_date__isnull=False
        ).annotate(year=ExtractYear("disposal_utilization_date")).values(
            "year"
        ).annotate(count=Count("reagent__catalog_no")).values(
            "year",
            "count",
            "laboratory",
            reagent_name=F("reagent__name"),
            catalog_no=F("reagent__catalog_no"),
        ).order_by("-count")

    nested_aggregated_laboratory_disposed_utilized_personal_reagents = defaultdict(lambda: defaultdict(list))
    for personal_reagent in laboratory_disposed_utilized_personal_reagents:
        nested_aggregated_laboratory_disposed_utilized_personal_reagents[
            personal_reagent["laboratory"]
        ][
            personal_reagent["year"]
        ].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_laboratory_disposed_utilized_personal_reagents = []
    for laboratory in nested_aggregated_laboratory_disposed_utilized_personal_reagents:
        for year in nested_aggregated_laboratory_disposed_utilized_personal_reagents[laboratory]:
            aggregated_laboratory_disposed_utilized_personal_reagents.append({
                "agg_fields": {
                    "laboratory": laboratory,
                    "year": year,
                },
                "data":\
                    nested_aggregated_laboratory_disposed_utilized_personal_reagents[laboratory][year],
            })

    # We can reuse `nested_aggregated_laboratory_personal_reagents`
    aggregated_top10_laboratory_personal_reagents = []
    aggregated_top20_laboratory_personal_reagents = []
    for laboratory in nested_aggregated_laboratory_personal_reagents:
        aggregated_top10_laboratory_personal_reagents.append({
            "agg_fields": {
                "laboratory": laboratory,
            },
            "data": nested_aggregated_laboratory_personal_reagents[laboratory][:10],
        })
        aggregated_top20_laboratory_personal_reagents.append({
            "agg_fields": {
                "laboratory": laboratory,
            },
            "data": nested_aggregated_laboratory_personal_reagents[laboratory][:20],
        })

    return {
        "laboratory_personal_reagents": aggregated_laboratory_personal_reagents,
        "laboratory_disposed_utilized_personal_reagents": aggregated_laboratory_disposed_utilized_personal_reagents,
        "top10_laboratory_personal_reagents": aggregated_top10_laboratory_personal_reagents,
        "top20_laboratory_personal_reagents": aggregated_top20_laboratory_personal_reagents,
    }


def generate_admin_statistics():
    global_personal_reagents = PersonalReagent.objects.values(
        username=F("main_owner__username"), reagent_name=F("reagent__name"), catalog_no=F("reagent__catalog_no")
    ).annotate(count=Count("reagent__catalog_no")).order_by("-count")

    nested_aggregated_global_personal_reagents = defaultdict(list)
    for personal_reagent in global_personal_reagents:
        nested_aggregated_global_personal_reagents[personal_reagent["username"]].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_global_personal_reagents = []
    for username in nested_aggregated_global_personal_reagents:
        aggregated_global_personal_reagents.append({
            "agg_fields": {
                "username": username,
            },
            "data": nested_aggregated_global_personal_reagents[username],
        })

    global_disposed_utilized_personal_reagents = PersonalReagent.objects.filter(
            disposal_utilization_date__isnull=False
        ).annotate(year=ExtractYear("disposal_utilization_date")).values(
            "year"
        ).annotate(count=Count("reagent__catalog_no")).values(
            "year",
            "count",
            username=F("main_owner__username"),
            reagent_name=F("reagent__name"),
            catalog_no=F("reagent__catalog_no"),
        ).order_by("-count")

    nested_aggregated_global_disposed_utilized_personal_reagents = defaultdict(lambda: defaultdict(list))
    for personal_reagent in global_disposed_utilized_personal_reagents:
        nested_aggregated_global_disposed_utilized_personal_reagents[
            personal_reagent["username"]
        ][
            personal_reagent["year"]
        ].append(
            {
                "reagent_name": personal_reagent["reagent_name"],
                "catalog_no": personal_reagent["catalog_no"],
                "count": personal_reagent["count"],
            }
        )

    aggregated_global_disposed_utilized_personal_reagents = []
    for username in nested_aggregated_global_disposed_utilized_personal_reagents:
        for year in nested_aggregated_global_disposed_utilized_personal_reagents[username]:
            aggregated_global_disposed_utilized_personal_reagents.append({
                "agg_fields": {
                    "username": username,
                    "year": year,
                },
                "data":\
                    nested_aggregated_global_disposed_utilized_personal_reagents[username][year],
            })

    return {
        "global_personal_reagents": aggregated_global_personal_reagents,
        "global_disposed_utilized_personal_reagents": aggregated_global_disposed_utilized_personal_reagents,
    }
