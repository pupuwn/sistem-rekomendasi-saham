import numpy as np

class DefuzzificationEngine:
    """
    Engine untuk melakukan Defuzzifikasi (Fuzzy to Crisp)
    Mengubah hasil inferensi fuzzy menjadi nilai crisp menggunakan Weighted Average
    """
    
    @staticmethod
    def weighted_average(inference_results):
        """
        Metode Weighted Average (Rata-rata Tertimbang) untuk Defuzzifikasi
        
        Formula Tsukamoto:
        Z* = (Σ(αi × zi)) / Σ(αi)
        
        Parameters:
        - inference_results: list of dict dari InferenceEngine.evaluate_all_rules()
          [
            {'rule_id': 1, 'alpha': 0.8, 'z': 85.0, 'output_set': 'Low_Risk'},
            {'rule_id': 2, 'alpha': 0.5, 'z': 50.0, 'output_set': 'Medium_Risk'},
            ...
          ]
        
        Returns:
        - float: nilai crisp akhir (Z*)
        """
        if not inference_results:
            return 0.0
        
        # Hitung pembilang: Σ(αi × zi)
        numerator = sum(result['alpha'] * result['z'] for result in inference_results)
        
        # Hitung penyebut: Σ(αi)
        denominator = sum(result['alpha'] for result in inference_results)
        
        # Hindari pembagian dengan nol
        if denominator == 0:
            return 0.0
        
        # Hitung Z*
        z_star = numerator / denominator
        
        return z_star
    
    @staticmethod
    def get_risk_category(score):
        """
        Menentukan kategori risiko berdasarkan skor akhir
        
        Parameters:
        - score: nilai skor akhir (0-100)
        
        Returns:
        - str: 'Low Risk', 'Medium Risk', atau 'High Risk'
        """
        if score >= 70:
            return 'Low Risk'
        elif score >= 40:
            return 'Medium Risk'
        else:
            return 'High Risk'
    
    @staticmethod
    def get_risk_label(score):
        """
        Mendapatkan label risiko dengan emoji
        
        Parameters:
        - score: nilai skor akhir (0-100)
        
        Returns:
        - str: label dengan emoji
        """
        category = DefuzzificationEngine.get_risk_category(score)
        
        if category == 'Low Risk':
            return '🟢 Low Risk'
        elif category == 'Medium Risk':
            return '🟡 Medium Risk'
        else:
            return '🔴 High Risk'
    
    @staticmethod
    def calculate_confidence(inference_results):
        """
        Menghitung tingkat kepercayaan hasil berdasarkan jumlah rules yang aktif
        
        Parameters:
        - inference_results: list of dict dari InferenceEngine.evaluate_all_rules()
        
        Returns:
        - float: confidence score (0-1)
        """
        if not inference_results:
            return 0.0
        
        # Confidence berdasarkan rata-rata alpha
        avg_alpha = sum(r['alpha'] for r in inference_results) / len(inference_results)
        
        return avg_alpha
    
    def defuzzify_with_details(self, inference_results):
        """
        Defuzzifikasi dengan informasi detail
        
        Parameters:
        - inference_results: hasil dari InferenceEngine.evaluate_all_rules()
        
        Returns:
        - dict: {
            'final_score': 85.5,
            'risk_category': 'Low Risk',
            'confidence': 0.75,
            'active_rules': 5,
            'calculation_details': [...]
          }
        """
        # Hitung skor akhir
        final_score = self.weighted_average(inference_results)
        
        # Tentukan kategori risiko
        risk_category = self.get_risk_category(final_score)
        
        # Hitung confidence
        confidence = self.calculate_confidence(inference_results)
        
        # Detail perhitungan
        calculation_details = []
        for i, result in enumerate(inference_results, 1):
            calculation_details.append({
                'step': i,
                'rule': result.get('rule_name', f"R{result['rule_id']}"),
                'alpha': result['alpha'],
                'z': result['z'],
                'contribution': result['alpha'] * result['z']
            })
        
        return {
            'final_score': round(final_score, 2),
            'risk_category': risk_category,
            'confidence': round(confidence, 3),
            'active_rules': len(inference_results),
            'calculation_details': calculation_details
        }
    
    @staticmethod
    def format_calculation_table(defuzz_result):
        """
        Format hasil perhitungan dalam bentuk tabel string untuk display
        
        Parameters:
        - defuzz_result: hasil dari defuzzify_with_details()
        
        Returns:
        - str: tabel formatted
        """
        output = []
        output.append("=" * 60)
        output.append("DETAIL PERHITUNGAN DEFUZZIFIKASI")
        output.append("=" * 60)
        output.append(f"{'Rule':<10} {'Alpha':<10} {'Z':<10} {'α × z':<15}")
        output.append("-" * 60)
        
        for detail in defuzz_result['calculation_details']:
            output.append(
                f"{detail['rule']:<10} "
                f"{detail['alpha']:<10.3f} "
                f"{detail['z']:<10.2f} "
                f"{detail['contribution']:<15.2f}"
            )
        
        output.append("=" * 60)
        
        # Hitung total
        total_alpha = sum(d['alpha'] for d in defuzz_result['calculation_details'])
        total_contribution = sum(d['contribution'] for d in defuzz_result['calculation_details'])
        
        output.append(f"{'TOTAL':<10} {total_alpha:<10.3f} {'':<10} {total_contribution:<15.2f}")
        output.append("")
        output.append(f"Z* = {total_contribution:.2f} / {total_alpha:.3f} = {defuzz_result['final_score']:.2f}")
        output.append("")
        output.append(f"Kategori Risiko: {defuzz_result['risk_category']}")
        output.append(f"Confidence Level: {defuzz_result['confidence']:.1%}")
        output.append("=" * 60)
        
        return "\n".join(output)


# Contoh penggunaan
if __name__ == "__main__":
    # Contoh inference results
    inference_results = [
        {'rule_id': 1, 'rule_name': 'R1', 'alpha': 0.8, 'z': 90.0, 'output_set': 'Low_Risk'},
        {'rule_id': 2, 'rule_name': 'R2', 'alpha': 0.5, 'z': 75.0, 'output_set': 'Low_Risk'},
        {'rule_id': 3, 'rule_name': 'R3', 'alpha': 0.3, 'z': 50.0, 'output_set': 'Medium_Risk'}
    ]
    
    # Test defuzzifikasi
    defuzz = DefuzzificationEngine()
    
    # Simple calculation
    final_score = defuzz.weighted_average(inference_results)
    print(f"Skor Akhir: {final_score:.2f}")
    print(f"Kategori: {defuzz.get_risk_category(final_score)}")
    print()
    
    # Detailed calculation
    result = defuzz.defuzzify_with_details(inference_results)
    print(defuzz.format_calculation_table(result))
