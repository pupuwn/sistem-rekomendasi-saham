import numpy as np

class InferenceEngine:
    """
    Engine untuk melakukan Inferensi Fuzzy menggunakan metode Tsukamoto
    Mengevaluasi aturan IF-THEN dan menghitung α-predikat & z secara dinamis
    """
    
    def __init__(self, rules, output_sets_config):
        """
        Parameters:
        - rules: list of dict berisi aturan fuzzy
        - output_sets_config: dict range output sets (Low_Risk: {min:70, max:100}, etc)
        """
        self.rules = rules
        self.output_sets = output_sets_config
    
    def calculate_alpha_predicate(self, fuzzy_inputs, rule):
        """Menghitung α-predikat menggunakan operator MIN (AND)"""
        # Ambil derajat keanggotaan (default 0 jika tidak ada)
        mu_volatilitas = fuzzy_inputs['Volatilitas'].get(rule['volatilitas_set'], 0.0)
        mu_volume = fuzzy_inputs['Volume'].get(rule['volume_set'], 0.0)
        mu_frekuensi = fuzzy_inputs['Frekuensi'].get(rule['frekuensi_set'], 0.0)
        
        # Pastikan float
        alpha = min(float(mu_volatilitas), float(mu_volume), float(mu_frekuensi))
        return alpha
    
    def calculate_z_tsukamoto(self, alpha, output_set_name):
        """
        Menghitung nilai z (crisp output) secara dinamis.
        Logika Tsukamoto:
        - Low_Risk (Positif/Bagus): Monoton Naik -> z = min + alpha * (max - min)
        - High_Risk (Negatif/Buruk): Monoton Turun -> z = max - alpha * (max - min)
        - Medium_Risk: Diasumsikan Monoton Naik untuk simplifikasi mapping ke skor
        """
        # Ambil konfigurasi range output
        config = self.output_sets.get(output_set_name)
        if not config:
            return 0.0
            
        min_val = float(config['min_value'])
        max_val = float(config['max_value'])
        range_val = max_val - min_val
        
        # --- LOGIKA PENENTUAN Z ---
        if output_set_name == 'High_Risk':
            # Kurva TURUN: Semakin High Risk (alpha=1), Skor semakin KECIL (mendekati 0)
            # Z = max - alpha * (max - min)
            z = max_val - (alpha * range_val)
        else:
            # Low_Risk & Medium_Risk
            # Kurva NAIK: Semakin Low Risk (alpha=1), Skor semakin BESAR (mendekati 100)
            # Z = min + alpha * (max - min)
            z = min_val + (alpha * range_val)
            
        return z
    
    def evaluate_all_rules(self, fuzzy_inputs):
        """Evaluasi semua aturan fuzzy"""
        results = []
        
        for rule in self.rules:
            # 1. Hitung α-predikat
            alpha = self.calculate_alpha_predicate(fuzzy_inputs, rule)
            
            # 2. Jika α > 0, rule aktif
            if alpha > 0:
                output_set = rule['output_set']
                
                # 3. Hitung z secara dinamis (bukan dari DB z_value lagi)
                z = self.calculate_z_tsukamoto(alpha, output_set)
                
                results.append({
                    'rule_id': rule.get('id', 0),
                    'rule_name': rule.get('rule_name', ''),
                    'alpha': alpha,
                    'z': z,
                    'output_set': output_set
                })
        
        return results

    def get_fired_rules_summary(self, inference_results):
        """Mendapatkan ringkasan aturan yang aktif"""
        total_rules = len(self.rules)
        fired_rules = len(inference_results)
        
        return {
            'total_rules': total_rules,
            'fired_rules': fired_rules,
            'firing_rate': (fired_rules / total_rules * 100) if total_rules > 0 else 0
        }