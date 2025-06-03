"""
Trafik Ajan Simülasyonu için Kavşak Sınıfı
"""
import pygame
import random
import time
from config import (
    INTERSECTION_SIZE, ROAD_WIDTH, LANE_WIDTH, VEHICLE_GENERATION_RATE, MAX_VEHICLES,
    MAIN_ROAD_DIRECTION, MAIN_ROAD_EXTENSION, MAIN_ROAD_SETTINGS
)

class Intersection:
    def __init__(self, screen_width, screen_height, control_strategy='equal_priority'):
        """
        Kavşak nesnesini oluşturur
        
        Args:
            screen_width (int): Ekran genişliği
            screen_height (int): Ekran yüksekliği
            control_strategy (str): Kullanılacak trafik kontrol stratejisi
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_strategy = control_strategy
        
        # Kavşak pozisyonu (ekranın ortası)
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        
        # Kavşak boyutu
        self.size = INTERSECTION_SIZE
        
        # Kavşak çarpışma dikdörtgeni
        self.rect = pygame.Rect(
            self.center_x - self.size // 2,
            self.center_y - self.size // 2,
            self.size,
            self.size
        )
        
        # Şu anda kavşağı kullanan araçlar
        self.current_vehicles_in_intersection = []
        
        # Trafik akışı istatistikleri
        self.stats = {
            'North': {'vehicles_passed': 0, 'total_wait_time': 0, 'avg_wait_time': 0, 
                     'congestion_level': 0, 'peak_congestion': 0, 'current_vehicles': 0},
            'South': {'vehicles_passed': 0, 'total_wait_time': 0, 'avg_wait_time': 0, 
                     'congestion_level': 0, 'peak_congestion': 0, 'current_vehicles': 0},
            'East': {'vehicles_passed': 0, 'total_wait_time': 0, 'avg_wait_time': 0, 
                    'congestion_level': 0, 'peak_congestion': 0, 'current_vehicles': 0},
            'West': {'vehicles_passed': 0, 'total_wait_time': 0, 'avg_wait_time': 0, 
                     'congestion_level': 0, 'peak_congestion': 0, 'current_vehicles': 0}
        }
        
        # Adaptif zamanlama için kullanılacak sayaçlar
        self.current_priority = None
        self.priority_timer = 0
        self.adaptive_counter = 0
        
        # Ana yol önceliği için
        self.main_road_direction = MAIN_ROAD_DIRECTION
        self.main_road_directions = [MAIN_ROAD_DIRECTION]  
        if MAIN_ROAD_DIRECTION in ['East', 'West']:
            self.main_road_directions = ['East', 'West']
        elif MAIN_ROAD_DIRECTION in ['North', 'South']:
            self.main_road_directions = ['North', 'South']
        
        # Ana yol özel ayarları
        self.main_road_settings = MAIN_ROAD_SETTINGS
        
        # Sıkışıklık takibi
        self.congestion_history = {
            'North': [],
            'South': [],
            'East': [],
            'West': []
        }
        self.frame_count = 0
    
    def draw(self, screen):
        """Kavşağı ekrana çizer"""
        # Ana yol rengini belirle (daha koyu ve geniş)
        main_road_color = (30, 30, 30)  # Ana yol için koyu gri
        normal_road_color = (50, 50, 50)  # Normal yollar için gri
        
        # Yolları çiz
        if self.main_road_direction in ['East', 'West']:
            # Ana yol yatay - daha geniş çiz
            main_road_width = int(ROAD_WIDTH * 1.2)
            pygame.draw.rect(screen, main_road_color, 
                           (0, self.center_y - main_road_width // 2, self.screen_width, main_road_width))
            
            # Ana yol uzantısını çiz (doğu tarafına)
            if self.main_road_direction == 'East':
                pygame.draw.rect(screen, main_road_color, 
                               (self.screen_width, self.center_y - main_road_width // 2, 
                                MAIN_ROAD_EXTENSION, main_road_width))
            
            # Dikey yol (normal)
            pygame.draw.rect(screen, normal_road_color, 
                           (self.center_x - ROAD_WIDTH // 2, 0, ROAD_WIDTH, self.screen_height))
            
            # Ana yol şerit çizgisi (daha belirgin)
            pygame.draw.line(screen, (255, 255, 100), 
                           (0, self.center_y), (self.screen_width + MAIN_ROAD_EXTENSION, self.center_y), 3)
            
            # Normal yol şerit çizgisi
            pygame.draw.line(screen, (255, 255, 255), 
                           (self.center_x, 0), (self.center_x, self.screen_height), 2)
        
        else:  # Ana yol dikey
            # Ana yol dikey - daha geniş çiz
            main_road_width = int(ROAD_WIDTH * 1.2)
            pygame.draw.rect(screen, main_road_color, 
                           (self.center_x - main_road_width // 2, 0, main_road_width, self.screen_height))
            
            # Ana yol uzantısını çiz (seçilen yöne göre)
            if self.main_road_direction == 'North':
                pygame.draw.rect(screen, main_road_color, 
                               (self.center_x - main_road_width // 2, -MAIN_ROAD_EXTENSION, 
                                main_road_width, MAIN_ROAD_EXTENSION))
            
            # Yatay yol (normal)
            pygame.draw.rect(screen, normal_road_color, 
                           (0, self.center_y - ROAD_WIDTH // 2, self.screen_width, ROAD_WIDTH))
            
            # Ana yol şerit çizgisi (daha belirgin)
            pygame.draw.line(screen, (255, 255, 100), 
                           (self.center_x, -MAIN_ROAD_EXTENSION), (self.center_x, self.screen_height), 3)
            
            # Normal yol şerit çizgisi
            pygame.draw.line(screen, (255, 255, 255), 
                           (0, self.center_y), (self.screen_width, self.center_y), 2)
        
        # Kavşak bölgesini saydam olarak işaretle
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((255, 255, 0, 60))  # Sarı, saydam
        screen.blit(s, (self.center_x - self.size // 2, self.center_y - self.size // 2))
        
        # Ana yol işaretini ekle
        if self.main_road_direction == 'East':
            # "ANA YOL" yazısı
            font = pygame.font.Font(None, 24)
            text = font.render("ANA YOL", True, (255, 255, 100))
            screen.blit(text, (self.screen_width - 150, self.center_y - 40))
    
    def control_traffic(self, vehicles):
        """
        Kavşaktaki trafik akışını kontrol eder
        
        Args:
            vehicles (list): Sistemdeki tüm araçların listesi
        
        Returns:
            list: Kavşağı geçmesine izin verilen araçlar listesi
        """
        # Önce kavşağı geçen tüm araçları serbest bırak
        for vehicle in vehicles:
            if vehicle.has_crossed and vehicle.is_waiting:
                vehicle.resume()
            # Ek kontrol: Kavşakta değil ama bekliyorsa da serbest bırak
            elif vehicle.has_crossed and not vehicle.rect.colliderect(self.rect) and vehicle.is_waiting:
                vehicle.resume()
        
        # Kavşağa yaklaşan araçları belirle (sadece henüz geçmemiş olanlar)
        approaching_vehicles = [v for v in vehicles if v.is_approaching_intersection(self.rect) and not v.has_crossed]
        
        # Kavşakta olan araçları belirle (sadece henüz geçmemiş olanlar)
        self.current_vehicles_in_intersection = [v for v in vehicles if v.rect.colliderect(self.rect) and not v.has_crossed]
        
        # Seçili kontrol stratejisine göre aracın geçip geçemeyeceğine karar ver
        if self.control_strategy == 'equal_priority':
            return self.equal_priority_strategy(approaching_vehicles)
        elif self.control_strategy == 'main_road_priority':
            return self.main_road_priority_strategy(approaching_vehicles)
        elif self.control_strategy == 'main_road_priority_enhanced':
            return self.main_road_priority_enhanced_strategy(approaching_vehicles)
        elif self.control_strategy == 'adaptive_timing':
            return self.adaptive_timing_strategy(approaching_vehicles)
        else:
            return self.equal_priority_strategy(approaching_vehicles)
    
    def equal_priority_strategy(self, approaching_vehicles):
        """
        Eşit öncelik stratejisi - ilk gelen ilk geçer
        
        Args:
            approaching_vehicles (list): Kavşağa yaklaşan araçlar
        
        Returns:
            list: Geçebilecek araçlar
        """
        allowed_vehicles = []
        
        # Kavşakta çarpışma olabilecek araçlar var mı?
        if len(self.current_vehicles_in_intersection) > 0:
            # Kavşak doluysa, hiçbir araca geçiş izni verme
            for vehicle in approaching_vehicles:
                vehicle.stop()
            return allowed_vehicles
        
        # Kavşak boşsa, kavşağa en yakın araca geçiş izni ver
        if approaching_vehicles:
            # En yakın aracı bul (basit bir yaklaşım)
            closest_vehicle = approaching_vehicles[0]
            
            for vehicle in approaching_vehicles:
                vehicle.stop()  # Önce tüm araçları durdur
            
            closest_vehicle.resume()  # Sadece en yakın aracın geçmesine izin ver
            allowed_vehicles.append(closest_vehicle)
        
        return allowed_vehicles
    
    def main_road_priority_strategy(self, approaching_vehicles):
        """
        Ana yol öncelik stratejisi - ana yoldaki araçlar önceliklidir
        
        Args:
            approaching_vehicles (list): Kavşağa yaklaşan araçlar
        
        Returns:
            list: Geçebilecek araçlar
        """
        allowed_vehicles = []
        
        # Kavşakta araç var mı?
        if len(self.current_vehicles_in_intersection) > 0:
            # Kavşak doluysa, hiçbir araca geçiş izni verme
            for vehicle in approaching_vehicles:
                vehicle.stop()
            return allowed_vehicles
        
        # Ana yol araçlarını ve diğer araçları ayır
        main_road_vehicles = [v for v in approaching_vehicles if v.direction in self.main_road_directions]
        other_road_vehicles = [v for v in approaching_vehicles if v.direction not in self.main_road_directions]
        
        # Saf ana yol önceliği - yan yol hiç geçmez
        # Normal ana yol önceliği
        if main_road_vehicles:
            # Ana yoldan geçecek araç sayısını belirle
            vehicles_to_pass = min(len(main_road_vehicles), 2)
            
            for i in range(vehicles_to_pass):
                if i < len(main_road_vehicles):
                    vehicle = main_road_vehicles[i]
                    allowed_vehicles.append(vehicle)
                    vehicle.resume()
            
            # Diğer tüm araçları durdur
            for vehicle in [v for v in approaching_vehicles if v not in allowed_vehicles]:
                vehicle.stop()
                
        # Yan yol araçları her zaman bekler (main road priority)
        else:
            # Tüm yan yol araçlarını durdur
            for vehicle in other_road_vehicles:
                vehicle.stop()
        
        # Priority timer'ı artır
        self.priority_timer += 1
        
        return allowed_vehicles
    
    def main_road_priority_enhanced_strategy(self, approaching_vehicles):
        """
        Gelişmiş ana yol öncelik stratejisi - ana yola öncelik verir ama daha adil
        
        Args:
            approaching_vehicles (list): Kavşağa yaklaşan araçlar
        
        Returns:
            list: Geçebilecek araçlar
        """
        allowed_vehicles = []
        
        # Kavşakta araç var mı?
        if len(self.current_vehicles_in_intersection) > 0:
            # Kavşak doluysa, hiçbir araca geçiş izni verme
            for vehicle in approaching_vehicles:
                vehicle.stop()
            return allowed_vehicles
        
        # Ana yol araçlarını ve diğer araçları ayır
        main_road_vehicles = [v for v in approaching_vehicles if v.direction in self.main_road_directions]
        other_road_vehicles = [v for v in approaching_vehicles if v.direction not in self.main_road_directions]
        
        # Zamanlama sistemi: 90 frame ana yol, sonra 30 frame diğer yollar
        cycle_length = 120
        main_road_phase = self.priority_timer % cycle_length < 90
        
        if main_road_phase and main_road_vehicles:
            # Ana yol fazı - ana yoldan araçları geçir
            vehicles_to_pass = min(len(main_road_vehicles), 2)
            
            for i in range(vehicles_to_pass):
                vehicle = main_road_vehicles[i]
                allowed_vehicles.append(vehicle)
                vehicle.resume()
            
            # Diğer araçları durdur
            for vehicle in other_road_vehicles:
                vehicle.stop()
                
        elif not main_road_phase and other_road_vehicles:
            # Diğer yollar fazı - diğer yollardan araçları geçir
            vehicles_to_pass = min(len(other_road_vehicles), 2)
            
            for i in range(vehicles_to_pass):
                vehicle = other_road_vehicles[i]
                allowed_vehicles.append(vehicle)
                vehicle.resume()
            
            # Ana yol araçlarını durdur
            for vehicle in main_road_vehicles:
                vehicle.stop()
                
        elif main_road_phase and not main_road_vehicles and other_road_vehicles:
            # Ana yol fazında ana yol araç yoksa, diğer yollardan geçir
            vehicle = other_road_vehicles[0]
            allowed_vehicles.append(vehicle)
            vehicle.resume()
            
            # Kalanları durdur
            for v in other_road_vehicles[1:]:
                v.stop()
                
        elif not main_road_phase and not other_road_vehicles and main_road_vehicles:
            # Diğer yol fazında diğer yol araç yoksa, ana yoldan geçir
            vehicle = main_road_vehicles[0]
            allowed_vehicles.append(vehicle)
            vehicle.resume()
            
            # Kalanları durdur
            for v in main_road_vehicles[1:]:
                v.stop()
        
        # Priority timer'ı artır
        self.priority_timer += 1
        
        return allowed_vehicles
    
    def adaptive_timing_strategy(self, approaching_vehicles):
        """
        Adaptif zamanlama stratejisi - Yoğun yöne öncelik verir
        
        Args:
            approaching_vehicles (list): Kavşağa yaklaşan araçlar
        
        Returns:
            list: Geçebilecek araçlar
        """
        allowed_vehicles = []
        
        # Kavşakta araç var mı?
        if len(self.current_vehicles_in_intersection) > 0:
            # Kavşak doluysa, hiçbir araca geçiş izni verme
            for vehicle in approaching_vehicles:
                vehicle.stop()
            return allowed_vehicles
        
        # Her yönden yaklaşan araç sayısını hesapla
        direction_counts = {
            'North': len([v for v in approaching_vehicles if v.direction == 'North']),
            'South': len([v for v in approaching_vehicles if v.direction == 'South']),
            'East': len([v for v in approaching_vehicles if v.direction == 'East']),
            'West': len([v for v in approaching_vehicles if v.direction == 'West'])
        }
        
        # Eğer mevcut bir öncelik yoksa veya öncelik süresi dolmuşsa yeni öncelik belirle
        if self.current_priority is None or self.priority_timer >= 45:  # Daha kısa öncelik süresi
            # En yoğun yönü bul
            max_count = 0
            max_direction = None
            directions_with_vehicles = []
            
            for direction, count in direction_counts.items():
                if count > 0:
                    directions_with_vehicles.append(direction)
                    if count > max_count:
                        max_count = count
                        max_direction = direction
            
            # Eğer hiç araç yoksa önceliği sıfırla
            if max_count == 0:
                self.current_priority = None
                self.priority_timer = 0
            else:
                # Daha dengeli rotasyon için
                if self.adaptive_counter >= 1 and len(directions_with_vehicles) > 1:
                    # En yoğun yönü listeden çıkar
                    directions_with_vehicles.remove(max_direction)
                    # Geriye kalan yönlerden rastgele birini seç
                    self.current_priority = random.choice(directions_with_vehicles)
                    self.adaptive_counter = 0
                else:
                    self.current_priority = max_direction
                    self.adaptive_counter += 1
                
                self.priority_timer = 0
        
        # Öncelikli yönden gelen araçları geçir
        if self.current_priority:
            priority_vehicles = [v for v in approaching_vehicles if v.direction == self.current_priority]
            
            if priority_vehicles:
                for vehicle in priority_vehicles:
                    vehicle.resume()
                    allowed_vehicles.append(vehicle)
                
                # Diğer yönlerden gelen araçları durdur
                for vehicle in [v for v in approaching_vehicles if v.direction != self.current_priority]:
                    vehicle.stop()
            else:
                # Öncelikli yönde araç yoksa, rastgele bir yönden araç geçir
                if approaching_vehicles:
                    # Rastgele araç seç
                    random_vehicle = random.choice(approaching_vehicles)
                    random_vehicle.resume()
                    allowed_vehicles.append(random_vehicle)
                    
                    for vehicle in [v for v in approaching_vehicles if v != random_vehicle]:
                        vehicle.stop()
        
        # Öncelik süresini artır
        self.priority_timer += 1
        
        return allowed_vehicles
    
    def update_stats(self, completed_vehicles):
        """
        Trafik akışı istatistiklerini günceller
        
        Args:
            completed_vehicles (list): Kavşağı geçmiş ve ekrandan çıkmış araçlar
        """
        for vehicle in completed_vehicles:
            direction = vehicle.direction
            stats = vehicle.get_stats()
            
            self.stats[direction]['vehicles_passed'] += 1
            self.stats[direction]['total_wait_time'] += stats['waiting_time']
            
            if self.stats[direction]['vehicles_passed'] > 0:
                self.stats[direction]['avg_wait_time'] = (
                    self.stats[direction]['total_wait_time'] / self.stats[direction]['vehicles_passed']
                )
        
        # Frame sayacını artır
        self.frame_count += 1
    
    def update_congestion_stats(self, vehicles):
        """
        Sıkışıklık istatistiklerini günceller
        
        Args:
            vehicles (list): Sistemdeki tüm araçlar
        """
        # Her yöndeki araç sayısını hesapla
        for direction in ['North', 'South', 'East', 'West']:
            current_vehicles = len([v for v in vehicles if v.direction == direction])
            self.stats[direction]['current_vehicles'] = current_vehicles
            
            # Sıkışıklık seviyesini hesapla (0-100 arası)
            max_vehicles = MAX_VEHICLES[direction]
            congestion_level = min(100, (current_vehicles / max_vehicles) * 100)
            self.stats[direction]['congestion_level'] = congestion_level
            
            # En yüksek sıkışıklığı kaydet
            if congestion_level > self.stats[direction]['peak_congestion']:
                self.stats[direction]['peak_congestion'] = congestion_level
            
            # Sıkışıklık geçmişini güncelle (son 100 frame)
            self.congestion_history[direction].append(congestion_level)
            if len(self.congestion_history[direction]) > 100:
                self.congestion_history[direction].pop(0)
    
    def get_congestion_analysis(self):
        """
        Sıkışıklık analizi raporu döndürür
        
        Returns:
            dict: Sıkışıklık analizi
        """
        analysis = {}
        
        for direction in ['North', 'South', 'East', 'West']:
            history = self.congestion_history[direction]
            
            if history:
                avg_congestion = sum(history) / len(history)
                current_congestion = self.stats[direction]['congestion_level']
                peak_congestion = self.stats[direction]['peak_congestion']
                
                # Sıkışıklık eğilimi hesapla (son 20 frame)
                if len(history) >= 20:
                    recent_avg = sum(history[-20:]) / 20
                    older_avg = sum(history[-40:-20]) / 20 if len(history) >= 40 else recent_avg
                    trend = recent_avg - older_avg
                else:
                    trend = 0
                
                analysis[direction] = {
                    'current': current_congestion,
                    'average': avg_congestion,
                    'peak': peak_congestion,
                    'trend': trend,
                    'is_main_road': direction == self.main_road_direction
                }
            else:
                analysis[direction] = {
                    'current': 0,
                    'average': 0,
                    'peak': 0,
                    'trend': 0,
                    'is_main_road': direction == self.main_road_direction
                }
        
        return analysis
    
    def generate_vehicle(self, vehicles, screen_width, screen_height):
        """
        Yeni araç oluşturur
        
        Args:
            vehicles (list): Mevcut araçlar listesi
            screen_width (int): Ekran genişliği
            screen_height (int): Ekran yüksekliği
        
        Returns:
            Vehicle: Oluşturulan yeni araç, yoksa None
        """
        from vehicle import Vehicle
        
        # Her yönden araç oluşturup oluşturmayacağına karar ver
        directions = ['North', 'South', 'East', 'West']
        
        # Yönleri rastgele karıştır (adil şans vermek için)
        random.shuffle(directions)
        
        # Her yön için olasılık değerlerini topla
        possible_directions = []
        
        for direction in directions:
            # Her yönden maksimum araç sayısını kontrol et
            current_count = len([v for v in vehicles if v.direction == direction])
            
            if current_count >= MAX_VEHICLES[direction]:
                continue
                
            # Olasılık hesaplaması
            if random.random() < VEHICLE_GENERATION_RATE[direction]:
                possible_directions.append(direction)
        
        # Uygun yönler varsa rastgele birini seç
        if possible_directions:
            selected_direction = random.choice(possible_directions)
            
            # Rastgele bir şerit konumu seç (0 veya 1)
            lane_position = random.randint(0, 1)
            
            # Yeni araç oluştur
            new_vehicle = Vehicle(selected_direction, lane_position, screen_width, screen_height)
            return new_vehicle
        
        return None
    
    def get_stats_report(self):
        """Kavşak istatistiklerini rapor formatında döndürür"""
        # Araç geçen yönleri say
        active_directions = 0
        total_wait_time = 0
        
        for direction, stats in self.stats.items():
            if stats['vehicles_passed'] > 0:
                active_directions += 1
                total_wait_time += stats['avg_wait_time']
        
        # Ortalama bekleme süresini hesapla (sadece araç geçen yönler için)
        if active_directions > 0:
            avg_wait_time = total_wait_time / active_directions
        else:
            avg_wait_time = 0
        
        # Ana yol istatistikleri
        main_road_stats = self.stats[self.main_road_direction]
        
        # Genel sıkışıklık seviyesi
        total_congestion = sum(stats['congestion_level'] for stats in self.stats.values()) / 4
            
        report = {
            'vehicles_passed': sum(stats['vehicles_passed'] for direction, stats in self.stats.items()),
            'avg_wait_time': avg_wait_time,
            'direction_stats': self.stats,
            'main_road_direction': self.main_road_direction,
            'main_road_stats': main_road_stats,
            'total_congestion': total_congestion,
            'congestion_analysis': self.get_congestion_analysis(),
            'frame_count': self.frame_count
        }
        
        return report