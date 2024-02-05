from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reagents import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Producer)
admin.site.register(models.Pictogram)
admin.site.register(models.ClpClassification)
admin.site.register(models.HazardStatement)
admin.site.register(models.PrecautionaryStatement)
admin.site.register(models.ReagentType)
admin.site.register(models.Concentration)
admin.site.register(models.Unit)
admin.site.register(models.PurityQuality)
admin.site.register(models.StorageCondition)
admin.site.register(models.Reagent)
admin.site.register(models.ProjectProcedure)
admin.site.register(models.PersonalReagent)
admin.site.register(models.ReagentRequest)
