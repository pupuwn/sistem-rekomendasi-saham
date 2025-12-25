import numpy as np

class FuzzificationEngine:
    """
    Engine untuk melakukan Fuzzifikasi (Crisp to Fuzzy)
    Mengubah nilai numerik menjadi derajat keanggotaan fuzzy
    """
    
    @staticmethod
    def triangular_membership(x, a, b, c):
        """Fungsi keanggotaan Segitiga (Fixed)"""
        x, a, b, c = float(x), float(a), float(b), float(c)
        
        # UBAH DISINI: Gunakan '<' bukan '<=' untuk batas kiri
        if x < a or x > c:
            return 0.0
        elif a <= x < b:
            return (x - a) / (b - a)
        elif b <= x <= c:
            return (c - x) / (c - b)
        return 0.0
    
    @staticmethod
    def trapezoid_membership(x, a, b, c, d):
        """Fungsi keanggotaan Trapezoid (Fixed)"""
        x, a, b, c, d = float(x), float(a), float(b), float(c), float(d)
        
        # UBAH DISINI: Gunakan '<' bukan '<=' untuk batas kiri
        if x < a or x > d:
            return 0.0
        elif a <= x < b:
            return (x - a) / (b - a)
        # Menangani range puncak (Flat top)
        elif b <= x <= c:
            return 1.0
        elif c < x <= d:
            return (d - x) / (d - c)
        return 0.0
    
    def fuzzify_value(self, value, fuzzy_sets):
        """Fuzzifikasi nilai input terhadap semua himpunan fuzzy"""
        result = {}
        
        for fuzzy_set in fuzzy_sets:
            set_name = fuzzy_set['set_name']
            # Pastikan mengambil nilai sebagai float
            a = float(fuzzy_set['min_value'])
            d = float(fuzzy_set['max_value'])
            b = float(fuzzy_set['peak_start'])
            c = float(fuzzy_set['peak_end'])
            
            # Tentukan apakah Segitiga atau Trapesium
            if b == c:
                membership = self.triangular_membership(value, a, b, d)
            else:
                membership = self.trapezoid_membership(value, a, b, c, d)
            
            result[set_name] = membership
        
        return result
    
    def fuzzify_all_inputs(self, volatilitas, volume, frekuensi, fuzzy_sets_config):
        """Fuzzifikasi semua input kriteria"""
        result = {
            'Volatilitas': self.fuzzify_value(volatilitas, fuzzy_sets_config['Volatilitas']),
            'Volume': self.fuzzify_value(volume, fuzzy_sets_config['Volume']),
            'Frekuensi': self.fuzzify_value(frekuensi, fuzzy_sets_config['Frekuensi'])
        }
        return result