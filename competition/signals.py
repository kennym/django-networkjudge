from django.dispatch import receiver, Signal
import logging

update_score = Signal(providing_args=["participant"])

@receiver(update_score)
def submission_saved(sender, **kwargs):
    logging.info("Submission modified")
    participant = kwargs['participant']
    participant.calculate_score()
