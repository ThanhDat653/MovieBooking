from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShowTime, Seat

@receiver(post_save, sender=ShowTime)
def create_seats_for_showtime(sender, instance, created, **kwargs):
    if created:
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        seats_per_row = 10
        for row in rows:
            for num in range(1, seats_per_row + 1):
                seat_number = f"{row}{num}"
                Seat.objects.create(showtime=instance, seat_number=seat_number)