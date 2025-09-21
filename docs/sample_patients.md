# Sample Patient Information for Stellest Lens Prediction Platform

## 📋 Patient Data Examples

### 🔬 **Sample Patient 1: High Success Probability**
```
Age: 12.0 years
Age at Myopia Diagnosis: 8.0 years
Gender: Female (2)
Family History of Myopia: Yes (1)
Outdoor Time: 2.5 hours/day
Screen Time: 3.0 hours/day
Previous Myopia Control: No (0)
Initial Power - Right Eye: -3.5 D
Initial Power - Left Eye: -3.25 D
Initial Axial Length - Right Eye: 24.5 mm
Initial Axial Length - Left Eye: 24.3 mm
Stellest Wearing Time: 15.0 hours/day
```
**Expected Result**: High probability of success (>80%)

---

### 🔬 **Sample Patient 2: Moderate Success Probability**
```
Age: 14.0 years
Age at Myopia Diagnosis: 10.0 years
Gender: Male (1)
Family History of Myopia: Yes (1)
Outdoor Time: 1.0 hours/day
Screen Time: 5.0 hours/day
Previous Myopia Control: Yes (1)
Initial Power - Right Eye: -5.0 D
Initial Power - Left Eye: -4.75 D
Initial Axial Length - Right Eye: 25.2 mm
Initial Axial Length - Left Eye: 25.0 mm
Stellest Wearing Time: 12.0 hours/day
```
**Expected Result**: Moderate probability of success (50-70%)

---

### 🔬 **Sample Patient 3: Lower Success Probability**
```
Age: 16.0 years
Age at Myopia Diagnosis: 6.0 years
Gender: Male (1)
Family History of Myopia: Yes (1)
Outdoor Time: 0.5 hours/day
Screen Time: 8.0 hours/day
Previous Myopia Control: No (0)
Initial Power - Right Eye: -7.0 D
Initial Power - Left Eye: -6.75 D
Initial Axial Length - Right Eye: 26.5 mm
Initial Axial Length - Left Eye: 26.3 mm
Stellest Wearing Time: 10.0 hours/day
```
**Expected Result**: Lower probability of success (30-50%)

---

### 🔬 **Sample Patient 4: Optimal Candidate**
```
Age: 10.0 years
Age at Myopia Diagnosis: 7.0 years
Gender: Female (2)
Family History of Myopia: No (0)
Outdoor Time: 3.0 hours/day
Screen Time: 2.0 hours/day
Previous Myopia Control: No (0)
Initial Power - Right Eye: -2.5 D
Initial Power - Left Eye: -2.25 D
Initial Axial Length - Right Eye: 23.8 mm
Initial Axial Length - Left Eye: 23.6 mm
Stellest Wearing Time: 16.0 hours/day
```
**Expected Result**: Very high probability of success (>90%)

---

### 🔬 **Sample Patient 5: High-Risk Case**
```
Age: 8.0 years
Age at Myopia Diagnosis: 4.0 years
Gender: Male (1)
Family History of Myopia: Yes (1)
Outdoor Time: 0.5 hours/day
Screen Time: 6.0 hours/day
Previous Myopia Control: Yes (1)
Initial Power - Right Eye: -4.0 D
Initial Power - Left Eye: -3.75 D
Initial Axial Length - Right Eye: 24.8 mm
Initial Axial Length - Left Eye: 24.6 mm
Stellest Wearing Time: 8.0 hours/day
```
**Expected Result**: High-risk case requiring intervention

---

## 📊 **Field Explanations**

### **Basic Information**
- **Age**: Current age in years (4-25 range)
- **Age at Myopia Diagnosis**: Age when myopia was first diagnosed (2-20 range)
- **Gender**: 1 = Male, 2 = Female

### **Family & Lifestyle**
- **Family History of Myopia**: 0 = No, 1 = Yes
- **Outdoor Time**: Hours per day spent outdoors (0-12 range)
- **Screen Time**: Hours per day of screen exposure (0-16 range)

### **Medical History**
- **Previous Myopia Control**: 0 = No previous treatment, 1 = Yes (atropine, vision therapy, etc.)

### **Clinical Measurements**
- **Initial Power**: Spherical equivalent in diopters (negative values, e.g., -3.5)
- **Initial Axial Length**: Eye length in millimeters (20-30 mm range)
- **Stellest Wearing Time**: Expected daily wearing hours (8-18 range)

---

## 🎯 **Quick Test Values for Web Form**

### **Minimal Test Case**
```
Age: 12
Age at Myopia Diagnosis: 8
Gender: Female
Family History: Yes
Outdoor Time: 2.0
Screen Time: 4.0
Previous Myopia Control: No
Right Eye Power: -3.5
Left Eye Power: -3.25
Right Eye Axial Length: 24.5
Left Eye Axial Length: 24.3
Stellest Wearing Time: 14.0
```

### **Copy-Paste Values (comma-separated)**
```
12.0, 8.0, 2, 1, 2.0, 4.0, 0, -3.5, -3.25, 24.5, 24.3, 14.0
```

---

## 💡 **Success Factors**

### **Positive Predictors**
- ✅ Young age at treatment start (8-12 years)
- ✅ Good compliance (≥14 hours/day)
- ✅ Adequate outdoor time (≥2 hours/day)
- ✅ Limited screen time (<4 hours/day)
- ✅ Moderate myopia (<5D)

### **Risk Factors**
- ⚠️ High myopia (>6D)
- ⚠️ Poor compliance (<10 hours/day)
- ⚠️ Excessive screen time (>6 hours/day)
- ⚠️ Very young age (<6 years)
- ⚠️ Insufficient outdoor time (<1 hour/day)

---

## 🔬 **Clinical Scenarios**

### **Scenario A: Ideal Candidate**
- 10-year-old with recent myopia onset
- Good lifestyle habits
- Excellent compliance expected
- **Prediction**: >90% success rate

### **Scenario B: Challenging Case**
- Teenager with high myopia
- Poor lifestyle factors
- Compliance concerns
- **Prediction**: Requires additional interventions

### **Scenario C: Early Intervention**
- Young child with progressive myopia
- Strong family history
- Good parental support
- **Prediction**: High success with proper monitoring

---

## 📱 **Using the Web Interface**

1. **Open**: http://localhost:8000
2. **Navigate**: To the "Prediction" tab
3. **Enter**: Any of the sample data above
4. **Click**: "Predict Stellest Lens Effectiveness"
5. **Review**: AI recommendations and risk factors

The platform will provide:
- 🎯 Treatment probability
- 📊 Confidence level
- 💡 Clinical recommendations
- ⚠️ Risk factor analysis
- 📈 Individual model predictions
