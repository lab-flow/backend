from rest_framework.permissions import BasePermission

from .models import User


def has_lab_role(user):
    return not set(user.lab_roles).isdisjoint(User.LAB_ROLES_VALUES)


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True

        if view.action in ("list", "retrieve", "get_current_user_info"):
            return user.is_authenticated and has_lab_role(user)

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or view.action in ("list", "retrieve"):
            return True

        if view.action == "get_current_user_info":
            return user == obj

        return False


class HazardPermission(BasePermission):
    """Common class for Classification, Pictogram, ClpClassification, HazardStatement and PrecautionaryStatement"""
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff or view.action in ("list", "retrieve", "get_ghs_pictograms"):
            return True

        return False


class ReagentFieldPermission(BasePermission):
    "Common class for Producer, ReagentType, Concentration, Unit, PurityQuality and StorageCondition."
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True

        if view.action in ("list", "create", "retrieve"):
            return user.is_authenticated and has_lab_role(user)

        return False


class ReagentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("get_safety_instructions", "get_safety_instruction"):
            return True

        user = request.user
        if user.is_staff:
            return True

        if view.action in ("list", "create", "retrieve"):
            return user.is_authenticated and has_lab_role(user)

        return False


class ProjectProcedurePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user.is_authenticated:
            if user.is_staff or (view.action != "get_historical_records" and User.LAB_MANAGER in user.lab_roles):
                return True

            if view.action == "create":
                return User.PROJECT_MANAGER in user.lab_roles

            if view.action in ("list", "retrieve"):
                return has_lab_role(user)

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if (user.is_staff
                or (user.is_authenticated and User.LAB_MANAGER in user.lab_roles)
                or view.action in ("list", "retrieve", "update", "partial_update")):
            return True

        return False


class PersonalReagentPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True

        if user.is_authenticated:
            if view.action in (
                "list",
                "create",
                "retrieve",
                "update",
                "partial_update",
                "destroy",
                "get_personal_view",
                "generate_usage_record",
                "generate_all_personal_reagents_report",
                "generate_personal_view_report",
                "generate_statistics",
            ):
                return has_lab_role(user)

            if view.action in ("generate_sanepid_pip_report", "generate_lab_manager_report"):
                return User.LAB_MANAGER in user.lab_roles

            if view.action == "generate_projects_procedures_report":
                return User.LAB_MANAGER in user.lab_roles or User.PROJECT_MANAGER in user.lab_roles

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or view.action in (
            "list",
            "retrieve",
            "get_personal_view",
            "generate_sanepid_pip_report",
            "generate_lab_manager_report",
            "generate_projects_procedures_report",
            "generate_all_personal_reagents_report",
            "generate_personal_view_report",
            "generate_statistics",
        ):
            return True

        if view.action in ("update", "generate_usage_record"):
            return (user == obj.main_owner
                        or (obj.project_procedure is not None and user == obj.project_procedure.manager))

        if view.action == "partial_update":
            return (user == obj.main_owner
                        or User.LAB_MANAGER in user.lab_roles
                        or (obj.project_procedure is not None and user == obj.project_procedure.manager))

        if view.action == "destroy":
            return user == obj.main_owner

        return False


class NotificationPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True

        if view.action in (
            "get_reagents_with_close_expiration_date",
            "get_reagents_with_not_generated_usage_records",
            "get_few_critical_reagents",
            "get_reagent_requests",
        ):
            return user.is_authenticated and has_lab_role(user)

        return False


class ReagentRequestPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True

        if view.action in (
            "create",
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "get_current_user_reagent_requests",
            "change_reagent_request_status",
        ):
            return user.is_authenticated and has_lab_role(user)

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True

        if view.action in ("retrieve", "update", "partial_update", "destroy", "get_current_user_reagent_requests"):
            return user == obj.requester

        if view.action == "change_reagent_request_status":
            return user == obj.personal_reagent.main_owner

        return False


class UserManualPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff or request.method == "GET":
            return True

        return False
