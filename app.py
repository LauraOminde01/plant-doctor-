import streamlit as st
import tensorflow as tf
import numpy as np
import json
import os
from PIL import Image

st.set_page_config(
    page_title="AI Crop Doctor Kenya",
    layout="wide"
)

DISEASE_INFO = {
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
        'english_name': 'Maize Gray Leaf Spot',
        'swahili_name': 'Ugonjwa wa Madoa ya Kijivu (Mahindi)',
        'severity': 'High',
        'description': 'Fungal disease causing rectangular gray-brown lesions on maize leaves.',
        'treatment': [
            'Apply fungicides containing strobilurin or triazole compounds',
            'Plant resistant maize varieties (e.g., DK8031, H614D)',
            'Practice crop rotation — avoid planting maize consecutively',
            'Remove and destroy infected crop residue after harvest',
            'Ensure adequate spacing between plants for air circulation'
        ],
        'prevention': 'Use certified disease-resistant seeds. Avoid overhead irrigation.',
        'urgency': 'Act within 1-2 weeks of first signs'
    },
    'Corn_(maize)___Common_rust_': {
        'english_name': 'Maize Common Rust',
        'swahili_name': 'Kutu ya Mahindi',
        'severity': 'Medium',
        'description': 'Fungal disease producing powdery orange-brown pustules on maize leaves.',
        'treatment': [
            'Apply fungicides early — mancozeb or copper-based fungicides',
            'Plant rust-resistant hybrid varieties',
            'Early planting helps avoid peak rust season',
            'Remove severely infected plants to reduce spread'
        ],
        'prevention': 'Monitor fields regularly during wet, humid weather.',
        'urgency': 'Act within 2-3 weeks of first signs'
    },
    'Corn_(maize)___Northern_Leaf_Blight': {
        'english_name': 'Maize Northern Leaf Blight',
        'swahili_name': 'Ugonjwa wa Majani ya Mahindi',
        'severity': 'High',
        'description': 'Fungal disease causing large cigar-shaped gray-green lesions on maize leaves.',
        'treatment': [
            'Apply fungicides containing propiconazole or azoxystrobin',
            'Plant blight-resistant hybrid varieties from KALRO',
            'Practice crop rotation with non-maize crops',
            'Remove and burn infected plant debris',
            'Avoid excessive nitrogen fertilizer'
        ],
        'prevention': 'Use certified seeds. Ensure proper drainage.',
        'urgency': 'Act within 1 week — spreads rapidly'
    },
    'Corn_(maize)___healthy': {
        'english_name': 'Healthy Maize',
        'swahili_name': 'Mahindi Yenye Afya',
        'severity': 'None',
        'description': 'Your maize crop appears healthy. No disease detected.',
        'treatment': ['Continue current farming practices', 'Monitor regularly'],
        'prevention': 'Maintain soil health and balanced fertilization.',
        'urgency': 'No action required'
    },
    'Potato___Early_blight': {
        'english_name': 'Potato Early Blight',
        'swahili_name': 'Ugonjwa wa Mapema wa Viazi',
        'severity': 'Medium',
        'description': 'Fungal disease causing dark brown spots with yellow rings on potato leaves.',
        'treatment': [
            'Apply fungicides containing chlorothalonil or mancozeb every 7-10 days',
            'Remove and destroy infected leaves immediately',
            'Avoid overhead irrigation',
            'Ensure adequate potassium fertilization',
            'Harvest promptly when mature'
        ],
        'prevention': 'Use certified disease-free seed potatoes. Practice 2-3 year crop rotation.',
        'urgency': 'Act within 1-2 weeks of first signs'
    },
    'Potato___Late_blight': {
        'english_name': 'Potato Late Blight',
        'swahili_name': 'Ugonjwa wa Marehemu wa Viazi',
        'severity': 'Critical',
        'description': 'Highly destructive disease causing water-soaked dark lesions. Can destroy entire crop within days.',
        'treatment': [
            'URGENT: Apply metalaxyl or cymoxanil fungicides immediately',
            'Remove and destroy all infected plants — do not compost',
            'Stop overhead irrigation completely',
            'Harvest remaining healthy tubers immediately',
            'Inform neighboring farmers — spreads very rapidly'
        ],
        'prevention': 'Plant resistant varieties. Never use infected tubers as seed.',
        'urgency': 'IMMEDIATE ACTION REQUIRED — can destroy entire crop within 1 week'
    },
    'Potato___healthy': {
        'english_name': 'Healthy Potato',
        'swahili_name': 'Viazi Vyenye Afya',
        'severity': 'None',
        'description': 'Your potato crop appears healthy. No disease detected.',
        'treatment': ['Continue current farming practices', 'Monitor weekly'],
        'prevention': 'Use certified seed potatoes. Practice proper crop rotation.',
        'urgency': 'No action required'
    },
    'Tomato___Bacterial_spot': {
        'english_name': 'Tomato Bacterial Spot',
        'swahili_name': 'Madoa ya Bakteria ya Nyanya',
        'severity': 'High',
        'description': 'Bacterial disease causing small water-soaked spots on leaves, stems, and fruits.',
        'treatment': [
            'Apply copper-based bactericides every 7 days',
            'Remove and destroy infected plant parts',
            'Avoid working in field when plants are wet',
            'Disinfect tools between plants',
            'Improve field drainage'
        ],
        'prevention': 'Use disease-free certified seeds. Avoid overhead irrigation.',
        'urgency': 'Act within 1 week of first signs'
    },
    'Tomato___Early_blight': {
        'english_name': 'Tomato Early Blight',
        'swahili_name': 'Ugonjwa wa Mapema wa Nyanya',
        'severity': 'Medium',
        'description': 'Fungal disease causing dark brown spots with concentric rings on lower leaves.',
        'treatment': [
            'Apply fungicides containing chlorothalonil or mancozeb',
            'Remove infected lower leaves',
            'Mulch around plants to prevent soil splash',
            'Ensure good air circulation',
            'Water at soil level only'
        ],
        'prevention': 'Rotate crops. Use resistant varieties when available.',
        'urgency': 'Act within 2 weeks of first signs'
    },
    'Tomato___Late_blight': {
        'english_name': 'Tomato Late Blight',
        'swahili_name': 'Ugonjwa wa Marehemu wa Nyanya',
        'severity': 'Critical',
        'description': 'Destructive disease causing dark water-soaked lesions and brown rot on fruits.',
        'treatment': [
            'URGENT: Apply metalaxyl or cymoxanil immediately',
            'Remove and destroy all infected plants',
            'Harvest mature fruits immediately',
            'Avoid irrigation until controlled',
            'Alert neighboring farmers immediately'
        ],
        'prevention': 'Plant resistant varieties. Never plant tomatoes near infected potatoes.',
        'urgency': 'IMMEDIATE ACTION REQUIRED'
    },
    'Tomato___Leaf_Mold': {
        'english_name': 'Tomato Leaf Mold',
        'swahili_name': 'Ukungu wa Majani ya Nyanya',
        'severity': 'Medium',
        'description': 'Fungal disease causing yellow patches on upper leaf surface and olive-green mold underneath.',
        'treatment': [
            'Improve ventilation — increase plant spacing',
            'Apply fungicides containing chlorothalonil or copper',
            'Reduce humidity in greenhouse environments',
            'Remove and destroy infected leaves'
        ],
        'prevention': 'Most common in humid poorly ventilated conditions. Ensure good airflow.',
        'urgency': 'Act within 2 weeks of first signs'
    },
    'Tomato___Septoria_leaf_spot': {
        'english_name': 'Tomato Septoria Leaf Spot',
        'swahili_name': 'Madoa ya Majani ya Nyanya',
        'severity': 'Medium',
        'description': 'Fungal disease causing small circular spots with dark borders on lower leaves.',
        'treatment': [
            'Apply fungicides containing chlorothalonil or copper hydroxide',
            'Remove infected lower leaves',
            'Avoid wetting foliage when watering',
            'Mulch to prevent soil splash'
        ],
        'prevention': 'Rotate crops. Remove plant debris at end of season.',
        'urgency': 'Act within 2 weeks of first signs'
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        'english_name': 'Tomato Spider Mites',
        'swahili_name': 'Utitiri wa Nyanya',
        'severity': 'Medium',
        'description': 'Tiny mites causing yellow stippling on leaves. Look for fine webbing under leaves.',
        'treatment': [
            'Apply miticides or insecticidal soap',
            'Spray plants with strong water stream',
            'Introduce predatory mites for biological control',
            'Avoid over-fertilizing with nitrogen',
            'Remove heavily infested leaves'
        ],
        'prevention': 'Spider mites thrive in hot dry conditions. Maintain adequate soil moisture.',
        'urgency': 'Act within 1-2 weeks — populations grow rapidly'
    },
    'Tomato___Target_Spot': {
        'english_name': 'Tomato Target Spot',
        'swahili_name': 'Madoa ya Lengo ya Nyanya',
        'severity': 'Medium',
        'description': 'Fungal disease causing circular brown spots with concentric rings on leaves and fruit.',
        'treatment': [
            'Apply fungicides containing chlorothalonil or azoxystrobin',
            'Improve air circulation through pruning',
            'Remove infected plant material',
            'Avoid overhead irrigation'
        ],
        'prevention': 'Common in warm wet conditions. Ensure proper plant spacing.',
        'urgency': 'Act within 2 weeks of first signs'
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'english_name': 'Tomato Yellow Leaf Curl Virus',
        'swahili_name': 'Virusi vya Manjano ya Nyanya',
        'severity': 'Critical',
        'description': 'Viral disease spread by whiteflies causing yellowing and curling leaves. No cure once infected.',
        'treatment': [
            'REMOVE infected plants immediately — there is no cure',
            'Control whitefly populations with imidacloprid',
            'Use yellow sticky traps to monitor whiteflies',
            'Plant virus-resistant tomato varieties next season',
            'Do not replant until whitefly population controlled'
        ],
        'prevention': 'Use whitefly-resistant varieties. Install insect-proof nets in nurseries.',
        'urgency': 'REMOVE INFECTED PLANTS IMMEDIATELY'
    },
    'Tomato___Tomato_mosaic_virus': {
        'english_name': 'Tomato Mosaic Virus',
        'swahili_name': 'Virusi vya Mosaic ya Nyanya',
        'severity': 'High',
        'description': 'Viral disease causing mottled yellow-green mosaic pattern on leaves. Spreads through contact.',
        'treatment': [
            'Remove and destroy infected plants — no chemical cure',
            'Wash hands before handling plants',
            'Disinfect tools with bleach solution (1:9 ratio)',
            'Control aphids which spread the virus',
            'Do not smoke near plants'
        ],
        'prevention': 'Use certified virus-free seeds. Wash hands before entering field.',
        'urgency': 'Remove infected plants within 24 hours'
    },
    'Tomato___healthy': {
        'english_name': 'Healthy Tomato',
        'swahili_name': 'Nyanya Yenye Afya',
        'severity': 'None',
        'description': 'Your tomato crop appears healthy. No disease detected.',
        'treatment': ['Continue current farming practices', 'Monitor weekly'],
        'prevention': 'Maintain proper spacing and balanced fertilization.',
        'urgency': 'No action required'
    }
}

@st.cache_resource
def load_model():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    model = tf.keras.models.load_model(os.path.join(base, 'crop_doctor_model.keras'))
    with open(os.path.join(base, 'class_names.json'), 'r') as f:
        class_names = json.load(f)
    return model, class_names

model, class_names = load_model()

def preprocess_image(image):
    img = image.convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)

st.title("AI Crop Doctor Kenya")
st.markdown(
    "Upload a photo of a crop leaf and get instant disease diagnosis, "
    "treatment recommendations, and prevention advice in English and Swahili. "
    "Supports maize, potato, and tomato crops."
)
st.markdown("---")

st.sidebar.title("AI Crop Doctor Kenya")
st.sidebar.markdown("**Supported Crops:**")
st.sidebar.markdown("- Maize (Mahindi)")
st.sidebar.markdown("- Potato (Viazi)")
st.sidebar.markdown("- Tomato (Nyanya)")
st.sidebar.markdown("---")
st.sidebar.markdown("**Model Performance:**")
st.sidebar.markdown("Validation Accuracy: 87.18%")
st.sidebar.markdown("Classes: 17 (14 diseases + 3 healthy)")
st.sidebar.markdown("Training images: 5,100")
st.sidebar.markdown("Architecture: MobileNetV2")
st.sidebar.markdown("---")
st.sidebar.warning(
    "This tool is for guidance only. "
    "For severe cases consult your nearest "
    "agricultural extension officer or KALRO."
)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Leaf Image")
    uploaded_file = st.file_uploader(
        "Take a clear photo of a single leaf and upload it",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded leaf image", use_container_width=True)

with col2:
    st.subheader("How to take a good photo")
    st.markdown("""
    For best results:
    - Take photo in natural daylight
    - Show one leaf clearly filling most of the frame
    - Focus on the affected area if disease is visible
    - Hold camera steady to avoid blur
    - Supported crops: maize, potato, tomato only
    """)
    st.info(
        "This model was trained on laboratory-quality leaf images. "
        "Results may vary with field photos taken in different lighting."
    )

if uploaded_file is not None:
    if st.button("Diagnose My Crop", type="primary", use_container_width=True):
        with st.spinner("Analyzing leaf image..."):
            img_array = preprocess_image(image)
            predictions = model.predict(img_array, verbose=0)
            predicted_idx = np.argmax(predictions[0])
            confidence = predictions[0][predicted_idx]
            predicted_class = class_names[predicted_idx]

        st.markdown("---")

        if confidence < 0.6:
            st.warning(
                f"Low confidence ({confidence:.1%}) — the model is uncertain about this image. "
                "Please consult an agricultural extension officer for a definitive diagnosis."
            )
        else:
            disease = DISEASE_INFO.get(predicted_class, {})
            severity = disease.get('severity', 'Unknown')

            col1, col2, col3 = st.columns(3)
            col1.metric("Diagnosis", disease.get('english_name', predicted_class))
            col2.metric("Confidence", f"{confidence:.1%}")
            col3.metric("Severity", severity)

            st.markdown(f"**Kiswahili:** {disease.get('swahili_name', 'Haijulikani')}")

            if severity == 'Critical':
                st.error(f"CRITICAL DISEASE DETECTED — {disease.get('urgency', 'Act immediately')}")
            elif severity == 'High':
                st.warning(f"HIGH SEVERITY — {disease.get('urgency', 'Act soon')}")
            elif severity == 'None':
                st.success("Your crop appears healthy. Continue current farming practices.")

            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("About This Disease")
                st.markdown(disease.get('description', ''))
                st.subheader("Prevention")
                st.markdown(disease.get('prevention', ''))
                st.subheader("Urgency")
                st.markdown(f"**{disease.get('urgency', '')}**")

            with col2:
                st.subheader("Treatment Steps")
                treatments = disease.get('treatment', [])
                for i, step in enumerate(treatments, 1):
                    if 'URGENT' in step or 'IMMEDIATE' in step or 'REMOVE' in step:
                        st.error(f"{i}. {step}")
                    else:
                        st.markdown(f"{i}. {step}")

            st.markdown("---")
            st.subheader("Top 3 Predictions")
            top3_idx = np.argsort(predictions[0])[-3:][::-1]
            for idx in top3_idx:
                cls = class_names[idx]
                conf = predictions[0][idx]
                info = DISEASE_INFO.get(cls, {})
                name = info.get('english_name', cls)
                st.progress(float(conf), text=f"{name}: {conf:.1%}")

            st.markdown("---")
            st.subheader("Need More Help?")
            col1, col2, col3 = st.columns(3)
            col1.info("KALRO Helpline\nKenya Agricultural Research Institute\n+254 20 4183301")
            col2.info("Extension Officers\nContact your nearest County Agriculture Office for free farm visits")
            col3.info("SMS Service\nText your crop problem to 0800 720 710 (Safaricom free line)")