from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# from django.contrib.auth.models import UserProfile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import DiseaseDetection, CropRecommendation, MarketPrice


def index(request):
    return render(request, 'farming/index.html')

def dashboard(request):
    """Dashboard page for authenticated users with all features"""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'farming/dashboard.html')
@login_required(login_url='login')

@login_required(login_url='login')
def crop_recommend(request):
    from farming.ml.crop_predict import predict_crops
    from farming.ml.soil_mapper import map_soil_inputs
    from farming.models import CropRecommendation

    result = None

    if request.method == "POST":
        fertility = request.POST['fertility']
        soil_type = request.POST['soil_type']
        climate = request.POST['climate']
        rainfall = request.POST['rainfall']  # "low / medium / heavy"

        # ✅ Unpack mapped values
        N, P, K, temperature, humidity, ph, rainfall_mm = map_soil_inputs(
            fertility, soil_type, climate, rainfall
        )

        data = [N, P, K, temperature, humidity, ph, rainfall_mm]

        # 🔥 Predict multiple crops
        results = predict_crops(data, top_k=3)

        # 🔥 Save each crop
        for r in results:
            CropRecommendation.objects.create(
                user=request.user,
                recommended_crop=r["crop"],
                fertility=fertility,
                soil_type=soil_type,
                climate=climate,
                rainfall_level=rainfall,   # "medium"
                rainfall=rainfall_mm,      # 120
                temperature=temperature,
                humidity=humidity,
                ph=ph,
            )

        result = results

    return render(request, 'farming/crop.html', {'result': result})


@login_required(login_url='login')
def disease_detection(request):
    from farming.disease.predictor import predict_disease
    result = None

    if request.method == "POST":
        image = request.FILES.get("image")

        if not image:
            messages.error(request, "Please upload a plant leaf image.")
            return redirect("disease")

        # Save image temporarily
        fs = FileSystemStorage()
        disease_images = fs.save(image.name, image)
        image_path = fs.path(disease_images)

        # ML Prediction
        disease, confidence = predict_disease(image_path)

        disease = disease.replace("___", " - ")
        confidence = round(confidence, 2)

        # Save to database
        DiseaseDetection.objects.create(
            user=request.user,
            image=image,
            disease_name=disease,
            confidence=confidence
        )

        result = {
            "disease": disease,
            "confidence": confidence
        }

    return render(request, "farming/disease.html", {"result": result})

def market_prediction(request):
    from farming.ml.market_predict import predict_prices, get_market_insights, get_all_crops, compare_crops
    result = None
    crops = get_all_crops()
    comparison = None
    
    if request.method == "POST":
        crop = request.POST.get('crop', '')
        action = request.POST.get('action', 'predict')
        
        if action == 'predict' and crop:
            result = predict_prices(crop, days_ahead=30)
            result['insights'] = get_market_insights(crop)
            
            # Zip dates and prices together for easier template iteration
            result['forecast'] = list(zip(result['dates'], result['prices']))
        
        elif action == 'compare':
            selected_crops = request.POST.getlist('compare_crops')
            comparison = compare_crops(selected_crops)
    
    return render(request, 'farming/market.html', {
        'result': result,
        'crops': crops,
        'comparison': comparison
    })

    MarketPrice.objects.create(
        user=request.user,
        crop_name=crop,
        estimated_price=result
    )

@login_required

@login_required
def combined_history(request):
    disease_history = DiseaseDetection.objects.filter(user=request.user)
    crop_history = CropRecommendation.objects.filter(user=request.user)
    market_history = MarketPrice.objects.filter(user=request.user)

    return render(
        request,
        'farming/combined_history.html',
        {
            'disease_history': disease_history,
            'crop_history': crop_history,
            'market_history': market_history,
        }
    )

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                'Account created successfully! Welcome to Smart Farm AI.'
            )
            return redirect('dashboard')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SignUpForm()

    return render(request, 'farming/signup.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Try to authenticate with username or email
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                # Try to find user by email
                from django.contrib.auth.models import User
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires on browser close
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'farming/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

def blog_and_news(request):
    """Blog, news, facts, and market trends page"""
    return render(request, 'farming/blog.html')

