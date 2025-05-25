from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# 🎬 Model Phim
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Ngày ngừng chiếu")
    duration = models.IntegerField(help_text="Duration in minutes")
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True, help_text="Thể loại phim")
    director = models.CharField(max_length=100, blank=True, help_text="Đạo diễn")
    actors = models.TextField(blank=True, help_text="Diễn viên (cách nhau bởi dấu phẩy)")
    trailer = models.URLField(blank=True, help_text="Đường dẫn video trailer")

    def __str__(self):
        return self.title

# 🎭 Model Rạp
class Cinema(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
    
class Room(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, null=True, default=1)

    def __str__(self):
        return f"{self.cinema.name} - Room {self.room_number}"

# 🎟️ Model Suất Chiếu
class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.start_time} at {self.cinema.name}"

# 💺 Model Ghế Ngồi# 💺 Model Ghế ngồi
class Seat(models.Model):
    showtime = models.ForeignKey('ShowTime', on_delete=models.CASCADE, related_name='seats')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal("79000.00"))
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

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

