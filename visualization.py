"""
Trafik Ajan Simülasyonu için Görselleştirme ve Raporlama Araçları
"""
import pygame
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from config import SAVE_PATH, BACKGROUND_COLOR

class Visualization:
    def __init__(self, save_results=True):
        """
        Görselleştirme ve raporlama sınıfını başlatır
        
        Args:
            save_results (bool): Sonuçların kaydedilip kaydedilmeyeceği
        """
        self.save_results = save_results
        self.stats_history = []
        
        # Kayıt klasörü oluştur
        if self.save_results and not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)
    
    def update_stats(self, stats):
        """
        İstatistik verilerini günceller
        
        Args:
            stats (dict): Güncel istatistik verileri
        """
        self.stats_history.append(stats)
    
    def draw_stats(self, screen, intersection):
        """
        Gerçek zamanlı istatistikleri ekrana çizer
        
        Args:
            screen (pygame.Surface): Çizim yapılacak ekran
            intersection (Intersection): Kavşak nesnesi
        """
        # Font oluştur
        font = pygame.font.SysFont('Arial', 14)
        small_font = pygame.font.SysFont('Arial', 12)
        
        # İstatistikleri al
        stats = intersection.get_stats_report()
        
        # Ekranın üstünde daha büyük istatistik kutusu oluştur
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), 90))
        
        # Genel istatistikler
        total_text = font.render(f"Toplam Araç: {stats['vehicles_passed']} | Ort. Bekleme: {stats['avg_wait_time']:.2f}s | Genel Sıkışıklık: {stats['total_congestion']:.1f}%", True, (255, 255, 255))
        screen.blit(total_text, (10, 10))
        
        # Ana yol bilgisi
        main_road_text = font.render(f"Ana Yol: {stats['main_road_direction']} | Ana Yol Araçları: {stats['main_road_stats']['vehicles_passed']}", True, (255, 255, 100))
        screen.blit(main_road_text, (10, 30))
        
        # Kontrol stratejisi
        strategy_name = {
            'equal_priority': 'Eşit Öncelik',
            'main_road_priority': 'Ana Yol Önceliği',
            'main_road_priority_enhanced': 'Gelişmiş Ana Yol Önceliği',
            'adaptive_timing': 'Adaptif Zamanlama'
        }
        
        strategy_text = font.render(f"Strateji: {strategy_name.get(intersection.control_strategy, intersection.control_strategy)}", True, (255, 255, 255))
        screen.blit(strategy_text, (500, 10))
        
        # Yön bazlı istatistikler
        directions = ['North', 'South', 'East', 'West']
        direction_names = {
            'North': 'Kuzey',
            'South': 'Güney', 
            'East': 'Doğu',
            'West': 'Batı'
        }
        
        # Her yön için detaylı bilgi göster
        for i, direction in enumerate(directions):
            dir_stats = stats['direction_stats'][direction]
            congestion = stats['congestion_analysis'][direction]
            
            # Ana yol vurgusu
            color = (255, 255, 100) if direction == stats['main_road_direction'] else (255, 255, 255)
            
            # Sıkışıklık durumu
            congestion_indicator = ""
            if congestion['current'] > 70:
                congestion_indicator = "🔴"
            elif congestion['current'] > 40:
                congestion_indicator = "🟡"
            else:
                congestion_indicator = "🟢"
            
            dir_text = small_font.render(
                f"{direction_names[direction]}: {dir_stats['vehicles_passed']} araç | {dir_stats['current_vehicles']} şu anda | Sıkışıklık: {congestion['current']:.0f}% {congestion_indicator}", 
                True, 
                color
            )
            screen.blit(dir_text, (10 + (i % 2) * 380, 50 + (i // 2) * 15))
        
        # Sağ tarafta ana yol sıkışıklık analizi
        congestion_analysis = stats['congestion_analysis'][stats['main_road_direction']]
        
        # Ana yol sıkışıklık kutusu
        pygame.draw.rect(screen, (40, 40, 40), (screen.get_width() - 200, 25, 190, 60))
        
        main_road_title = small_font.render("ANA YOL DURUM", True, (255, 255, 100))
        screen.blit(main_road_title, (screen.get_width() - 195, 30))
        
        current_cong = small_font.render(f"Şu an: {congestion_analysis['current']:.0f}%", True, (255, 255, 255))
        screen.blit(current_cong, (screen.get_width() - 195, 45))
        
        peak_cong = small_font.render(f"En yüksek: {congestion_analysis['peak']:.0f}%", True, (255, 255, 255))
        screen.blit(peak_cong, (screen.get_width() - 195, 60))
        
        # Sıkışıklık eğilimi
        trend_text = "↗️" if congestion_analysis['trend'] > 5 else "↘️" if congestion_analysis['trend'] < -5 else "➡️"
        trend = small_font.render(f"Eğilim: {trend_text}", True, (255, 255, 255))
        screen.blit(trend, (screen.get_width() - 120, 45))
    
    def generate_reports(self, strategy_name):
        """
        Simülasyon sonuçlarını grafiksel olarak raporlar
        
        Args:
            strategy_name (str): Kullanılan kontrol stratejisinin adı
        """
        if not self.stats_history:
            print("Rapor oluşturmak için yeterli veri yok!")
            return
        
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ana yol bilgilerini kontrol et
        has_main_road = 'main_road_direction' in self.stats_history[-1]
        
        if has_main_road:
            # Ana yol sistemi var - 3x2 grid kullan
            fig, axes = plt.subplots(3, 2, figsize=(16, 14))
            fig.suptitle(f'Ana Yol Trafik Simülasyonu Sonuçları - {strategy_name}')
        else:
            # Standart sistem - 2x2 grid kullan
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'Trafik Simülasyonu Sonuçları - {strategy_name}')
        
        # Son istatistikleri al
        final_stats = self.stats_history[-1]
        directions = ['North', 'South', 'East', 'West']
        direction_names = ['Kuzey', 'Güney', 'Doğu', 'Batı']
        
        # 1. Grafik: Yön bazlı toplam araç sayısı
        vehicles_passed = [final_stats['direction_stats'][d]['vehicles_passed'] for d in directions]
        axes[0, 0].bar(direction_names, vehicles_passed, color=['red', 'blue', 'green', 'yellow'])
        axes[0, 0].set_ylabel('Araç Sayısı')
        axes[0, 0].set_xlabel('Yön')
        axes[0, 0].set_title('Toplam Geçen Araç Sayısı')
        
        # Her çubuğun üzerine değeri yaz
        for i, v in enumerate(vehicles_passed):
            axes[0, 0].text(i, v + 0.1, str(v), ha='center')
        
        # 2. Grafik: Yön bazlı ortalama bekleme süresi
        avg_wait_times = [final_stats['direction_stats'][d]['avg_wait_time'] for d in directions]
        axes[0, 1].bar(direction_names, avg_wait_times, color=['red', 'blue', 'green', 'yellow'])
        axes[0, 1].set_ylabel('Ortalama Bekleme Süresi (s)')
        axes[0, 1].set_xlabel('Yön')
        axes[0, 1].set_title('Yön Bazlı Ortalama Bekleme Süresi')
        
        # Bekleme süresi değerlerini grafik üzerine yazmıyoruz - grafiği temiz tutmak için
        
        # 3. Grafik: Zaman içinde toplam araç sayısı
        time_points = list(range(len(self.stats_history)))
        cumulative_vehicles = [stats['vehicles_passed'] for stats in self.stats_history]
        
        axes[1, 0].plot(time_points, cumulative_vehicles, 'b-')
        axes[1, 0].set_ylabel('Toplam Araç Sayısı')
        axes[1, 0].set_xlabel('Simülasyon Zamanı')
        axes[1, 0].set_title('Zaman İçinde Toplam Araç Sayısı')
        
        # 4. Grafik: Her yön için ayrı ortalama bekleme süresi
        for i, direction in enumerate(directions):
            wait_times = [stats['direction_stats'][direction]['avg_wait_time'] for stats in self.stats_history]
            axes[1, 1].plot(time_points, wait_times, label=direction_names[i])
        
        axes[1, 1].set_ylabel('Ortalama Bekleme Süresi (s)')
        axes[1, 1].set_xlabel('Simülasyon Zamanı')
        axes[1, 1].set_title('Yön Bazlı Ortalama Bekleme Süresi Değişimi')
        axes[1, 1].legend()
        
        # Ana yol sistemi varsa ek grafikler ekle
        if has_main_road:
            main_road_direction = final_stats['main_road_direction']
            main_road_idx = directions.index(main_road_direction)
            
            # 5. Grafik: Ana yol vs diğer yollar araç karşılaştırması
            main_road_vehicles = final_stats['direction_stats'][main_road_direction]['vehicles_passed']
            other_vehicles = sum(final_stats['direction_stats'][d]['vehicles_passed'] 
                               for d in directions if d != main_road_direction)
            
            axes[2, 0].pie([main_road_vehicles, other_vehicles], 
                          labels=[f'Ana Yol ({direction_names[main_road_idx]})', 'Diğer Yollar'],
                          autopct='%1.1f%%',
                          colors=['gold', 'lightblue'])
            axes[2, 0].set_title('Ana Yol vs Diğer Yollar - Araç Dağılımı')
            
            # 6. Grafik: Sıkışıklık analizi (zaman içinde)
            if 'congestion_analysis' in final_stats:
                for i, direction in enumerate(directions):
                    # Sıkışıklık geçmişini stats_history'den çıkar
                    congestion_history = []
                    for stats in self.stats_history:
                        if 'congestion_analysis' in stats:
                            congestion_history.append(stats['congestion_analysis'][direction]['current'])
                        else:
                            congestion_history.append(0)
                    
                    # Ana yol için farklı stil
                    if direction == main_road_direction:
                        axes[2, 1].plot(time_points[:len(congestion_history)], congestion_history, 
                                       label=f'{direction_names[i]} (Ana Yol)', 
                                       linewidth=3, color='red')
                    else:
                        axes[2, 1].plot(time_points[:len(congestion_history)], congestion_history, 
                                       label=direction_names[i], alpha=0.7)
                
                axes[2, 1].set_ylabel('Sıkışıklık Seviyesi (%)')
                axes[2, 1].set_xlabel('Simülasyon Zamanı')
                axes[2, 1].set_title('Yön Bazlı Sıkışıklık Seviyesi Değişimi')
                axes[2, 1].legend()
                axes[2, 1].axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Kritik Sıkışıklık')
                axes[2, 1].axhline(y=40, color='orange', linestyle='--', alpha=0.5, label='Orta Sıkışıklık')
        
        # Raporu kaydet
        if self.save_results:
            filepath = os.path.join(SAVE_PATH, f"trafik_raporu_{strategy_name}_{now}.png")
            plt.tight_layout()
            plt.savefig(filepath)
            print(f"Rapor kaydedildi: {filepath}")
            
            # Verileri metin dosyasına da kaydet
            text_report = os.path.join(SAVE_PATH, f"trafik_raporu_{strategy_name}_{now}.txt")
            with open(text_report, 'w', encoding='utf-8') as f:
                f.write(f"Trafik Simülasyonu Sonuçları - {strategy_name}\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Toplam Geçen Araç Sayısı: {final_stats['vehicles_passed']}\n")
                f.write(f"Ortalama Bekleme Süresi: {final_stats['avg_wait_time']:.2f}s\n")
                
                if has_main_road:
                    f.write(f"Genel Sıkışıklık Seviyesi: {final_stats['total_congestion']:.1f}%\n")
                    f.write(f"Ana Yol: {final_stats['main_road_direction']}\n")
                    f.write(f"Ana Yol Araç Sayısı: {final_stats['main_road_stats']['vehicles_passed']}\n\n")
                else:
                    f.write("\n")
                
                f.write("Yön Bazlı İstatistikler:\n")
                for i, direction in enumerate(directions):
                    dir_stats = final_stats['direction_stats'][direction]
                    f.write(f"  {direction_names[i]}: {dir_stats['vehicles_passed']} araç, {dir_stats['avg_wait_time']:.2f}s ort. bekleme")
                    
                    if has_main_road:
                        congestion = final_stats['congestion_analysis'][direction]
                        is_main = " (ANA YOL)" if direction == final_stats['main_road_direction'] else ""
                        f.write(f", Sıkışıklık: {congestion['current']:.1f}% (En yüksek: {congestion['peak']:.1f}%){is_main}")
                    
                    f.write("\n")
                    
                if has_main_road:
                    f.write("\nSıkışıklık Analizi:\n")
                    for i, direction in enumerate(directions):
                        congestion = final_stats['congestion_analysis'][direction]
                        f.write(f"  {direction_names[i]}: Şu an {congestion['current']:.1f}%, Ortalama {congestion['average']:.1f}%, En yüksek {congestion['peak']:.1f}%\n")
        
        return fig
    
    def compare_strategies(self, stats_dict):
        """
        Farklı kontrol stratejilerini karşılaştırır
        
        Args:
            stats_dict (dict): Her strateji için son istatistikler
                Örnek: {'strategy1': stats1, 'strategy2': stats2, ...}
        """
        if not stats_dict or len(stats_dict) < 2:
            print("Karşılaştırma için en az iki strateji gereklidir!")
            return
        
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Karşılaştırma grafikleri
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle('Kontrol Stratejileri Karşılaştırması')
        
        # Strateji isimleri ve istatistikler
        strategy_names = list(stats_dict.keys())
        strategy_display_names = {
            'equal_priority': 'Eşit Öncelik',
            'main_road_priority': 'Ana Yol Önceliği',
            'main_road_priority_enhanced': 'Gelişmiş Ana Yol Önceliği',
            'adaptive_timing': 'Adaptif Zamanlama'
        }
        
        # Kısa isimlerle değiştir
        display_names = [strategy_display_names.get(s, s) for s in strategy_names]
        
        # 1. Grafik: Toplam araç sayısı karşılaştırması
        vehicles_passed = [stats_dict[s]['vehicles_passed'] for s in strategy_names]
        
        axes[0].bar(display_names, vehicles_passed)
        axes[0].set_ylabel('Toplam Araç Sayısı')
        axes[0].set_title('Stratejilere Göre Toplam Geçen Araç Sayısı')
        
        # 2. Grafik: Ortalama bekleme süresi karşılaştırması
        avg_wait_times = [stats_dict[s]['avg_wait_time'] for s in strategy_names]
        
        axes[1].bar(display_names, avg_wait_times)
        axes[1].set_ylabel('Ortalama Bekleme Süresi (s)')
        axes[1].set_title('Stratejilere Göre Ortalama Bekleme Süresi')
        
        # Sadece araç sayısı değerlerini göster, bekleme süresini gösterme
        for i, v in enumerate(vehicles_passed):
            axes[0].text(i, v + 0.1, str(v), ha='center')
            
        # Bekleme süresi değerlerini grafik üzerine yazmıyoruz - grafiği temiz tutmak için
        
        # Grafiği kaydet
        if self.save_results:
            filepath = os.path.join(SAVE_PATH, f"strateji_karsilastirma_{now}.png")
            plt.tight_layout()
            plt.savefig(filepath)
            print(f"Karşılaştırma raporu kaydedildi: {filepath}")
            
            # Metin dosyasına detaylı raporu kaydet
            text_report = os.path.join(SAVE_PATH, f"strateji_karsilastirma_{now}.txt")
            with open(text_report, 'w', encoding='utf-8') as f:
                f.write("Trafik Kontrol Stratejileri Karşılaştırması\n")
                f.write("=" * 50 + "\n\n")
                
                for i, strategy in enumerate(strategy_names):
                    stats = stats_dict[strategy]
                    f.write(f"{display_names[i]} Stratejisi:\n")
                    f.write(f"  Toplam Geçen Araç: {stats['vehicles_passed']}\n")
                    f.write(f"  Ortalama Bekleme Süresi: {stats['avg_wait_time']:.2f}s\n")
                    
                    f.write("  Yön Bazlı İstatistikler:\n")
                    for direction in ['North', 'South', 'East', 'West']:
                        dir_name = {'North': 'Kuzey', 'South': 'Güney', 'East': 'Doğu', 'West': 'Batı'}[direction]
                        dir_stats = stats['direction_stats'][direction]
                        f.write(f"    {dir_name}: {dir_stats['vehicles_passed']} araç, {dir_stats['avg_wait_time']:.2f}s ort. bekleme\n")
                    
                    f.write("\n")
                
                # Sonuçların yorumlanması
                f.write("Sonuçların Yorumlanması:\n")
                f.write("-" * 30 + "\n")
                
                # En iyi stratejiyi bul (en az bekleme süresi)
                best_strategy_idx = np.argmin(avg_wait_times)
                best_strategy = strategy_names[best_strategy_idx]
                best_display = display_names[best_strategy_idx]
                
                # En fazla aracın geçtiği strateji
                max_vehicles_idx = np.argmax(vehicles_passed)
                max_vehicle_strategy = strategy_names[max_vehicles_idx]
                max_vehicle_display = display_names[max_vehicles_idx]
                
                f.write(f"En düşük ortalama bekleme süresine sahip strateji: {best_display} ({avg_wait_times[best_strategy_idx]:.2f}s)\n")
                f.write(f"En fazla aracın geçtiği strateji: {max_vehicle_display} ({vehicles_passed[max_vehicles_idx]} araç)\n\n")
                
                # Kapsamlı değerlendirme
                f.write("Genel Değerlendirme:\n")
                
                if best_strategy == max_vehicle_strategy:
                    f.write(f"{best_display} stratejisi hem en düşük bekleme süresine hem de en yüksek araç akışına sahip olması nedeniyle bu senaryoda en verimli strateji olarak öne çıkmaktadır.\n")
                else:
                    wait_diff = max(avg_wait_times) - min(avg_wait_times)
                    vehicle_diff = max(vehicles_passed) - min(vehicles_passed)
                    
                    f.write(f"Ortalama bekleme süreleri arasındaki fark: {wait_diff:.2f}s\n")
                    f.write(f"Geçen araç sayıları arasındaki fark: {vehicle_diff} araç\n\n")
                    
                    if wait_diff > 5.0:  # 5 saniyeden fazla fark varsa
                        f.write("Bekleme süreleri arasında önemli bir fark vardır. Trafik yoğunluğuna göre uygun strateji seçimi önemlidir.\n")
                    else:
                        f.write("Bekleme süreleri arasındaki fark minimal düzeydedir. Tercih, trafik yoğunluğuna ve senaryoya bağlı olarak değişebilir.\n")
        
        return fig