from rest_framework import serializers
from .models import Movie, Cinema, ShowTime, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'

class ShowTimeSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='movie.title', read_only=True)
    cinema = serializers.CharField(source='cinema.name', read_only=True)
    class Meta:
        model = ShowTime
        fields = ['id', 'start_time', 'movie', 'cinema']

class SeatSerializer(serializers.ModelSerializer):
    showtime = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'price', 'seat_number', 'is_booked', 'showtime']

    def get_showtime(self, obj):
        return f"{obj.showtime.start_time} | {obj.showtime.movie.title} | {obj.showtime.cinema.name}"

class BookingSerializer(serializers.ModelSerializer):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Nếu context có showtime_id, thì lọc ghế theo showtime và isBooking = False
        request = self.context.get('request')
        if request:
            showtime_id = request.query_params.get('showtime')
            if showtime_id:
                self.fields['seat'].queryset = Seat.objects.filter(
                    showtime_id=showtime_id,
                    isBooking=False
                )
            else:
                self.fields['seat'].queryset = Seat.objects.none()
