"""
Trafik Ajan Simülasyonu için Araç Sınıfı
"""
import pygame
import random
import time
import os
from config import (
    VEHICLE_WIDTH, VEHICLE_LENGTH, VEHICLE_COLORS, SPEED_RANGE,
    ASSETS_FOLDER, USE_VEHICLE_IMAGES
)

class Vehicle:
    def __init__(self, direction, lane_position, screen_width, screen_height):
        """
        Araç nesnesini oluşturur
        
        Args:
            direction (str): Aracın geldiği yön ('North', 'South', 'East', 'West')
            lane_position (int): Şeritteki konumu
            screen_width (int): Ekran genişliği
            screen_height (int): Ekran yüksekliği
        """
        self.direction = direction
        self.lane_position = lane_position
        self.color = VEHICLE_COLORS[direction]
        self.width = VEHICLE_WIDTH
        self.length = VEHICLE_LENGTH
        
        # Hız faktörü (piksel/frame)
        self.speed = random.uniform(SPEED_RANGE['min'], SPEED_RANGE['max'])
        
        # Aracın başlangıç konumu ve rotasını ayarla
        self.init_position(screen_width, screen_height)
        
        # Çarpışma kontrolü ve davranış ayarları
        self.is_waiting = False
        self.has_crossed = False
        self.waiting_time = 0
        self.start_time = time.time()
        self.cross_time = None
        
        # Araba simgesi yükleme
        self.use_image = USE_VEHICLE_IMAGES
        self.image = None
        self.load_image()
        
        # Collision rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.length)
    
    def load_image(self):
        """Araba simgesini yükler"""
        if self.use_image:
            try:
                # Farklı renkli araçlar için farklı dosya adları
                car_colors = {
                    'North': 'red_car.png',
                    'South': 'blue_car.png',
                    'East': 'green_car.png',
                    'West': 'yellow_car.png'
                }
                
                # Araba resmini yükle
                image_path = os.path.join(ASSETS_FOLDER, car_colors[self.direction])
                
                # Eğer resim dosyası yoksa, basit bir araba resmi oluştur
                if not os.path.exists(image_path):
                    self.create_default_car_image(car_colors[self.direction])
                    
                self.image = pygame.image.load(image_path)
                
                # Resmi ölçeklendir
                self.image = pygame.transform.scale(self.image, (self.length, self.width))
                
                # Aracın yönüne göre resmi döndür
                if self.direction == 'North':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'South':
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == 'East':
                    self.image = pygame.transform.rotate(self.image, 180)
                # West yönü için rotasyon gerekmez (0 derece)
                
            except Exception as e:
                print(f"Araba resmi yüklenirken hata: {e}")
                self.use_image = False
    
    def create_default_car_image(self, filename):
        """Eğer araba resmi yoksa daha detaylı bir araba resmi oluşturur ve kaydeder"""
        try:
            # Araba boyutları
            car_width = 60
            car_height = 30
            
            # Daha büyük ve detaylı bir araba yüzeyi oluştur
            surface = pygame.Surface((car_width, car_height), pygame.SRCALPHA)
            
            # Araç gövdesi - ana gövde
            body_color = self.color
            
            # Araba gövdesinin alt kısmı
            pygame.draw.rect(surface, body_color, (5, 10, 50, 20), border_radius=3)
            
            # Üst kabin kısmı
            pygame.draw.rect(surface, body_color, (15, 2, 30, 12), border_radius=5)
            
            # Tamponlar
            bumper_color = (60, 60, 60)
            pygame.draw.rect(surface, bumper_color, (2, 12, 5, 16), border_radius=2)  # Ön tampon
            pygame.draw.rect(surface, bumper_color, (53, 12, 5, 16), border_radius=2)  # Arka tampon
            
            # Tekerlekler
            wheel_color = (30, 30, 30)
            pygame.draw.circle(surface, wheel_color, (15, 28), 5)  # Sol ön tekerlek
            pygame.draw.circle(surface, wheel_color, (45, 28), 5)  # Sağ ön tekerlek
            
            # Tekerlek jantları
            wheel_rim_color = (180, 180, 180)
            pygame.draw.circle(surface, wheel_rim_color, (15, 28), 2)  # Sol ön jant
            pygame.draw.circle(surface, wheel_rim_color, (45, 28), 2)  # Sağ ön jant
            
            # Farlar
            headlight_color = (255, 255, 200)
            pygame.draw.circle(surface, headlight_color, (7, 15), 3)  # Sol far
            pygame.draw.circle(surface, headlight_color, (7, 25), 3)  # Sağ far
            
            # Arka lambalar
            taillight_color = (255, 50, 50)
            pygame.draw.rect(surface, taillight_color, (53, 14, 4, 4), border_radius=1)  # Sol arka lamba
            pygame.draw.rect(surface, taillight_color, (53, 22, 4, 4), border_radius=1)  # Sağ arka lamba
            
            # Camlar - daha şeffaf ve parlak
            window_color = (200, 230, 255, 180)
            
            # Ön cam - trapezoid
            pygame.draw.polygon(surface, window_color, 
                               [(18, 4), (42, 4), (40, 10), (20, 10)])
            
            # Yan camlar
            pygame.draw.rect(surface, window_color, (15, 10, 8, 6))   # Sol yan cam
            pygame.draw.rect(surface, window_color, (37, 10, 8, 6))   # Sağ yan cam
            
            # Gölgelendirme (derinlik etkisi için)
            shadow_color = (0, 0, 0, 30)  # Yarı saydam siyah
            pygame.draw.rect(surface, shadow_color, (10, 20, 40, 8))

            # Assets klasörünü kontrol et ve oluştur
            if not os.path.exists(ASSETS_FOLDER):
                os.makedirs(ASSETS_FOLDER)
                
            # Resmi kaydet
            file_path = os.path.join(ASSETS_FOLDER, filename)
            pygame.image.save(surface, file_path)
            
        except Exception as e:
            print(f"Araba resmi oluşturulurken hata: {e}")
            self.use_image = False
    
    def init_position(self, screen_width, screen_height):
        """Aracın başlangıç konumunu ve hedef konumunu ayarlar"""
        half_width = screen_width // 2
        half_height = screen_height // 2
        
        if self.direction == 'North':
            # Yukarıdan geliyor, aşağıya gidiyor
            self.x = half_width - 20 + self.lane_position * 10
            self.y = 0 - self.length
            self.target_x = half_width - 20 + self.lane_position * 10
            self.target_y = screen_height + self.length
            self.rotation = 90  # Aşağı doğru
        
        elif self.direction == 'South':
            # Aşağıdan geliyor, yukarıya gidiyor
            self.x = half_width + self.lane_position * 10
            self.y = screen_height + self.length
            self.target_x = half_width + self.lane_position * 10
            self.target_y = 0 - self.length
            self.rotation = 270  # Yukarı doğru
        
        elif self.direction == 'East':
            # Sağdan geliyor, sola gidiyor
            self.x = screen_width + self.length
            self.y = half_height + self.lane_position * 10
            self.target_x = 0 - self.length
            self.target_y = half_height + self.lane_position * 10
            self.rotation = 180  # Sola doğru
        
        elif self.direction == 'West':
            # Soldan geliyor, sağa gidiyor
            self.x = 0 - self.length
            self.y = half_height - 20 + self.lane_position * 10
            self.target_x = screen_width + self.length
            self.target_y = half_height - 20 + self.lane_position * 10
            self.rotation = 0  # Sağa doğru
    
    def update(self, intersection_rect):
        """
        Aracın pozisyonunu günceller
        
        Args:
            intersection_rect (pygame.Rect): Kavşak bölgesinin çarpışma dikdörtgeni
        
        Returns:
            bool: Araç ekrandan çıktıysa True, aksi halde False
        """
        # Önce kavşağı geçip geçmediğini kontrol et
        if not self.has_crossed and self.has_crossed_intersection(intersection_rect):
            self.has_crossed = True
            # Araç kavşağı geçtiyse, beklemiyorsa hemen devam etsin
            if self.is_waiting:
                self.resume()
        
        # Kavşak bölgesine yaklaşıyor mu? (sadece henüz geçmemişse)
        approaching_intersection = not self.has_crossed and self.is_approaching_intersection(intersection_rect)
        
        # Kavşakta mı?
        in_intersection = self.rect.colliderect(intersection_rect)
        
        # Kavşak zamanını kaydet
        if in_intersection and not self.has_crossed and not self.cross_time:
            self.cross_time = time.time()
            
        # Hız kontrolü - kavşağı geçmişse tam hızla git
        if self.has_crossed:
            current_speed = self.speed  # Kavşağı geçtikten sonra tam hız
        elif not self.is_waiting and approaching_intersection and not in_intersection:
            # Sadece kavşağa yaklaşırken yavaşla (kavşakta değilken)
            current_speed = self.speed * 0.8
        else:
            current_speed = self.speed
        
        # Pozisyonu güncelle
        if self.direction == 'North':
            if not self.is_waiting:
                self.y += current_speed
        elif self.direction == 'South':
            if not self.is_waiting:
                self.y -= current_speed
        elif self.direction == 'East':
            if not self.is_waiting:
                self.x -= current_speed
        elif self.direction == 'West':
            if not self.is_waiting:
                self.x += current_speed
        
        # Çarpışma dikdörtgenini güncelle
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.length)
        
        # Ekrandan çıktı mı kontrolü
        if self.direction == 'North' and self.y > self.target_y:
            return True
        elif self.direction == 'South' and self.y < self.target_y:
            return True
        elif self.direction == 'East' and self.x < self.target_x:
            return True
        elif self.direction == 'West' and self.x > self.target_x:
            return True
        
        return False
    
    def is_approaching_intersection(self, intersection_rect, buffer=30):
        """Aracın kavşağa yaklaşıp yaklaşmadığını kontrol eder"""
        # Eğer araç kavşağı geçmişse, artık yaklaşmıyor demektir
        if self.has_crossed:
            return False
            
        # Buffer değerini azalttık (50 -> 30) 
        expanded_rect = intersection_rect.inflate(buffer, buffer)
        return self.rect.colliderect(expanded_rect) and not self.rect.colliderect(intersection_rect)
    
    def has_crossed_intersection(self, intersection_rect):
        """Aracın kavşağı geçip geçmediğini kontrol eder"""
        # Araç kavşağın ortasını geçtiğinde "geçti" olarak işaretle (daha erken)
        center_x = intersection_rect.centerx
        center_y = intersection_rect.centery
        
        if self.direction == 'North':
            # Aracın ön kısmı kavşak merkezini geçtiyse
            return self.y > center_y
        elif self.direction == 'South':
            # Aracın ön kısmı kavşak merkezini geçtiyse
            return self.y + self.length < center_y
        elif self.direction == 'East':
            # Aracın ön kısmı kavşak merkezini geçtiyse
            return self.x + self.length < center_x
        elif self.direction == 'West':
            # Aracın ön kısmı kavşak merkezini geçtiyse
            return self.x > center_x
    
    def draw(self, screen):
        """Aracı ekrana çizer"""
        if self.use_image and self.image:
            # Simge ile çizim
            screen.blit(self.image, (int(self.x), int(self.y)))
        else:
            # Basit dikdörtgen olarak çizim
            if self.direction in ['North', 'South']:
                rect = pygame.Rect(int(self.x), int(self.y), self.width, self.length)
            else:
                rect = pygame.Rect(int(self.x), int(self.y), self.length, self.width)
            
            pygame.draw.rect(screen, self.color, rect)
    
    def stop(self):
        """Aracı durdurur"""
        if not self.is_waiting:
            self.is_waiting = True
            self.waiting_time_start = time.time()
    
    def resume(self):
        """Aracı tekrar hareket ettirir"""
        if self.is_waiting:
            self.is_waiting = False
            wait_duration = time.time() - self.waiting_time_start
            # 0 saniyeyi önlemek için minimum bir değer koy
            self.waiting_time += max(wait_duration, 0.01)
    
    def get_stats(self):
        """Araç istatistiklerini döndürür"""
        current_time = time.time()
        total_time = current_time - self.start_time
        
        # Hala bekliyor ise bekleme süresini güncelle
        if self.is_waiting:
            current_waiting = time.time() - self.waiting_time_start
            total_waiting = self.waiting_time + current_waiting
        else:
            total_waiting = self.waiting_time
        
        if self.cross_time:
            cross_duration = self.cross_time - self.start_time
        else:
            cross_duration = None
        
        return {
            'direction': self.direction,
            'total_time': total_time,
            'waiting_time': total_waiting,
            'cross_time': cross_duration,
            'has_crossed': self.has_crossed
        }