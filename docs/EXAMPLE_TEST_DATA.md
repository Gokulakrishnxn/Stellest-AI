# 🧪 **Example Test Data for AI Prediction**

## 📊 **Sample Patient Data for Testing**

### **✅ Example 1: High Success Probability Patient**

```json
{
    "patient_name": "Emma Johnson",
    "age": 10,
    "age_myopia_diagnosis": 7,
    "gender": 2,
    "family_history_myopia": 0,
    "outdoor_time": 3.5,
    "screen_time": 2.0,
    "previous_myopia_control": 0,
    "initial_power_re": -1.5,
    "initial_power_le": -1.25,
    "initial_axial_length_re": 22.8,
    "initial_axial_length_le": 22.7,
    "stellest_wearing_time": 14.0
}
```

**Expected Result**: High probability of success (likely >70%)

### **⚠️ Example 2: Medium Success Probability Patient**

```json
{
    "patient_name": "Michael Chen",
    "age": 14,
    "age_myopia_diagnosis": 9,
    "gender": 1,
    "family_history_myopia": 1,
    "outdoor_time": 1.5,
    "screen_time": 6.0,
    "previous_myopia_control": 1,
    "initial_power_re": -3.5,
    "initial_power_le": -3.25,
    "initial_axial_length_re": 24.2,
    "initial_axial_length_le": 24.1,
    "stellest_wearing_time": 10.0
}
```

**Expected Result**: Medium probability of success (likely 40-70%)

### **❌ Example 3: Low Success Probability Patient**

```json
{
    "patient_name": "Sarah Williams",
    "age": 16,
    "age_myopia_diagnosis": 6,
    "gender": 2,
    "family_history_myopia": 1,
    "outdoor_time": 0.5,
    "screen_time": 8.0,
    "previous_myopia_control": 1,
    "initial_power_re": -5.5,
    "initial_power_le": -5.25,
    "initial_axial_length_re": 25.8,
    "initial_axial_length_le": 25.7,
    "stellest_wearing_time": 8.0
}
```

**Expected Result**: Low probability of success (likely <40%)

## 🧪 **How to Test the AI Prediction**

### **Method 1: Using the Website Form**

1. **Open**: http://localhost:8000
2. **Fill in the form** with any of the example data above
3. **Click**: "Predict Treatment Effectiveness"
4. **Check the results** for:
   - Patient name display
   - Probability percentage
   - Confidence level
   - Recommendation text
   - Individual model results
   - Risk factors analysis

### **Method 2: Using API Directly**

#### **Test Example 1 (High Success)**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Emma Johnson",
    "age": 10,
    "age_myopia_diagnosis": 7,
    "gender": 2,
    "family_history_myopia": 0,
    "outdoor_time": 3.5,
    "screen_time": 2.0,
    "previous_myopia_control": 0,
    "initial_power_re": -1.5,
    "initial_power_le": -1.25,
    "initial_axial_length_re": 22.8,
    "initial_axial_length_le": 22.7,
    "stellest_wearing_time": 14.0
  }'
```

#### **Test Example 2 (Medium Success)**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Michael Chen",
    "age": 14,
    "age_myopia_diagnosis": 9,
    "gender": 1,
    "family_history_myopia": 1,
    "outdoor_time": 1.5,
    "screen_time": 6.0,
    "previous_myopia_control": 1,
    "initial_power_re": -3.5,
    "initial_power_le": -3.25,
    "initial_axial_length_re": 24.2,
    "initial_axial_length_le": 24.1,
    "stellest_wearing_time": 10.0
  }'
```

#### **Test Example 3 (Low Success)**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Sarah Williams",
    "age": 16,
    "age_myopia_diagnosis": 6,
    "gender": 2,
    "family_history_myopia": 1,
    "outdoor_time": 0.5,
    "screen_time": 8.0,
    "previous_myopia_control": 1,
    "initial_power_re": -5.5,
    "initial_power_le": -5.25,
    "initial_axial_length_re": 25.8,
    "initial_axial_length_le": 25.7,
    "stellest_wearing_time": 8.0
  }'
```

## 🔍 **What to Look For in Results**

### **✅ Successful Prediction Response Should Include:**

```json
{
    "patient_name": "Emma Johnson",
    "ensemble_prediction": {
        "will_benefit": true,
        "probability": 0.85,
        "confidence": "High"
    },
    "individual_models": {
        "Random Forest": {
            "probability": 0.82,
            "prediction": 1,
            "confidence": "High"
        },
        "Gradient Boosting": {
            "probability": 0.88,
            "prediction": 1,
            "confidence": "High"
        }
        // ... other models
    },
    "risk_factors": {
        "age": -0.15,
        "family_history_myopia": 0.25,
        "screen_time": -0.30
        // ... other factors
    },
    "recommendation": "Patient shows excellent potential for Stellest lens treatment...",
    "patient_id": "patient_20241222_123456",
    "timestamp": "2024-12-22T12:34:56",
    "processing_time": 0.023
}
```

### **🎯 Key Indicators of Working AI:**

1. **Patient Name**: Should appear in results
2. **Probability**: Should be between 0.0 and 1.0
3. **Confidence**: Should be "High", "Medium", or "Low"
4. **Individual Models**: Should show 4-6 different ML models
5. **Risk Factors**: Should show numerical impact values
6. **Processing Time**: Should be <1 second
7. **Recommendation**: Should be a meaningful text response

## 🚨 **Troubleshooting**

### **If You Get Errors:**

#### **422 Unprocessable Entity**
- Check all required fields are filled
- Ensure numeric fields are numbers, not strings
- Verify field names match exactly

#### **500 Internal Server Error**
- Check if the AI model is loaded
- Verify the server is running
- Check server logs for details

#### **No Results Displayed**
- Check browser console for JavaScript errors
- Verify the API response format
- Ensure the form validation passes

## 📊 **Expected Results by Example**

### **Example 1 (Emma - High Success)**
- **Probability**: 75-95%
- **Confidence**: High
- **Recommendation**: Strong positive recommendation
- **Risk Factors**: Low risk factors, positive indicators

### **Example 2 (Michael - Medium Success)**
- **Probability**: 40-70%
- **Confidence**: Medium
- **Recommendation**: Cautious recommendation
- **Risk Factors**: Mixed risk factors

### **Example 3 (Sarah - Low Success)**
- **Probability**: 20-50%
- **Confidence**: Medium/Low
- **Recommendation**: Alternative treatments suggested
- **Risk Factors**: High risk factors

## 🎯 **Quick Test Commands**

### **Test API Health**
```bash
curl -s "http://localhost:8000/health" | jq '.status'
# Should return: "healthy"
```

### **Test Model Info**
```bash
curl -s "http://localhost:8000/model_info" | jq '.model_name'
# Should return: "Stellest AI Ensemble"
```

### **Test Simple Prediction**
```bash
curl -s -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"patient_name": "Test Patient", "age": 12, "age_myopia_diagnosis": 8, "gender": 1, "family_history_myopia": 0, "outdoor_time": 2.0, "screen_time": 4.0, "previous_myopia_control": 0, "initial_power_re": -2.0, "initial_power_le": -2.0, "initial_axial_length_re": 23.0, "initial_axial_length_le": 23.0, "stellest_wearing_time": 12.0}' | jq '.ensemble_prediction.probability'
```

---

## 🎊 **Ready to Test!**

Use any of the example data above to verify your AI prediction system is working correctly. The examples are designed to show different probability ranges, so you can see how the AI responds to various patient profiles.

**🌐 Test URL**: http://localhost:8000
**🧪 API Endpoint**: http://localhost:8000/predict
