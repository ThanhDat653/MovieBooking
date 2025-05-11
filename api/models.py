from django.db import models
from django.contrib.auth.models import User

# 🎬 Model Phim
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.title

# 🎭 Model Rạp
class Cinema(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=500)

    def __str__(self):
        return self.name

# 🎟️ Model Suất Chiếu
class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.start_time} at {self.cinema.name}"

# 💺 Model Ghế Ngồi
class Seat(models.Model):
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)  # Ví dụ: A1, B5

    def __str__(self):
        return f"{self.seat_number} - {self.showtime}"

# 🔑 Model Đặt Vé
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.showtime} - {self.seat}"

