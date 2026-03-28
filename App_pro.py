# ========================= APP VERSION PRO =========================
import streamlit as st
from streamlit.components.v1 import html
from datetime import datetime

st.set_page_config(page_title="Gestion de Classe PRO", layout="wide")

# Dummy data (replace with your DB logic)
if "etudiants" not in st.session_state:
    st.session_state.etudiants = {
        "1": {"nom": "Ahmed Benali", "score": 3, "historique": []},
        "2": {"nom": "Fatima Zahra", "score": 0, "historique": []}
    }

etudiants = st.session_state.etudiants

def get_mention(score):
    if score >= 10:
        return "Passable"
    return "Echec"

# Handle button clicks via query params
query_params = st.query_params
if "eid" in query_params and "delta" in query_params:
    eid = query_params["eid"]
    delta = int(query_params["delta"])

    if eid in etudiants:
        etudiants[eid]["score"] += delta
        etudiants[eid]["historique"].append({
            "note": delta,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

    st.query_params.clear()
    st.rerun()

# CSS
st.markdown("""
<style>
.student-card {
    background: #FFFFFF;
    border-radius: 24px;
    border: 1px solid #C8D8D5;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.student-info {
    display: flex;
    gap: 20px;
    align-items: center;
}

.student-name {
    font-size: 18px;
    font-weight: 800;
    color: #004D40;
}

.student-score {
    font-size: 30px;
    font-weight: 900;
    color: #004D40;
}

.mention-badge {
    padding: 6px 14px;
    border-radius: 40px;
    font-size: 12px;
    font-weight: 800;
    background: #FFEBEE;
    color: #C62828;
}

.btn-group {
    display: flex;
    gap: 10px;
}

.btn {
    border: none;
    border-radius: 40px;
    font-weight: 800;
    padding: 10px 20px;
    cursor: pointer;
}

.btn-plus {
    background: #2E7D32;
    color: white;
}

.btn-moins {
    background: #C62828;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Gestion de Classe (Version PRO)")

# Display students
for eid, etudiant in etudiants.items():
    score = etudiant["score"]
    mention = get_mention(score)

    html_code = f"""
    <div class="student-card">
        <div class="student-info">
            <span class="student-name">{etudiant["nom"]}</span>
            <span class="student-score">{score}</span>
            <span class="mention-badge">{mention}</span>
        </div>

        <div class="btn-group">
            <button onclick="updateScore('{eid}', 1)" class="btn btn-plus">+1</button>
            <button onclick="updateScore('{eid}', -1)" class="btn btn-moins">-1</button>
        </div>
    </div>

    <script>
    function updateScore(eid, delta) {
        const url = new URL(window.location);
        url.searchParams.set("eid", eid);
        url.searchParams.set("delta", delta);
        window.location.href = url.toString();
    }
    </script>
    """

    html(html_code, height=120)
