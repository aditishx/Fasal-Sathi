from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# User profile to store additional data for each user
class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	phone = models.CharField(max_length=20, blank=True)
	farm_name = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=100, blank=True)
	state = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		try:
			return f"{self.user.username} Profile"
		except Exception:
			return "UserProfile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	"""Create a UserProfile whenever a new user is created."""
	if created:
		UserProfile.objects.create(user=instance)

# 1️⃣ Disease Detection
class DiseaseDetection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='disease_images/')
    disease_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease_name}"


# 2️⃣ Crop Recommendation
class CropRecommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    recommended_crop = models.CharField(max_length=100, default="Rice")

    fertility = models.CharField(max_length=100, default="medium")
    soil_type = models.CharField(max_length=100, default="loamy")
    climate = models.CharField(max_length=100, default="moderate")
    rainfall_level = models.CharField(max_length=20, default="medium")  # "low / medium / heavy"
    rainfall = models.IntegerField(default=0)                   # 50 / 120 / 200

    temperature = models.FloatField(default=25)
    humidity = models.FloatField(default=70)
    ph = models.FloatField(default=7.0)

    recommended_crops = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recommended_crop



# 3️⃣ Market Price Estimation
class MarketPrice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    estimated_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

