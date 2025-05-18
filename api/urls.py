from .views import RegisterAPIView, LoginAPIView, LogoutAPIView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, CinemaViewSet, ShowTimeViewSet, SeatViewSet, BookingViewSet, SeatByShowtimeView

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'cinemas', CinemaViewSet)
router.register(r'showtimes', ShowTimeViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Tự động tạo các endpoint API
    path('seats/showtime/<int:showtime_id>/', SeatByShowtimeView.as_view()),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]

