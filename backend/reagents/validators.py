from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class PolishAlphabetUsernameValidator(validators.RegexValidator):
    regex = r"^[A-ZĄĆĘŁŃÓŚŹŻ]{2,4}$"
    message = "Wprowadź prawidłową nazwę. Może zawierać wyłącznie od 2 do 4 wielkich liter z polskiego alfabetu."\
              "Przykłady: GK, AMA, WW."
    flags = 0


@deconstructible
class ClpClassificationValidator(validators.RegexValidator):
    regex = r"^$|^GHS(0[0-9]|[0-9]{2})$"
    message = "Wprowadź prawidłową nazwę. Może być pusta lub musi zaczynać się od GHS, "\
              "a następnie posiadać dwie cyfry. Przykłady: GHS01, GHS09."
    flags = 0


@deconstructible
class HazardStatementCodeValidator(validators.RegexValidator):
    regex = r"^$|"\
            r"^(H[0-9]{3}[A-Za-z]{,2})+( \+ H[0-9]{3}[A-Za-z]{,2})*$|"\
            r"^(EUH[0-9]{3}[A-Za-z]{,2})+( \+ EUH[0-9]{3}[A-Za-z]{,2})*$"
    message = "Kod H musi zaczynać się od H lub EUH, a następnie posiadać 3 cyfry i opcjonalnie maks. 2 litery. "\
              "Może też występować połączenie kodów za pomocą znaku + otoczonego spacjami. "\
              "Przykłady: H200, H360FD, EUH209A, H301 + H331."
    flags = 0


@deconstructible
class PrecautionaryStatementCodeValidator(validators.RegexValidator):
    regex = r"^$|^(P[0-9]{3})+( \+ P[0-9]{3})*$"
    message = "Kod P musi zaczynać się od P, a następnie posiadać 3 cyfry. "\
              "Może też występować połączenie kodów za pomocą znaku + otoczonego spacjami. "\
              "Przykłady: P200, P231 + P232."
    flags = 0


@deconstructible
class SafetyInstructionNameValidator(validators.RegexValidator):
    regex = r"^$|^IB(000[0-9]|00[0-9]{2}|0[0-9]{3}|[0-9]{4})(.[0-9])?$"
    message = "Nr instrukcji bezpieczeństwa musi zaczynać się od IB, a następnie posiadać liczbę wypełnioną "\
              "od lewej zerami. Dodatkowo może kończyć się na kropce i cyfrze dla oznaczenia wersji. "\
              "Przykłady: IB0001, IB1234, IB5678.2"
    flags = 0


@deconstructible
class SafetyDataSheetNameValidator(validators.RegexValidator):
    regex = r"^$|^SDS(000[0-9]|00[0-9]{2}|0[0-9]{3}|[0-9]{4})(.[0-9])?$"
    message = "MSDS/SDS producenta musi zaczynać się od SDS, a następnie posiadać liczbę wypełnioną "\
              "od lewej zerami. Dodatkowo może kończyć się na kropce i cyfrze dla oznaczenia wersji. "\
              "Przykłady: SDS0001, SDS1234, SDS5678.3"
    flags = 0
