# 🌐 How to See Output on Your Website

## 🚨 **"422 Unprocessable Entity" Error Explained**

**What it means**: The form is missing required fields or has invalid data.

**Why it happens**: All 12 patient information fields must be completely filled in.

---

## ✅ **3 Ways to See Website Output**

### **Method 1: Test Page (Easiest)**
1. **Open**: http://localhost:8000/test
2. **Pre-filled form** with sample data
3. **Click "Test Prediction"**
4. **See immediate output** with detailed error messages

### **Method 2: Main Website**
1. **Open**: http://localhost:8000
2. **Fill ALL 12 fields** in the form
3. **Click "Predict Stellest Lens Effectiveness"**
4. **View comprehensive results**

### **Method 3: API Direct Test**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 12.0,
    "age_myopia_diagnosis": 8.0,
    "gender": 2,
    "family_history_myopia": 1,
    "outdoor_time": 1.5,
    "screen_time": 4.0,
    "previous_myopia_control": 0,
    "initial_power_re": -3.5,
    "initial_power_le": -3.25,
    "initial_axial_length_re": 24.5,
    "initial_axial_length_le": 24.3,
    "stellest_wearing_time": 14.0
  }'
```

---

## 📝 **Required Fields Checklist**

Make sure ALL these fields are filled:

✅ **Basic Info**
- [ ] Age (4-25 years)
- [ ] Age at Myopia Diagnosis (2-20 years)
- [ ] Gender (Male=1, Female=2)
- [ ] Family History of Myopia (No=0, Yes=1)

✅ **Lifestyle**
- [ ] Outdoor Time (0-12 hours/day)
- [ ] Screen Time (0-16 hours/day)
- [ ] Previous Myopia Control (No=0, Yes=1)

✅ **Clinical Measurements**
- [ ] Initial Power - Right Eye (negative values like -3.5)
- [ ] Initial Power - Left Eye (negative values like -3.25)
- [ ] Initial Axial Length - Right Eye (20-30 mm)
- [ ] Initial Axial Length - Left Eye (20-30 mm)
- [ ] Stellest Wearing Time (8-18 hours/day)

---

## 🎯 **Expected Website Output**

When you successfully submit the form, you'll see:

### **🎉 Main Prediction Results**
```
✅ High Likelihood of Success
📊 Success Probability: 96.0%
🎯 Confidence Level: High
💡 Recommendation: Highly recommended for Stellest lens treatment
```

### **⚠️ Risk Analysis**
```
🟡 Medium Risk Factors:
• Moderate myopia (3-6D)
• Family history of myopia
• High screen time (3-6 hours/day)

✅ Protective Factors:
• Excellent compliance (≥14 hours/day)
```

### **🤖 AI Model Results**
```
Random Forest:      90.7% (High confidence)
Gradient Boosting:  100.0% (High confidence)
Logistic Regression: 100.0% (High confidence)
SVM:               93.3% (High confidence)
```

### **📈 Enhanced Analytics**
```
Risk Profile: Low Risk (2/10 score)
Population Comparison:
• Age: 49th percentile
• Myopia Severity: 55th percentile
• Screen Time: 96th percentile (HIGH)
• Outdoor Time: 90th percentile (needs improvement)
```

### **📋 Clinical Recommendations**
```
Primary Treatment:
• Stellest lens is highly recommended as first-line therapy

Lifestyle Modification:
• Increase outdoor time from 1.5 to ≥2 hours/day

Monitoring:
• Schedule 6-month follow-ups with axial length measurement
```

---

## 🔧 **Quick Fix for 422 Error**

### **Step 1: Use the Test Page**
```
http://localhost:8000/test
```
This page has pre-filled sample data and will show you exactly what's being sent to the API.

### **Step 2: Check All Fields**
Make sure every field in the form has a value:
- No empty fields
- All dropdowns selected
- All numbers within valid ranges

### **Step 3: Common Field Issues**
- **Gender**: Must select "Male" or "Female" (not empty)
- **Family History**: Must select "Yes" or "No" (not empty)
- **Previous Control**: Must select "Yes" or "No" (not empty)
- **Power values**: Must be negative (e.g., -3.5, not 3.5)
- **Age ranges**: Age 4-25, Diagnosis age 2-20

---

## 🌐 **Live Website Links**

- **🏠 Main Website**: http://localhost:8000
- **🧪 Test Page**: http://localhost:8000/test
- **📚 API Docs**: http://localhost:8000/docs
- **🔍 Health Check**: http://localhost:8000/health

---

## 💡 **Pro Tips for Getting Output**

1. **Start with Test Page**: http://localhost:8000/test (pre-filled data)
2. **Copy Sample Values**: Use the sample patient data provided
3. **Check Browser Console**: F12 → Console tab for JavaScript errors
4. **Verify Server**: Check terminal for any error messages
5. **Use API Docs**: http://localhost:8000/docs for interactive testing

---

## 🎊 **Your Output Will Include**

✅ **Treatment Recommendation** (Will Benefit / May Not Benefit)
✅ **Success Probability** (0-100%)
✅ **Confidence Level** (High/Medium/Low)
✅ **Risk Factor Analysis** (High/Medium/Protective)
✅ **Individual Model Results** (4 AI models)
✅ **Population Comparison** (percentiles)
✅ **Clinical Recommendations** (evidence-based)
✅ **Follow-up Protocols** (monitoring schedule)
✅ **Patient Education** (lifestyle advice)

**🚀 Go to http://localhost:8000/test to see immediate output with sample data!**
