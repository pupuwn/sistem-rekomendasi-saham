import numpy as np

class FuzzificationEngine:
    """
    Engine untuk melakukan Fuzzifikasi (Crisp to Fuzzy)
    Mengubah nilai numerik menjadi derajat keanggotaan fuzzy
    """
    
    @staticmethod
    def triangular_membership(x, a, b, c):
        """
        Fungsi keanggotaan Segitiga
        
        Parameters:
        - x: nilai input (crisp)
        - a: batas kiri
        - b: puncak
        - c: batas kanan
        
        Returns:
        - membership degree (0-1)
        """
        if x <= a:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return (c - x) / (c - b)
        else:
            return 0.0
    
    @staticmethod
    def trapezoid_membership(x, a, b, c, d):
        """
        Fungsi keanggotaan Trapezoid
        
        Parameters:
        - x: nilai input (crisp)
        - a: batas bawah
        - b: batas atas segitiga kiri (peak start)
        - c: batas bawah segitiga kanan (peak end)
        - d: batas atas
        
        Returns:
        - membership degree (0-1)
        """
        if x <= a:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return 1.0
        elif c < x <= d:
            return (d - x) / (d - c)
        else:
            return 0.0
    
    def fuzzify_value(self, value, fuzzy_sets):
        """
        Fuzzifikasi nilai input terhadap semua himpunan fuzzy
        
        Parameters:
        - value: nilai crisp yang akan difuzzifikasi
        - fuzzy_sets: list of dict dengan struktur:
          [
            {
              'set_name': 'Rendah',
              'min_value': 0,
              'max_value': 500,
              'peak_start': 0,
              'peak_end': 200
            },
            ...
          ]
        
        Returns:
        - dict: {'Rendah': 0.5, 'Sedang': 0.3, 'Tinggi': 0.0}
        """
        result = {}
        
        for fuzzy_set in fuzzy_sets:
            set_name = fuzzy_set['set_name']
            a = fuzzy_set['min_value']
            b = fuzzy_set['peak_start']
            c = fuzzy_set['peak_end']
            d = fuzzy_set['max_value']
            
            # Check if it's a triangular or trapezoidal membership function
            # If peak_start == peak_end, it's a triangular function
            if b == c:
                # Use triangular membership
                membership = self.triangular_membership(value, a, b, d)
            else:
                # Use trapezoid membership
                membership = self.trapezoid_membership(value, a, b, c, d)
            
            result[set_name] = membership
        
        return result
    
    def fuzzify_all_inputs(self, volatilitas, volume, frekuensi, fuzzy_sets_config):
        """
        Fuzzifikasi semua input kriteria
        
        Parameters:
        - volatilitas: nilai volatilitas (selisih harga)
        - volume: nilai volume transaksi
        - frekuensi: nilai frekuensi transaksi
        - fuzzy_sets_config: dict berisi konfigurasi fuzzy sets untuk setiap variabel
          {
            'Volatilitas': [...],
            'Volume': [...],
            'Frekuensi': [...]
          }
        
        Returns:
        - dict: {
            'Volatilitas': {'Rendah': 0.5, 'Sedang': 0.3, 'Tinggi': 0.0},
            'Volume': {...},
            'Frekuensi': {...}
          }
        """
        result = {
            'Volatilitas': self.fuzzify_value(volatilitas, fuzzy_sets_config['Volatilitas']),
            'Volume': self.fuzzify_value(volume, fuzzy_sets_config['Volume']),
            'Frekuensi': self.fuzzify_value(frekuensi, fuzzy_sets_config['Frekuensi'])
        }
        
        return result
    
    def get_max_membership(self, fuzzy_values):
        """
        Mendapatkan himpunan dengan derajat keanggotaan tertinggi
        
        Parameters:
        - fuzzy_values: dict seperti {'Rendah': 0.5, 'Sedang': 0.3, 'Tinggi': 0.0}
        
        Returns:
        - tuple: (set_name, membership_value)
        """
        max_set = max(fuzzy_values, key=fuzzy_values.get)
        return (max_set, fuzzy_values[max_set])