from rest_framework import viewsets, generics
from .models import Movie, Cinema, ShowTime, Seat, Booking
from .serializers import MovieSerializer, CinemaSerializer, ShowTimeSerializer, SeatSerializer, BookingSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

class ShowTimeViewSet(viewsets.ModelViewSet):
    queryset = ShowTime.objects.all()
    serializer_class = ShowTimeSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    
class SeatByShowtimeView(APIView):
    def get(self, request, showtime_id):
        seats = Seat.objects.filter(showtime_id=showtime_id)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "Vui lòng điền đầy đủ thông tin!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Tên đăng nhập đã tồn tại!"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "Đăng ký thành công!"}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Đăng nhập bằng session
            return Response({"message": "Đăng nhập thành công!"})
        return Response({"error": "Sai thông tin đăng nhập!"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Đăng xuất thành công!"})

class UpcomingMovieListAPIView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return Movie.objects.filter(release_date__gt=today)

class NowShowingMovieListAPIView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return Movie.objects.filter(
            release_date__lt=today
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=today)
        )
