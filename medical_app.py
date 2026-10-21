# medical_app.py
# Medical Diagnosis Expert System — Streamlit GUI
# Educational rule-based demonstration for CO4 and CO5.
# NOT for real diagnosis, treatment, or emergency decisions.

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Medical Diagnosis Expert System",
    page_icon="🩺",
    layout="wide"
)

RULES = [
    {
        "id": "R1",
        "if": {"fever", "cough"},
        "then": "Respiratory symptoms present",
        "weight": 0.55,
        "explanation": "Both fever and cough were entered."
    },
    {
        "id": "R2",
        "if": {"fever", "body_ache", "fatigue"},
        "then": "Flu-like symptom pattern",
        "weight": 0.60,
        "explanation": "Fever, body ache, and fatigue were entered."
    },
    {
        "id": "R3",
        "if": {"sneezing", "runny_nose"},
        "then": "Allergy/cold-like symptom pattern",
        "weight": 0.45,
        "explanation": "Sneezing and runny nose were entered."
    },
    {
        "id": "R4",
        "if": {"headache", "nausea"},
        "then": "Headache with nausea pattern",
        "weight": 0.40,
        "explanation": "Headache and nausea were entered."
    },
    {
        "id": "R5",
        "if": {"fever", "rash"},
        "then": "Fever with rash needs professional assessment",
        "weight": 0.65,
        "explanation": "Fever and rash were entered; professional assessment is important."
    }
]

SYMPTOMS = {
    "fever", "cough", "body_ache", "fatigue",
    "sneezing", "runny_nose", "headache", "nausea", "rash"
}

def load_rule_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    required = {"Rule_ID", "Symptoms", "Conclusion", "Weight"}
    if not required.issubset(df.columns):
        raise ValueError("CSV must contain Rule_ID, Symptoms, Conclusion, and Weight columns.")
    return df

def forward_chain(facts):
    # CO4: rules fire when every required symptom fact is present.
    return [rule for rule in RULES if rule["if"].issubset(facts)]

def score_uncertainty(matches):
    # CO5: illustrative rule weights, not medically validated probabilities.
    results = []
    for rule in matches:
        results.append({
            "Possible pattern": rule["then"],
            "Illustrative score": rule["weight"],
            "Matched rule": rule["id"],
            "Explanation": rule["explanation"]
        })
    return sorted(results, key=lambda x: x["Illustrative score"], reverse=True)

def resolution_demo():
    # From (A OR B) and (NOT A), resolution derives B.
    clause1 = {"A", "B"}
    clause2 = {"-A"}
    resolvents = []
    for literal in clause1:
        opposite = literal[1:] if literal.startswith("-") else "-" + literal
        if opposite in clause2:
            resolvents.append(sorted((clause1 - {literal}) | (clause2 - {opposite})))
    return resolvents

st.title("🩺 Medical Diagnosis Expert System")
st.caption("Artificial Intelligence Techniques | CO4: Knowledge Representation · CO5: Uncertainty and Reasoning")

st.warning(
    "Educational demonstration only — this system cannot diagnose illness, recommend treatment, "
    "or replace a qualified healthcare professional. Do not use it for emergencies."
)

with st.sidebar:
    st.header("Patient Symptom Input")
    st.write("Select all symptoms that apply.")
    selected = []
    symptom_labels = {
        "fever": "Fever",
        "cough": "Cough",
        "body_ache": "Body ache",
        "fatigue": "Fatigue",
        "sneezing": "Sneezing",
        "runny_nose": "Runny nose",
        "headache": "Headache",
        "nausea": "Nausea",
        "rash": "Rash"
    }
    for key, label in symptom_labels.items():
        if st.checkbox(label, key=f"symptom_{key}"):
            selected.append(key)

    st.divider()
    uploaded_rules = st.file_uploader(
        "Optional: upload rules CSV",
        type=["csv"],
        help="The app uses its built-in rules for reasoning. Uploading the CSV lets you inspect the rule table."
    )
    analyze = st.button("Analyze symptoms", type="primary", use_container_width=True)

tab1, tab2, tab3 = st.tabs([
    "🩺 Symptom Analysis", "📚 Knowledge Base (CO4)", "🧠 Reasoning (CO5)"
])

with tab1:
    st.subheader("Symptom Analysis")
    if not analyze:
        st.info("Select symptoms in the sidebar and click **Analyze symptoms**.")
        c1, c2, c3 = st.columns(3)
        c1.metric("CO4", "IF–THEN Rules")
        c2.metric("CO5", "Uncertainty")
        c3.metric("Inference", "Forward Chaining")
    else:
        facts = set(selected)
        if not facts:
            st.error("Please select at least one symptom before analyzing.")
        else:
            matches = forward_chain(facts)
            st.write("**Symptoms selected:** " + ", ".join(symptom_labels[s] for s in selected))
            if not matches:
                st.info("No predefined rule matched these symptoms. This does not mean that no medical condition exists.")
            else:
                results = score_uncertainty(matches)
                st.subheader("Possible educational patterns — not diagnoses")
                st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
                st.caption("Illustrative scores are rule weights only, not probabilities or clinical risk estimates.")
            if "fever" in facts and "rash" in facts:
                st.error("Fever with rash can require prompt professional assessment. Contact a healthcare professional, especially if symptoms are severe or worsening.")
            st.success("Inference completed using the educational rule base.")

with tab2:
    st.subheader("Knowledge Base — CO4")
    st.write("Facts are the symptoms selected by the user. A rule fires only when all symptoms in its IF condition are present.")
    rule_rows = []
    for rule in RULES:
        rule_rows.append({
            "Rule ID": rule["id"],
            "IF symptoms": " AND ".join(sorted(rule["if"])),
            "THEN conclusion": rule["then"],
            "Illustrative weight": rule["weight"]
        })
    st.dataframe(pd.DataFrame(rule_rows), use_container_width=True, hide_index=True)
    if uploaded_rules is not None:
        try:
            st.write("Uploaded rule CSV preview:")
            st.dataframe(load_rule_csv(uploaded_rules), use_container_width=True, hide_index=True)
        except Exception as exc:
            st.error(str(exc))

with tab3:
    st.subheader("Uncertainty and Logical Reasoning — CO5")
    st.write("The rule weights demonstrate that conclusions can have different illustrative strengths. They are not calibrated probabilities.")
    st.markdown("**Resolution example**")
    st.code("(A OR B) AND (NOT A)  ⟹  B")
    st.write("Computed resolvent:", resolution_demo())
    st.caption("This is a small propositional-logic example to illustrate resolution; it is not a medical rule.")

st.divider()
st.caption("Academic prototype for demonstrating CO4 and CO5. It is not clinically validated.")
