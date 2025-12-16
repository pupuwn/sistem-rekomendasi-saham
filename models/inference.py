import numpy as np

class InferenceEngine:
    """
    Engine untuk melakukan Inferensi Fuzzy menggunakan metode Tsukamoto
    Mengevaluasi aturan IF-THEN dan menghitung α-predikat & z
    """
    
    def __init__(self, rules):
        """
        Parameters:
        - rules: list of dict berisi aturan fuzzy
          [
            {
              'id': 1,
              'rule_name': 'R1',
              'volatilitas_set': 'Rendah',
              'volume_set': 'Tinggi',
              'frekuensi_set': 'Tinggi',
              'output_set': 'Low_Risk',
              'z_value': 40.0  # Nilai z spesifik untuk setiap aturan
            },
            ...
          ]
        """
        self.rules = rules
        # Output sets tidak lagi diperlukan karena z sudah ditentukan per aturan
    
    def calculate_alpha_predicate(self, fuzzy_inputs, rule):
        """
        Menghitung α-predikat menggunakan operator MIN (AND)
        
        Parameters:
        - fuzzy_inputs: hasil fuzzifikasi
          {
            'Volatilitas': {'Rendah': 0.5, 'Sedang': 0.3, 'Tinggi': 0.0},
            'Volume': {...},
            'Frekuensi': {...}
          }
        - rule: dict aturan tunggal
        
        Returns:
        - float: nilai α-predikat (0-1)
        """
        # Ambil derajat keanggotaan untuk setiap antecedent
        mu_volatilitas = fuzzy_inputs['Volatilitas'].get(rule['volatilitas_set'], 0)
        mu_volume = fuzzy_inputs['Volume'].get(rule['volume_set'], 0)
        mu_frekuensi = fuzzy_inputs['Frekuensi'].get(rule['frekuensi_set'], 0)
        
        # Operator AND = MIN
        alpha = min(mu_volatilitas, mu_volume, mu_frekuensi)
        
        return alpha
    
    def calculate_z_tsukamoto(self, alpha, rule):
        """
        Menghitung nilai z (crisp output) menggunakan metode Tsukamoto.
        Pada implementasi ini, nilai z diambil langsung dari definisi aturan (z_value).
        
        Parameters:
        - alpha: nilai α-predikat (tidak digunakan dalam perhitungan z ini, tapi dipertahankan untuk konsistensi)
        - rule: dict aturan tunggal yang sudah termasuk z_value
        
        Returns:
        - float: nilai z (crisp)
        """
        # Nilai z sudah ditentukan per aturan dalam database
        return rule.get('z_value', 0.0)
    
    def evaluate_all_rules(self, fuzzy_inputs):
        """
        Evaluasi semua aturan fuzzy
        
        Parameters:
        - fuzzy_inputs: hasil fuzzifikasi dari semua input
        
        Returns:
        - list of dict: [
            {
              'rule_id': 1,
              'rule_name': 'R1',
              'alpha': 0.5,
              'z': 40.0,
              'output_set': 'Low_Risk'
            },
            ...
          ]
        """
        results = []
        
        for rule in self.rules:
            # Hitung α-predikat
            alpha = self.calculate_alpha_predicate(fuzzy_inputs, rule)
            
            # Jika α > 0, rule aktif, hitung z
            if alpha > 0:
                # Kirim seluruh objek 'rule' ke fungsi calculate_z_tsukamoto
                z = self.calculate_z_tsukamoto(alpha, rule)
                
                results.append({
                    'rule_id': rule.get('id', 0),
                    'rule_name': rule.get('rule_name', ''),
                    'alpha': alpha,
                    'z': z,
                    'output_set': rule['output_set']
                })
        
        return results
    
    def get_fired_rules_summary(self, inference_results):
        """
        Mendapatkan ringkasan aturan yang aktif (fired)
        
        Parameters:
        - inference_results: hasil dari evaluate_all_rules()
        
        Returns:
        - dict: statistik aturan yang aktif
        """
        total_rules = len(self.rules)
        fired_rules = len(inference_results)
        
        return {
            'total_rules': total_rules,
            'fired_rules': fired_rules,
            'firing_rate': (fired_rules / total_rules * 100) if total_rules > 0 else 0
        }
