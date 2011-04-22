from django.contrib import admin
from competition.models import *

class CompetitionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Competition, CompetitionAdmin)

class JudgeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Judge, JudgeAdmin)

class OrganizerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Organizer, OrganizerAdmin)

class TeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(Team, TeamAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    pass
admin.site.register(Participant, ParticipantAdmin)

class ProblemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Problem, ProblemAdmin)

class SolutionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Solution, SolutionAdmin)


