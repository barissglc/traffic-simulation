"""
Trafik Ajan Simülasyonu Ana Programı
"""
import pygame
import sys
import random
import time
import os
import matplotlib.pyplot as plt
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS,
    CONTROL_STRATEGIES, DEFAULT_STRATEGY, SIMULATION_DURATION, REPORT_INTERVAL,
    SAVE_SIMULATION, SAVE_PATH, BUILDING_POSITIONS, BUILDING_SIZE,
    ASSETS_FOLDER, USE_BUILDING_IMAGES
)
from vehicle import Vehicle
from intersection import Intersection
from visualization import Visualization


class Building:
    def __init__(self, x, y, size=BUILDING_SIZE):
        """
        Bina nesnesini oluşturur
        
        Args:
            x (int): Binanın x koordinatı
            y (int): Binanın y koordinatı
            size (int): Binanın boyutu
        """
        self.x = x
        self.y = y
        self.size = size
        self.color = (100, 100, 150)  # Bina rengi
        
        # Bina görseli
        self.use_image = USE_BUILDING_IMAGES
        self.image = None
        self.load_image()
    
    def load_image(self):
        """Bina simgesini yükler"""
        if self.use_image:
            try:
                # Bina resmini yükle
                image_path = os.path.join(ASSETS_FOLDER, "building.png")
                
                # Eğer resim dosyası yoksa, basit bir bina resmi oluştur
                if not os.path.exists(image_path):
                    self.create_default_building_image()
                
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                
            except Exception as e:
                print(f"Bina resmi yüklenirken hata: {e}")
                self.use_image = False
    
    def create_default_building_image(self):
        """Eğer bina resmi yoksa detaylı bir bina resmi oluşturur ve kaydeder"""
        try:
            # Bina boyutları
            building_width = 100
            building_height = 120
            
            # Daha büyük ve detaylı bir bina yüzeyi oluştur
            surface = pygame.Surface((building_width, building_height), pygame.SRCALPHA)
            
            # Binanın farklı bölümleri
            # Ana bina gövdesi
            building_base_color = self.color
            pygame.draw.rect(surface, building_base_color, (0, 30, building_width, 90), border_radius=2)
            
            # Bina çatısı - daha detaylı
            roof_color = (160, 82, 45)
            pygame.draw.polygon(surface, roof_color, 
                               [(0, 30), (building_width//2, 0), (building_width, 30)])
            
            # Çatı detayları - kiremit dokusu
            roof_line_color = (140, 70, 35)
            for i in range(1, 10):
                pygame.draw.line(surface, roof_line_color, 
                                (i * 10, 30 - i * 2), 
                                (i * 10, 5), 2)
            
            # Bina giriş kapısı
            door_color = (110, 60, 30)
            pygame.draw.rect(surface, door_color, (40, 85, 20, 35), border_radius=3)
            
            # Kapı kolu
            doorknob_color = (220, 220, 180)
            pygame.draw.circle(surface, doorknob_color, (55, 100), 2)
            
            # Pencereler - daha gerçekçi ve ışıklı görünüm
            window_positions = [
                # Üst kat
                (15, 40, 20, 25),
                (65, 40, 20, 25),
                # Orta kat
                (15, 70, 20, 20),
                (65, 70, 20, 20)
            ]
            
            # Pencere çizimi
            for window in window_positions:
                # Pencere çerçevesi
                frame_color = (180, 180, 150)
                pygame.draw.rect(surface, frame_color, window, border_radius=2)
                
                # Pencere camı
                window_color = (200, 230, 255, 200)
                inner_window = (window[0] + 2, window[1] + 2, window[2] - 4, window[3] - 4)
                pygame.draw.rect(surface, window_color, inner_window)
                
                # Pencere çapraz çerçeveleri
                pygame.draw.line(surface, frame_color, 
                                (window[0], window[1]), 
                                (window[0] + window[2], window[1] + window[3]), 1)
                pygame.draw.line(surface, frame_color, 
                                (window[0] + window[2], window[1]), 
                                (window[0], window[1] + window[3]), 1)
            
            # Baca
            chimney_color = (130, 70, 40)
            pygame.draw.rect(surface, chimney_color, (70, 5, 10, 20))
            pygame.draw.rect(surface, (100, 100, 100), (68, 0, 14, 5))
            
            # Baca dumanı (bulut etkisi)
            smoke_color = (220, 220, 220, 150)
            pygame.draw.circle(surface, smoke_color, (75, -5), 7)
            pygame.draw.circle(surface, smoke_color, (80, -8), 5)
            pygame.draw.circle(surface, smoke_color, (70, -8), 6)
            
            # Zemin & bahçe
            grass_color = (100, 180, 100)
            pygame.draw.rect(surface, grass_color, (0, 110, building_width, 10))
            
            # Çiçekler
            flower_positions = [(20, 112), (30, 113), (70, 112), (80, 113)]
            flower_colors = [(255, 50, 50), (255, 255, 50), (255, 150, 0), (200, 0, 200)]
            
            for i, pos in enumerate(flower_positions):
                pygame.draw.circle(surface, flower_colors[i % len(flower_colors)], pos, 3)
                pygame.draw.rect(surface, (0, 100, 0), (pos[0] - 1, pos[1] + 3, 2, 5))
            
            # Gölge efekti
            shadow_color = (0, 0, 0, 50)
            shadow_points = [(10, 120), (building_width - 10, 120), 
                           (building_width + 20, 110), (-20, 110)]
            pygame.draw.polygon(surface, shadow_color, shadow_points)
            
            # Assets klasörünü kontrol et
            if not os.path.exists(ASSETS_FOLDER):
                os.makedirs(ASSETS_FOLDER)
                
            # Resmi kaydet
            pygame.image.save(surface, os.path.join(ASSETS_FOLDER, "building.png"))
            
        except Exception as e:
            print(f"Bina resmi oluşturulurken hata: {e}")
            self.use_image = False
    
    def draw(self, screen):
        """Binayı ekrana çizer"""
        if self.use_image and self.image:
            # Simge ile çizim
            screen.blit(self.image, (self.x, self.y))
        else:
            # Basit dikdörtgen olarak çizim
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
            
            # Pencereler
            window_color = (200, 220, 255)
            for row in range(3):
                for col in range(3):
                    pygame.draw.rect(screen, window_color, 
                                    (self.x + 5 + col * 10, self.y + 5 + row * 10, 6, 6))


class TrafficSimulation:
    def __init__(self, control_strategy=DEFAULT_STRATEGY, headless=False):
        """
        Trafik simülasyonu başlatır
        
        Args:
            control_strategy (str): Kullanılacak trafik kontrol stratejisi
            headless (bool): Görsel arayüz olmadan çalıştırma modu
        """
        self.control_strategy = control_strategy
        self.headless = headless
        
        # Pygame başlat
        if not self.headless:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(f"Trafik Ajan Simülasyonu - {self.control_strategy}")
            self.clock = pygame.time.Clock()
        
        # Verileri kaydetmek için dizin oluştur
        if SAVE_SIMULATION and not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)
        
        # Simülasyon nesnelerini oluştur
        self.intersection = Intersection(SCREEN_WIDTH, SCREEN_HEIGHT, control_strategy)
        self.vehicles = []
        self.completed_vehicles = []
        
        # Binaları oluştur
        self.buildings = []
        for pos in BUILDING_POSITIONS:
            self.buildings.append(Building(pos["x"], pos["y"]))
        
        # Görselleştirme ve raporlama
        self.visualization = Visualization(save_results=SAVE_SIMULATION)
        
        # Simülasyon sayacı
        self.frame_count = 0
        self.start_time = time.time()
    
    def run(self):
        """Simülasyonu çalıştırır"""
        running = True
        
        while running and self.frame_count < SIMULATION_DURATION:
            # FPS sınırlama
            if not self.headless:
                self.clock.tick(FPS)
            
            # Klavye/pencere olaylarını kontrol et
            if not self.headless:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
            
            # Simülasyon adımı
            self.update()
            
            # Periyodik rapor güncelleme
            if self.frame_count % REPORT_INTERVAL == 0:
                self.visualization.update_stats(self.intersection.get_stats_report())
            
            # Çizim
            if not self.headless:
                self.draw()
            
            # Frame sayacını artır
            self.frame_count += 1
        
        # Simülasyon tamamlandı
        if not self.headless:
            pygame.quit()
        
        # Son raporu güncelle
        self.visualization.update_stats(self.intersection.get_stats_report())
        
        # Raporları oluştur
        self.visualization.generate_reports(self.control_strategy)
        
        # Sonuçları döndür
        return self.intersection.get_stats_report()
    
    def update(self):
        """Simülasyon mantığını günceller"""
        # Yeni araç oluştur
        new_vehicle = self.intersection.generate_vehicle(self.vehicles, SCREEN_WIDTH, SCREEN_HEIGHT)
        if new_vehicle:
            self.vehicles.append(new_vehicle)
        
        # Trafik kontrolü - araçların kavşağı geçip geçemeyeceğine karar ver
        self.intersection.control_traffic(self.vehicles)
        
        # Araçları güncelle
        vehicles_to_remove = []
        
        for vehicle in self.vehicles:
            # Aracın konumunu güncelle
            if vehicle.update(self.intersection.rect):
                # Araç ekrandan çıktı - tamamlanan araçları sakla
                if vehicle.has_crossed:
                    self.completed_vehicles.append(vehicle)
                
                # Ekrandan çıkan aracı listeden kaldır
                vehicles_to_remove.append(vehicle)
        
        # Ekrandan çıkan araçları kaldır
        for vehicle in vehicles_to_remove:
            if vehicle in self.vehicles:  # Güvenlik kontrolü
                self.vehicles.remove(vehicle)
        
        # İstatistikleri güncelle - Sadece kavşağı geçmeyi başaranları say
        self.intersection.update_stats(self.completed_vehicles)
        
        # Sıkışıklık istatistiklerini güncelle
        self.intersection.update_congestion_stats(self.vehicles)
        
        # Sayılan araçları temizle (tekrar sayılmamaları için)
        self.completed_vehicles = []
    
    def draw(self):
        """Ekranı çizer"""
        # Ekranı temizle
        self.screen.fill(BACKGROUND_COLOR)
        
        # Binaları çiz
        for building in self.buildings:
            building.draw(self.screen)
        
        # Kavşağı çiz
        self.intersection.draw(self.screen)
        
        # Araçları çiz
        for vehicle in self.vehicles:
            vehicle.draw(self.screen)
        
        # İstatistikleri ekranda göster
        self.visualization.draw_stats(self.screen, self.intersection)
        
        # Ekranı güncelle
        pygame.display.flip()


def run_single_simulation(strategy=DEFAULT_STRATEGY, headless=False):
    """
    Belirli bir strateji ile tek bir simülasyon çalıştırır
    
    Args:
        strategy (str): Kullanılacak kontrol stratejisi
        headless (bool): Görsel arayüz olmadan çalıştırma modu
    
    Returns:
        dict: Simülasyon sonuçları
    """
    print(f"Simülasyon başlatılıyor: {strategy}")
    simulation = TrafficSimulation(control_strategy=strategy, headless=headless)
    results = simulation.run()
    print(f"Simülasyon tamamlandı: {strategy}")
    print(f"Toplam araç: {results['vehicles_passed']}, Ortalama bekleme: {results['avg_wait_time']:.2f}s")
    return results


def run_comparative_simulation(headless=True):
    """
    Tüm stratejiler için karşılaştırmalı simülasyon çalıştırır
    
    Args:
        headless (bool): Görsel arayüz olmadan çalıştırma modu
    """
    results = {}
    
    for strategy in CONTROL_STRATEGIES:
        # Her strateji için bir simülasyon çalıştır
        results[strategy] = run_single_simulation(strategy, headless=headless)
    
    # Karşılaştırma raporunu oluştur
    viz = Visualization(save_results=SAVE_SIMULATION)
    viz.compare_strategies(results)
    
    return results


if __name__ == "__main__":
    # Komut satırı argümanlarını işle
    import argparse
    
    parser = argparse.ArgumentParser(description="Trafik Ajan Simülasyonu")
    parser.add_argument("--strategy", type=str, default=DEFAULT_STRATEGY,
                        choices=CONTROL_STRATEGIES,
                        help="Kullanılacak trafik kontrol stratejisi")
    parser.add_argument("--compare", action="store_true",
                        help="Tüm stratejileri karşılaştır")
    parser.add_argument("--headless", action="store_true",
                        help="Görsel arayüz olmadan çalıştır")
    
    args = parser.parse_args()
    
    if args.compare:
        run_comparative_simulation(headless=args.headless)
    else:
        run_single_simulation(strategy=args.strategy, headless=args.headless)