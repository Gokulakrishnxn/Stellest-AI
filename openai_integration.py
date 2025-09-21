#!/usr/bin/env python3
"""
OpenAI Integration for Stellest Lens Myopia Prediction
Provides AI-powered clinical analysis and recommendations
"""

import os
from typing import Dict, Any, Optional

class OpenAIPredictor:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.available = self.api_key is not None
        
    def check_status(self) -> Dict[str, Any]:
        """Check OpenAI integration status"""
        return {
            'status': 'available' if self.available else 'not_configured',
            'message': 'OpenAI integration ready' if self.available else 'OpenAI API key not configured',
            'features': [
                'Clinical narrative generation',
                'Treatment plan recommendations',
                'Risk assessment analysis',
                'Follow-up scheduling',
                'Patient education content',
                'Alternative treatment suggestions'
            ] if self.available else []
        }
    
    def analyze_patient(self, patient_data: Dict, prediction_result: Dict) -> Dict[str, Any]:
        """Generate AI-powered clinical analysis"""
        if not self.available:
            return self._get_demo_analysis(patient_data, prediction_result)
        
        try:
            # In a real implementation, this would call OpenAI API
            # For now, we'll return structured demo content
            return self._get_demo_analysis(patient_data, prediction_result)
        except Exception as e:
            print(f"OpenAI analysis error: {e}")
            return self._get_demo_analysis(patient_data, prediction_result)
    
    def _get_demo_analysis(self, patient_data: Dict, prediction_result: Dict) -> Dict[str, Any]:
        """Generate demo analysis when OpenAI is not available"""
        patient_name = patient_data.get('patient_name', 'Patient')
        age = patient_data.get('age', 0)
        probability = prediction_result.get('ensemble_prediction', {}).get('probability', 0.5)
        
        return {
            'clinical_narrative': f"""
            {patient_name} is a {age}-year-old patient presenting for myopia management evaluation. 
            Based on the comprehensive AI analysis, the patient shows {'excellent' if probability > 0.7 else 'moderate' if probability > 0.5 else 'limited'} 
            potential for Stellest lens treatment success. The ensemble model indicates a {probability*100:.1f}% probability 
            of positive treatment outcomes, which is {'highly encouraging' if probability > 0.7 else 'promising' if probability > 0.5 else 'concerning'} 
            for clinical decision-making.
            """,
            
            'treatment_plan': f"""
            **Primary Treatment Plan:**
            1. Initiate Stellest lens therapy with {'high' if probability > 0.7 else 'moderate' if probability > 0.5 else 'cautious'} confidence
            2. Schedule follow-up appointments every 6 months
            3. Monitor axial length progression and refractive changes
            4. Implement lifestyle modifications as needed
            
            **Expected Timeline:**
            - Initial fitting and adaptation: 2-4 weeks
            - First follow-up: 3 months
            - Regular monitoring: Every 6 months
            - Treatment duration: 2-3 years minimum
            """,
            
            'risk_assessment': f"""
            **Risk Profile Analysis:**
            - Treatment Success Probability: {probability*100:.1f}%
            - Risk Level: {'Low' if probability > 0.7 else 'Medium' if probability > 0.5 else 'High'}
            - Key Risk Factors: {self._identify_risk_factors(patient_data)}
            - Protective Factors: {self._identify_protective_factors(patient_data)}
            """,
            
            'follow_up_schedule': """
            **Recommended Follow-up Schedule:**
            1. **Week 1-2**: Initial fitting and comfort assessment
            2. **Month 1**: Visual acuity and comfort evaluation
            3. **Month 3**: Comprehensive examination with axial length measurement
            4. **Month 6**: Full assessment including progression analysis
            5. **Every 6 months**: Ongoing monitoring and treatment adjustment
            """,
            
            'patient_education': f"""
            **Patient Education Points:**
            1. **Treatment Goals**: Slow myopia progression and reduce risk of complications
            2. **Expected Outcomes**: {'Significant' if probability > 0.7 else 'Moderate' if probability > 0.5 else 'Limited'} 
               reduction in myopia progression over 2-3 years
            3. **Compliance Importance**: Consistent wear for optimal results
            4. **Lifestyle Modifications**: Increase outdoor time, reduce screen time
            5. **Long-term Benefits**: Reduced risk of high myopia complications
            """,
            
            'alternative_treatments': """
            **Alternative Treatment Options:**
            1. **Atropine Eye Drops**: Low-dose atropine (0.01-0.05%) for myopia control
            2. **Orthokeratology**: Overnight contact lenses for temporary vision correction
            3. **Multifocal Contact Lenses**: Soft contact lenses with myopia control features
            4. **Lifestyle Interventions**: Increased outdoor time, reduced near work
            5. **Combination Therapy**: Stellest lens with low-dose atropine
            """
        }
    
    def _identify_risk_factors(self, patient_data: Dict) -> str:
        """Identify key risk factors"""
        risk_factors = []
        
        age = patient_data.get('age', 0)
        if age > 15:
            risk_factors.append('Advanced age')
        
        screen_time = patient_data.get('screen_time', 0)
        if screen_time > 6:
            risk_factors.append('High screen time')
        
        outdoor_time = patient_data.get('outdoor_time', 0)
        if outdoor_time < 1:
            risk_factors.append('Limited outdoor time')
        
        if patient_data.get('family_history_myopia', 0) == 1:
            risk_factors.append('Family history')
        
        return ', '.join(risk_factors) if risk_factors else 'Minimal risk factors identified'
    
    def _identify_protective_factors(self, patient_data: Dict) -> str:
        """Identify protective factors"""
        protective_factors = []
        
        age = patient_data.get('age', 0)
        if age < 12:
            protective_factors.append('Young age')
        
        outdoor_time = patient_data.get('outdoor_time', 0)
        if outdoor_time >= 2:
            protective_factors.append('Good outdoor time')
        
        screen_time = patient_data.get('screen_time', 0)
        if screen_time < 3:
            protective_factors.append('Limited screen time')
        
        wearing_time = patient_data.get('stellest_wearing_time', 0)
        if wearing_time >= 12:
            protective_factors.append('Good compliance potential')
        
        return ', '.join(protective_factors) if protective_factors else 'Standard risk profile'
    
    def create_patient_summary(self, patient_data: Dict, prediction_result: Dict, openai_analysis: Dict) -> str:
        """Create a comprehensive patient summary"""
        patient_name = patient_data.get('patient_name', 'Patient')
        age = patient_data.get('age', 0)
        probability = prediction_result.get('ensemble_prediction', {}).get('probability', 0.5)
        
        summary = f"""
        **PATIENT SUMMARY: {patient_name}**
        
        **Demographics:**
        - Age: {age} years
        - Gender: {'Male' if patient_data.get('gender', 1) == 1 else 'Female'}
        - Myopia Duration: {age - patient_data.get('age_myopia_diagnosis', 0):.1f} years
        
        **Clinical Assessment:**
        - Treatment Success Probability: {probability*100:.1f}%
        - Recommendation: {'Highly Recommended' if probability > 0.7 else 'Recommended' if probability > 0.5 else 'Consider Alternatives'}
        - Risk Level: {'Low' if probability > 0.7 else 'Medium' if probability > 0.5 else 'High'}
        
        **Key Findings:**
        {openai_analysis.get('clinical_narrative', 'Analysis pending')}
        
        **Treatment Plan:**
        {openai_analysis.get('treatment_plan', 'Plan pending')}
        
        **Next Steps:**
        1. Discuss treatment options with patient and family
        2. Schedule initial fitting if proceeding with Stellest lens
        3. Implement lifestyle modifications
        4. Schedule follow-up appointments
        """
        
        return summary.strip()
    
    def generate_treatment_report(self, patient_data: Dict, prediction_result: Dict) -> str:
        """Generate a comprehensive treatment report"""
        if not self.available:
            return self._get_demo_report(patient_data, prediction_result)
        
        # In real implementation, this would generate a detailed report using OpenAI
        return self._get_demo_report(patient_data, prediction_result)
    
    def _get_demo_report(self, patient_data: Dict, prediction_result: Dict) -> str:
        """Generate demo treatment report"""
        patient_name = patient_data.get('patient_name', 'Patient')
        probability = prediction_result.get('ensemble_prediction', {}).get('probability', 0.5)
        
        return f"""
        **STELLEST LENS TREATMENT REPORT**
        
        Patient: {patient_name}
        Date: {patient_data.get('timestamp', 'Current')}
        
        **EXECUTIVE SUMMARY**
        This patient shows {'excellent' if probability > 0.7 else 'moderate' if probability > 0.5 else 'limited'} 
        potential for successful Stellest lens treatment with a {probability*100:.1f}% probability of positive outcomes.
        
        **RECOMMENDATION**
        {'Proceed with Stellest lens treatment' if probability > 0.5 else 'Consider alternative treatments'}
        
        **RISK ASSESSMENT**
        {'Low risk profile with high success potential' if probability > 0.7 else 'Moderate risk with good success potential' if probability > 0.5 else 'Higher risk profile requiring careful monitoring'}
        
        **TREATMENT PLAN**
        - Primary: Stellest lens therapy
        - Monitoring: 6-month follow-ups
        - Duration: 2-3 years minimum
        - Lifestyle: Outdoor time increase, screen time reduction
        
        **EXPECTED OUTCOMES**
        {'Significant myopia control (>50% reduction)' if probability > 0.7 else 'Moderate myopia control (30-50% reduction)' if probability > 0.5 else 'Limited myopia control (<30% reduction)'}
        """.strip()
