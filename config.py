"""
Trafik Ajan Simülasyonu için Konfigürasyon Dosyası
"""
import os

# Ekran ayarları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (200, 200, 200)
FPS = 30

# Assets ayarları
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), "assets")
USE_VEHICLE_IMAGES = True
USE_BUILDING_IMAGES = True

# Kavşak ayarları
INTERSECTION_SIZE = 80
ROAD_WIDTH = 40
LANE_WIDTH = 20

# Ana yol ayarları
MAIN_ROAD_DIRECTION = 'East'  # Ana yol doğu yönünde
MAIN_ROAD_LENGTH_MULTIPLIER = 1.5  # Ana yol diğer yollardan 1.5 kat uzun
MAIN_ROAD_EXTENSION = 200  # Ana yol için ek uzunluk (piksel)

# Araç ayarları
VEHICLE_WIDTH = 10
VEHICLE_LENGTH = 20
VEHICLE_COLORS = {
    'North': (255, 0, 0),    # Kırmızı
    'South': (0, 0, 255),    # Mavi
    'East': (0, 255, 0),     # Yeşil
    'West': (255, 255, 0)    # Sarı
}

# Bina ayarları
BUILDING_SIZE = 40
BUILDING_POSITIONS = [
    {"x": 50, "y": 50},    # Sol üst
    {"x": 700, "y": 50},   # Sağ üst
    {"x": 50, "y": 500},   # Sol alt
    {"x": 700, "y": 500},  # Sağ alt
]

# Trafik kontrolü ayarları
CONTROL_STRATEGIES = ['equal_priority', 'main_road_priority', 'main_road_priority_enhanced', 'adaptive_timing']
DEFAULT_STRATEGY = 'main_road_priority'

# Araç oluşturma ayarları (Daha gerçekçi trafik yoğunluğu için)
VEHICLE_GENERATION_RATE = {
    'North': 0.12,   # Daha yoğun trafik için artırıldı
    'South': 0.12,   # Daha yoğun trafik için artırıldı
    'East': 0.15,    # Ana yol daha yoğun
    'West': 0.12     # Daha yoğun trafik için artırıldı
}

MAX_VEHICLES = {
    'North': 18,     # Daha yoğun trafik için artırıldı
    'South': 18,     # Daha yoğun trafik için artırıldı
    'East': 25,      # Ana yol için daha fazla araç
    'West': 18       # Daha yoğun trafik için artırıldı
}

# Hız ayarları (piksel/frame) - Daha gerçekçi trafik için yavaşlatıldı
SPEED_RANGE = {
    'min': 1,    # Minimum hız azaltıldı
    'max': 3,    # Maksimum hız azaltıldı  
    'default': 2 # Ortalama hız azaltıldı
}

# Simülasyon ayarları
SIMULATION_DURATION = 9000  # LaTeX için uzun ve güvenilir simülasyon
REPORT_INTERVAL = 100      # Uzun simülasyon için daha az sık rapor

# Dosya kayıt ayarları
SAVE_SIMULATION = True
SAVE_PATH = "./simulation_results/"

# Ana yol trafiği için özel ayarlar - Sıkışıklığı azaltmak için optimize edildi
MAIN_ROAD_SETTINGS = {
    'priority_factor': 1.8,      # Ana yol öncelik faktörü azaltıldı
    'traffic_density': 0.15,     # Ana yolda trafik yoğunluğu azaltıldı
    'congestion_threshold': 10,  # Sıkışıklık eşiği azaltıldı (araç sayısı)
    'avg_speed_reduction': 0.8   # Sıkışıklık durumunda daha az hız azalması
}