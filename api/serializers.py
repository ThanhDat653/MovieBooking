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
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    cinema = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all())
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    cinema_name = serializers.CharField(source='cinema.name', read_only=True)

    class Meta:
        model = ShowTime
        fields = ['id', 'start_time', 'movie', 'cinema', 'movie_title', 'cinema_name']

class SeatSerializer(serializers.ModelSerializer):
    showtime = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = Seat
        fields = ['id', 'price', 'seat_number', 'is_booked', 'showtime']

    def get_showtime(self, obj):
        return f"{obj.showtime.start_time} | {obj.showtime.movie.title} | {obj.showtime.cinema.name}"

class BookingSerializer(serializers.ModelSerializer):
    seat = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.none(),
        help_text="Danh sách ghế sẽ hiển thị theo tham số ?showtime trên URL."
    )

    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nếu context có showtime_id, thì lọc ghế theo showtime và is_booked = False
        request = self.context.get('request')
        if request:
            showtime_id = request.query_params.get('showtime')
            if showtime_id:
                self.fields['seat'].queryset = Seat.objects.filter(
                    showtime_id=showtime_id,
                    is_booked=False
                )
            else:
                self.fields['seat'].queryset = Seat.objects.none()
