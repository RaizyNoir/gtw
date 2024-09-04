import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load datasets
description = pd.read_csv('description.csv')
precautions = pd.read_csv('precautions_df.csv')
medications = pd.read_csv('medications.csv')
diets = pd.read_csv("diets.csv")
workout = pd.read_csv("workout_df.csv")

# Load the model
best_model = pickle.load(open('best_model.pkl', 'rb'))

# Define helper functions


def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][[
        'Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values[0] if pd.notna(col)]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [m for m in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [d for d in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']
    wrkout = [w for w in wrkout.values]

    return desc, pre, med, die, wrkout


symptoms_dict = {
    'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4,
    'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10,
    'vomiting': 11, 'burning_micturition': 12, 'spotting_urination': 13, 'fatigue': 14, 'weight_gain': 15,
    'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20,
    'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25,
    'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30,
    'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35,
    'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40,
    'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45,
    'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49,
    'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54,
    'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59,
    'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64,
    'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70,
    'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75,
    'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80,
    'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85,
    'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89,
    'foul_smell_of_urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93,
    'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98,
    'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic_patches': 102,
    'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106,
    'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110,
    'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113,
    'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116,
    'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120,
    'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125,
    'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129,
    'red_sore_around_nose': 130, 'yellow_crust_ooze': 131
}

diseases_list = {
    15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Kholestasis Kronis', 14: 'Reaksi Obat', 33: 'Penyakit Ulkus Peptikum',
    1: 'AIDS', 12: 'Diabetes', 17: 'Gastroenteritis', 6: 'Asma Bronkial', 23: 'Hipertensi', 30: 'Migrain',
    7: 'Spondilosis Serviks', 32: 'Paralisis (Pendarahan Otak)', 28: 'Jaundice', 29: 'Malaria', 8: 'Cacar Air',
    11: 'Dengue', 37: 'Typhoid', 40: 'Hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D',
    22: 'Hepatitis E', 3: 'Hepatitis Alkoholik', 36: 'Tuberkulosis', 10: 'Flu Biasa', 34: 'Pneumonia',
    13: 'Hemoroid Dimorfik', 18: 'Serangan Jantung', 39: 'Vena Varises', 26: 'Hipotiroidisme', 24: 'Hipertiroidisme',
    25: 'Hipoglikemia', 31: 'Osteoartritis', 5: 'Artritis', 0: 'Vertigo Posisi Paroksismal', 2: 'Jerawat',
    38: 'Infeksi Saluran Kemih', 35: 'Psoriasis', 27: 'Impetigo'
}


def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1
    return diseases_list[best_model.predict([input_vector])[0]]


# Streamlit UI
st.title("Sistem Rekomendasi Kesehatan")
st.write("Pilih gejala yang Anda alami:")

# Create multiple select box for symptoms
symptoms_options = list(symptoms_dict.keys())
selected_symptoms = st.multiselect("Gejala:", symptoms_options)

if st.button('Prediksi'):
    if selected_symptoms:
        predicted_disease = get_predicted_value(selected_symptoms)
        st.write("**Penyakit yang Diprediksi:**", predicted_disease)
        desc, pre, med, die, wrkout = helper(predicted_disease)
        st.write("**Deskripsi:**", desc)
        
    else:
        st.write("Silakan pilih gejala terlebih dahulu.")

# Show additional information based on the stored values
if predicted_disease:
    if st.button('Tampilkan Tindakan Pencegahan'):
        st.write("**Tindakan Pencegahan:**")
        for i, p in enumerate(pre, 1):
            st.write(f"{i}. {p}")
        
    if st.button('Tampilkan Obat-obatan'):
        st.write("**Obat-obatan:**")
        for i, m in enumerate(med, 1):
            st.write(f"{i}. {m}")
        
    if st.button('Tampilkan Diet'):
        st.write("**Diet:**")
        for i, d in enumerate(die, 1):
            st.write(f"{i}. {d}")
        
    if st.button('Tampilkan Latihan'):
        st.write("**Latihan:**")
        for i, w in enumerate(wrkout, 1):
            st.write(f"{i}. {w}")
