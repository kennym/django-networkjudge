from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

update_score = Signal(providing_args=["participant"])

@receiver(update_score)
def submission_saved(sender, **kwargs):
    participant = kwargs['participant']
    print "Updating score..."
    participant.calculate_score()
