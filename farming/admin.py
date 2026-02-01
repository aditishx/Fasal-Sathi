from django.contrib import admin
from .models import UserProfile
from .models import DiseaseDetection, CropRecommendation, MarketPrice


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "farm_name", "phone","city","state", "country", "created_at")
	search_fields = ("user__username", "farm_name", "phone")

@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
	list_display = ("user", "image", "disease_name", "confidence", "created_at")
	search_fields = ("user__username", "disease_name")

@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
	list_display = ("user", "recommended_crop", "fertility", "soil_type", "climate", "rainfall", "created_at")
	search_fields = ("user__username", "recommended_crop")

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
	list_display = ("user", "crop_name", "estimated_price", "created_at")
	search_fields = ("user__username", "crop_name")
