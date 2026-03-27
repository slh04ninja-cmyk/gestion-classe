# ========================= PARTIE 1 =========================
# Imports, configuration, CSS, fonctions de base et Supabase

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from supabase import create_client, Client

st.set_page_config(
    page_title="Gestion de Classe",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Récupération des secrets Supabase ──────────────────────────────────
# Assurez-vous que ces secrets sont définis dans Streamlit Cloud ou dans .streamlit/secrets.toml
SUPABASE_URL = st.secrets["supabase_url"]
SUPABASE_KEY = st.secrets["supabase_key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── CSS (identique à l'original) ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@400;600;700&display=swap');

:root {
    --teal:    #00796B;
    --teal2:   #004D40;
    --mint:    #E0F2F1;
    --gold:    #FF8F00;
    --red:     #C62828;
    --blue:    #1565C0;
    --bg:      #F4F7F6;
    --card:    #FFFFFF;
    --text:    #1A2E2A;
    --muted:   #546E6A;
    --border:  #C8D8D5;
}

* { font-family: 'Nunito', sans-serif; color: var(--text); }

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(circle at 5% 10%, rgba(0,121,107,0.07) 0%, transparent 50%),
        radial-gradient(circle at 95% 90%, rgba(255,143,0,0.05) 0%, transparent 50%);
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, var(--teal2) 0%, var(--teal) 100%);
    border-radius: 20px; padding: 28px 36px 24px;
    margin-bottom: 24px; position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,77,64,0.25);
}
.app-header::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, var(--gold), transparent);
}
.app-tag   { font-size:11px; font-weight:800; letter-spacing:4px; color:rgba(255,255,255,0.5); text-transform:uppercase; margin-bottom:5px; }
.app-title { font-size:30px; font-weight:900; color:#fff; line-height:1.1; margin:0; }
.app-sub   { font-size:13px; color:rgba(255,255,255,0.6); margin-top:6px; }

/* ── Cards ── */
.card {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 16px; padding: 24px; margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,77,64,0.06);
}
.card-title {
    font-size:16px; font-weight:800; color:var(--teal2);
    border-bottom: 2px solid var(--mint);
    padding-bottom:10px; margin-bottom:16px;
}

/* Cartes étudiant */
.student-card {
    background: #FFFFFF;
    border-radius: 16px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: box-shadow 0.2s;
}
.student-card:hover {
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* Nom en grand */
.student-name-large {
    font-size: 18px;
    font-weight: 800;
    color: var(--teal2);
    margin-bottom: 6px;
}

/* Score + mention */
.student-score-large {
    font-size: 28px;
    font-weight: 900;
    color: var(--teal2);
    display: flex;
    align-items: baseline;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}
.mention-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 800;
    background: #E0F2F1;
    color: #00796B;
}
.mention-badge.m-tb { background: #E8F5E9; color: #1B5E20; }
.mention-badge.m-b  { background: #E3F2FD; color: #0D47A1; }
.mention-badge.m-ab { background: #FFF8E1; color: #7B5800; }
.mention-badge.m-p  { background: #FFF3E0; color: #E65100; }
.mention-badge.m-ec { background: #FFEBEE; color: #B71C1C; }

/* Dernières notes */
.recent-notes {
    margin: 8px 0;
    font-size: 12px;
    color: var(--muted);
}
.note-badge {
    display: inline-block;
    background: #F5F5F5;
    border-radius: 20px;
    padding: 2px 8px;
    margin-right: 5px;
    font-weight: 700;
}
.note-badge.note-1  { background: #C8E6C9; color: #1B5E20; }
.note-badge.note-0  { background: #E0E0E0; color: #757575; }
.note-badge.note--1 { background: #FFCDD2; color: #C62828; }

/* Tendances */
.trend {
    font-size: 13px;
    font-weight: 600;
    margin-top: 6px;
}
.trend-up      { color: #2E7D32; }
.trend-down    { color: #C62828; }
.trend-stable  { color: #FF8F00; }

/* ── Boutons note ── */
.stButton > button {
    border-radius:10px !important; font-weight:800 !important;
    font-size:16px !important; padding:8px 20px !important;
    border: none !important; transition: all 0.15s !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--mint); border-radius:12px; padding:4px; gap:4px;
    border:none; margin-bottom:16px;
}
.stTabs [data-baseweb="tab"] {
    border-radius:8px; font-weight:800; font-size:13px; color:var(--muted);
    padding:9px 18px; border:none; background:transparent;
}
.stTabs [aria-selected="true"] { background:var(--teal) !important; color:white !important; }
.stTabs [data-baseweb="tab-border"] { display:none; }

/* ── Inputs ── */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    border-radius:8px !important; border-color:var(--border) !important;
    color:var(--text) !important; background:#fff !important;
    font-weight:600 !important;
}
.stTextInput label, .stSelectbox label, .stNumberInput label,
.stTextArea label { font-weight:700 !important; color:var(--text) !important; }

/* ── Download buttons ── */
.stDownloadButton > button {
    background:white !important; border-radius:10px !important;
    font-weight:700 !important; font-size:13px !important; width:100%; margin-top:6px;
}
.dl-excel .stDownloadButton > button { color:var(--teal) !important; border:2px solid var(--teal) !important; }
.dl-pdf   .stDownloadButton > button { color:var(--red) !important;  border:2px solid var(--red)  !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background:var(--mint); border-radius:10px; padding:12px 16px !important; border:1px solid var(--border);
}
[data-testid="stMetricLabel"] p  { color:#333 !important; font-weight:700 !important; font-size:12px !important; }
[data-testid="stMetricValue"] div{ color:var(--teal2) !important; font-weight:900 !important; font-size:22px !important; }

/* ── Divers ── */
hr { border-color:var(--border) !important; margin:16px 0 !important; }
.app-footer { text-align:center; padding:16px; color:var(--muted); font-size:11px; margin-top:24px; border-top:1px solid var(--border); }
.badge { display:inline-block; background:var(--mint); color:var(--teal2); font-size:11px; font-weight:700; padding:3px 10px; border-radius:20px; border:1px solid var(--border); }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding-top:2rem; }
</style>
""", unsafe_allow_html=True)

# ── Fonctions utilitaires ──────────────────────────────────────────────
def get_mention(score):
    if score >= 16:   return "Très Bien",  "m-tb"
    elif score >= 14: return "Bien",        "m-b"
    elif score >= 12: return "Assez Bien",  "m-ab"
    elif score >= 10: return "Passable",    "m-p"
    else:             return "Echec",       "m-ec"

def load_db():
    """Charge toutes les classes depuis Supabase."""
    try:
        response = supabase.table("classes").select("*").execute()
        db = {}
        for row in response.data:
            db[row["id"]] = row["data"]
        return db
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")
        return {}

def save_db(db):
    """Sauvegarde toutes les classes dans Supabase."""
    try:
        for class_id, class_data in db.items():
            # Vérifier si la classe existe déjà
            existing = supabase.table("classes").select("id").eq("id", class_id).execute()
            if existing.data:
                # Mise à jour
                supabase.table("classes").update({"data": class_data}).eq("id", class_id).execute()
            else:
                # Insertion
                supabase.table("classes").insert({"id": class_id, "data": class_data}).execute()
        # Optionnel : suppression des classes qui ne sont plus dans le dictionnaire (nettoyage)
        # Récupérer tous les IDs existants en base
        all_ids = {row["id"] for row in supabase.table("classes").select("id").execute().data}
        for class_id in all_ids - set(db.keys()):
            supabase.table("classes").delete().eq("id", class_id).execute()
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")
# ========================= PARTIE 2 =========================
# Header, sidebar, initialisation session, onglets Accueil et Créer une classe

# ── Initialisation de la session ───────────────────────────────────────
if "db" not in st.session_state:
    st.session_state.db = load_db()
if "selected_class" not in st.session_state:
    st.session_state.selected_class = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None

db = st.session_state.db  # alias local

# ── HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-tag">Outil Pédagogique</div>
    <div class="app-title">📚 Gestion de Classe</div>
    <div class="app-sub">Suivi des notes de comportement — Accumulation +1 / -1 / 0</div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR : liste des classes ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📂 Mes Classes")
    if db:
        for cid, cls in db.items():
            label = cls["nom"] + " — " + cls["annee"]
            if st.button(label, key=f"sel_{cid}", use_container_width=True):
                st.session_state.selected_class = cid
                st.rerun()
    else:
        st.info("Aucune classe créée.")
    st.markdown("---")
    if st.button("➕ Nouvelle classe", use_container_width=True):
        st.session_state.selected_class = "new"
        st.rerun()

# ── TABS PRINCIPAL ──────────────────────────────────────────────────────
tab_home, tab_new, tab_class = st.tabs(["🏠 Accueil", "➕ Créer une classe", "📋 Gérer la classe"])

# ════════════════════════════════════════════════════════════════════════
# TAB ACCUEIL
# ════════════════════════════════════════════════════════════════════════
with tab_home:
    if not db:
        st.markdown("""
        <div style="text-align:center;padding:48px 20px;color:#546E6A">
            <div style="font-size:56px;margin-bottom:16px">📚</div>
            <div style="font-size:18px;font-weight:800;color:#00796B;margin-bottom:8px">
                Aucune classe enregistrée
            </div>
            <div style="font-size:14px">
                Créez votre première classe dans l'onglet <b>Créer une classe</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Vue d\'ensemble</div>', unsafe_allow_html=True)

        nb_classes   = len(db)
        nb_etudiants = sum(len(c["etudiants"]) for c in db.values())
        c1, c2 = st.columns(2)
        c1.metric("Classes enregistrées", nb_classes)
        c2.metric("Total étudiants",      nb_etudiants)
        st.markdown("---")

        for cid, cls in db.items():
            etudiants = cls["etudiants"]
            nb = len(etudiants)
            scores = [e["score"] for e in etudiants.values()]
            moy = sum(scores) / nb if nb else 0

            col_a, col_b, col_c = st.columns([3,1,1])
            col_a.markdown(
                '<b style="font-size:15px">' + cls["nom"] + '</b>'
                ' <span style="color:#546E6A;font-size:13px">— ' + cls["annee"] + '</span>',
                unsafe_allow_html=True
            )
            col_b.markdown(
                '<div style="text-align:center;font-size:13px;color:#546E6A">'
                + str(nb) + ' étudiants</div>',
                unsafe_allow_html=True
            )
            col_c.markdown(
                '<div style="text-align:center;font-size:13px;font-weight:800;color:#00796B">'
                'Moy: ' + "{:.1f}".format(moy) + '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# TAB CRÉER UNE CLASSE
# ════════════════════════════════════════════════════════════════════════
with tab_new:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">➕ Nouvelle Classe</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        nom_classe  = st.text_input("Nom de la classe", placeholder="ex: 2BACSPF-1")
    with col2:
        annee_scol  = st.text_input("Année scolaire", placeholder="ex: 2025/2026")

    st.markdown("**Liste des étudiants**")
    methode = st.radio("Méthode de saisie", ["Saisie manuelle", "Import Excel/CSV"], horizontal=True)

    etudiants_input = []

    if methode == "Saisie manuelle":
        nb_students = st.number_input("Nombre d'étudiants", min_value=1, max_value=60, value=5, step=1)
        st.markdown("*Saisissez un nom par ligne :*")
        noms_text = st.text_area(
            "Noms des étudiants (un par ligne)",
            height=max(120, int(nb_students) * 22),
            placeholder="Ahmed Benali\nFatima Zahra\nYoussef Alami\n..."
        )
        if noms_text.strip():
            etudiants_input = [n.strip() for n in noms_text.strip().split("\n") if n.strip()]
    else:
        uploaded_list = st.file_uploader("Fichier Excel ou CSV (1 colonne = noms)", type=["xlsx","xls","csv"])
        if uploaded_list:
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    if uploaded_list.name.endswith(".csv"):
                        df_list = pd.read_csv(io.BytesIO(uploaded_list.getvalue()), header=None)
                    else:
                        df_list = pd.read_excel(io.BytesIO(uploaded_list.getvalue()), header=None, engine="openpyxl")
                for col in df_list.columns:
                    vals = df_list[col].dropna().astype(str).str.strip()
                    vals = vals[vals.str.len() > 1]
                    if len(vals) > 0:
                        etudiants_input = vals.tolist()
                        break
                st.success(f"✅ {len(etudiants_input)} étudiants détectés")
                st.write(etudiants_input[:5])
            except Exception as e:
                st.error(f"Erreur : {e}")

    if etudiants_input:
        st.info(f"👥 {len(etudiants_input)} étudiants prêts à être enregistrés")

    if st.button("💾 Créer la classe", type="primary"):
        if not nom_classe.strip():
            st.error("❌ Le nom de la classe est obligatoire.")
        elif not annee_scol.strip():
            st.error("❌ L'année scolaire est obligatoire.")
        elif not etudiants_input:
            st.error("❌ Ajoutez au moins un étudiant.")
        else:
            cid = nom_classe.strip().replace(" ", "_") + "_" + annee_scol.strip().replace("/", "-")
            if cid in db:
                st.error("❌ Une classe avec ce nom et cette année existe déjà.")
            else:
                db[cid] = {
                    "nom":       nom_classe.strip(),
                    "annee":     annee_scol.strip(),
                    "created":   datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "etudiants": {
                        str(i): {
                            "nom":       nom,
                            "score":     0,
                            "historique":[]
                        }
                        for i, nom in enumerate(etudiants_input)
                    }
                }
                save_db(db)  # ← Sauvegarde immédiate
                st.session_state.selected_class = cid
                st.success(f"✅ Classe '{nom_classe}' créée avec {len(etudiants_input)} étudiants !")
                st.balloons()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
# ========================= PARTIE 3 =========================
# Onglet Gérer la classe et footer

# ════════════════════════════════════════════════════════════════════════
# TAB GÉRER LA CLASSE
# ════════════════════════════════════════════════════════════════════════
with tab_class:
    if not db:
        st.info("Aucune classe disponible. Créez-en une d'abord.")
    else:
        # Sélecteur de classe
        classe_options = {cid: cls["nom"] + " — " + cls["annee"] for cid, cls in db.items()}
        selected = st.selectbox("Choisir une classe", options=list(classe_options.keys()),
                                format_func=lambda x: classe_options[x],
                                index=list(classe_options.keys()).index(st.session_state.selected_class)
                                if st.session_state.selected_class in classe_options else 0)
        st.session_state.selected_class = selected
        cls = db[selected]

        # ── Sous-tabs
        stab1, stab2, stab3, stab4 = st.tabs(["⚡ Saisie Notes", "📊 Classement", "📜 Historique", "⚙️ Gérer"])

        # ── SOUS-TAB 1 : Saisie des notes ──────────────────────────────
        with stab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="card-title">⚡ Saisie rapide — '
                + cls["nom"] + ' &nbsp;<span style="font-size:13px;color:#546E6A">'
                + cls["annee"] + '</span></div>',
                unsafe_allow_html=True
            )

            etudiants = cls["etudiants"]
            nb = len(etudiants)
            scores = [e["score"] for e in etudiants.values()]
            moy = sum(scores) / nb if nb else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Étudiants", nb)
            c2.metric("Moyenne", "{:.2f}".format(moy))
            c3.metric("Meilleur", max(scores) if scores else 0)
            c4.metric("Plus bas", min(scores) if scores else 0)
            st.markdown("---")

            # Note globale (tous les étudiants)
            st.markdown("**Note globale (toute la classe)**")
            col_g1, col_g2, col_g3, col_g4 = st.columns([1,1,1,3])
            note_globale = None
            with col_g1:
                if st.button("➕ +1 Classe", key="g_plus"):
                    note_globale = 1
            with col_g2:
                if st.button("⓪ 0 Classe", key="g_zero"):
                    note_globale = 0
            with col_g3:
                if st.button("➖ -1 Classe", key="g_moins"):
                    note_globale = -1
            with col_g4:
                motif_global = st.text_input("Motif (optionnel)", key="motif_global",
                                             placeholder="ex: Participation active, Retard...")

            if note_globale is not None:
                ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                for eid in etudiants:
                    etudiants[eid]["score"] += note_globale
                    etudiants[eid]["historique"].append({
                        "note": note_globale, "motif": motif_global,
                        "date": ts, "type": "global"
                    })
                save_db(db)  # ← Sauvegarde
                st.success(f"✅ Note {'+1' if note_globale==1 else ('-1' if note_globale==-1 else '0')} appliquée à toute la classe !")
                st.rerun()

            st.markdown("---")
            st.markdown("**Notes individuelles**")

            # Afficher chaque étudiant avec une carte
            for eid, etudiant in sorted(etudiants.items(), key=lambda x: x[1]["nom"]):
                score = etudiant["score"]
                mention, m_cls = get_mention(score)

                # Calcul de la tendance
                historique = etudiant["historique"]
                last_notes = [h["note"] for h in historique[-3:]] if historique else []
                net_change = sum(last_notes)
                if net_change > 0:
                    trend = "📈 En progression"
                    trend_class = "trend-up"
                elif net_change < 0:
                    trend = "📉 En baisse"
                    trend_class = "trend-down"
                else:
                    trend = "➡️ Stable"
                    trend_class = "trend-stable"

                st.markdown('<div class="student-card">', unsafe_allow_html=True)

                col_left, col_right = st.columns([2, 1])

                with col_left:
                    st.markdown(f'<div class="student-name-large">{etudiant["nom"]}</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="student-score-large">{score} '
                        f'<span class="mention-badge {m_cls}">{mention}</span></div>',
                        unsafe_allow_html=True
                    )

                    if last_notes:
                        badges = []
                        for n in last_notes:
                            if n > 0:
                                badges.append(f'<span class="note-badge note-1">+{n}</span>')
                            elif n == 0:
                                badges.append(f'<span class="note-badge note-0">0</span>')
                            else:
                                badges.append(f'<span class="note-badge note--1">{n}</span>')
                        st.markdown(
                            f'<div class="recent-notes">Dernières notes : {" ".join(badges)}</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown(f'<div class="trend {trend_class}">{trend}</div>', unsafe_allow_html=True)

                with col_right:
                    btns = st.columns(3)
                    with btns[0]:
                        if st.button("➕ +1", key=f"p_{eid}", use_container_width=True):
                            motif = st.session_state.get(f"motif_{eid}", "")
                            ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                            etudiants[eid]["score"] += 1
                            etudiants[eid]["historique"].append({"note":1,"motif":motif,"date":ts,"type":"indiv"})
                            save_db(db)
                            st.rerun()
                    with btns[1]:
                        if st.button("⓪ 0", key=f"z_{eid}", use_container_width=True):
                            motif = st.session_state.get(f"motif_{eid}", "")
                            ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                            etudiants[eid]["historique"].append({"note":0,"motif":motif,"date":ts,"type":"indiv"})
                            save_db(db)
                            st.rerun()
                    with btns[2]:
                        if st.button("➖ -1", key=f"m_{eid}", use_container_width=True):
                            motif = st.session_state.get(f"motif_{eid}", "")
                            ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                            etudiants[eid]["score"] -= 1
                            etudiants[eid]["historique"].append({"note":-1,"motif":motif,"date":ts,"type":"indiv"})
                            save_db(db)
                            st.rerun()

                    st.text_input(
                        "Motif",
                        key=f"motif_{eid}",
                        label_visibility="collapsed",
                        placeholder="Motif (optionnel)"
                    )

                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # ── SOUS-TAB 2 : Classement ─────────────────────────────────────
        with stab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📊 Classement — ' + cls["nom"] + '</div>', unsafe_allow_html=True)

            etudiants = cls["etudiants"]
            sorted_etudiants = sorted(etudiants.items(), key=lambda x: x[1]["score"], reverse=True)

            rows_html = ""
            for rang, (eid, e) in enumerate(sorted_etudiants, 1):
                score = e["score"]
                mention, m_cls = get_mention(score)
                if rang == 1:   medal = "🥇"
                elif rang == 2: medal = "🥈"
                elif rang == 3: medal = "🥉"
                else:           medal = str(rang)
                bg = "#E8F5E9" if score >= 14 else ("#E0F2F1" if score >= 10 else "#FFEBEE")
                sc_color = "#2E7D32" if score > 0 else ("#C62828" if score < 0 else "#546E6A")
                rows_html += (
                    '<tr style="background:' + bg + '">'
                    '<td style="text-align:center;font-weight:800;font-size:15px">' + str(medal) + '</td>'
                    '<td style="font-weight:700;padding-left:8px">' + e["nom"] + '</td>'
                    '<td style="text-align:center;font-weight:900;font-size:20px;color:' + sc_color + '">' + str(score) + '</td>'
                    '<td style="text-align:center"><span style="background:white;border-radius:12px;'
                    'padding:2px 10px;font-size:11px;font-weight:700">' + mention + '</span></td>'
                    '<td style="text-align:center;color:#546E6A;font-size:12px">'
                    + str(len(e["historique"])) + ' opérations</td>'
                    '</tr>'
                )

            table_html = (
                '<table style="width:100%;border-collapse:collapse;font-size:13px">'
                '<thead><tr style="background:#004D40;color:white">'
                '<th style="padding:10px 6px">Rang</th>'
                '<th style="padding:10px 8px;text-align:left">Étudiant</th>'
                '<th style="padding:10px 6px">Score</th>'
                '<th style="padding:10px 6px">Mention</th>'
                '<th style="padding:10px 6px">Historique</th>'
                '</tr></thead>'
                '<tbody>' + rows_html + '</tbody>'
                '</table>'
            )
            st.markdown(table_html, unsafe_allow_html=True)
            st.markdown("---")

            # Export Excel et PDF (identique à l'original)
            dl1, dl2 = st.columns(2)
            with dl1:
                st.markdown('<div class="dl-excel">', unsafe_allow_html=True)
                import openpyxl
                from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Classement"
                thin = Side(style="thin", color="C8D8D5")
                bdr  = Border(left=thin, right=thin, top=thin, bottom=thin)
                teal_fill = PatternFill("solid", fgColor="004D40")
                mint_fill = PatternFill("solid", fgColor="E0F2F1")

                ws.merge_cells("A1:E1")
                c = ws.cell(row=1, column=1, value=cls["nom"] + " — " + cls["annee"])
                c.fill = teal_fill; c.font = Font(bold=True, color="FFFFFF", size=13)
                c.alignment = Alignment(horizontal="center", vertical="center")
                ws.row_dimensions[1].height = 30

                for col, h in enumerate(["Rang","Nom Étudiant","Score","Mention","Nb Opérations"], 1):
                    x = ws.cell(row=2, column=col, value=h)
                    x.fill = PatternFill("solid", fgColor="00796B")
                    x.font = Font(bold=True, color="FFFFFF", size=10)
                    x.alignment = Alignment(horizontal="center", vertical="center")
                    x.border = bdr

                for r, (eid, e) in enumerate(sorted_etudiants, 3):
                    mention, _ = get_mention(e["score"])
                    fill = mint_fill if r % 2 == 0 else None
                    for col, val in enumerate([r-2, e["nom"], e["score"], mention, len(e["historique"])], 1):
                        x = ws.cell(row=r, column=col, value=val)
                        if fill: x.fill = fill
                        x.alignment = Alignment(horizontal="center" if col != 2 else "left", vertical="center")
                        x.border = bdr
                        if col == 2: x.font = Font(bold=True)

                for col, width in zip("ABCDE", [8, 30, 10, 15, 16]):
                    ws.column_dimensions[col].width = width

                buf = io.BytesIO()
                wb.save(buf); buf.seek(0)
                st.download_button("📊 Exporter Excel",
                    data=buf,
                    file_name=cls["nom"] + "_classement.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="dl_cls_excel")
                st.markdown('</div>', unsafe_allow_html=True)

            with dl2:
                st.markdown('<div class="dl-pdf">', unsafe_allow_html=True)
                try:
                    from reportlab.lib.pagesizes import A4
                    from reportlab.lib import colors as rl_colors
                    from reportlab.lib.units import cm
                    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.pdfbase import pdfmetrics
                    from reportlab.pdfbase.ttfonts import TTFont
                    import os as _os

                    pdf_buf = io.BytesIO()
                    doc = SimpleDocTemplate(pdf_buf, pagesize=A4,
                                            leftMargin=2*cm, rightMargin=2*cm,
                                            topMargin=2*cm, bottomMargin=2*cm)
                    styles = getSampleStyleSheet()
                    TEAL  = rl_colors.HexColor("#004D40")
                    TEAL2 = rl_colors.HexColor("#00796B")
                    MINT  = rl_colors.HexColor("#E0F2F1")
                    GOLD  = rl_colors.HexColor("#FFF8E1")
                    GREEN = rl_colors.HexColor("#E8F5E9")
                    RED   = rl_colors.HexColor("#FFEBEE")

                    # Police arabe
                    ar_font = "Helvetica"
                    try:
                        script_dir = _os.path.dirname(_os.path.abspath(__file__)) if "__file__" in dir() else "/mount/src/gestion-classe"
                        amiri = _os.path.join(script_dir, "Amiri-Regular.ttf")
                        if not _os.path.exists(amiri): amiri = "Amiri-Regular.ttf"
                        if _os.path.exists(amiri):
                            pdfmetrics.registerFont(TTFont("Amiri", amiri))
                            ar_font = "Amiri"
                    except Exception:
                        pass

                    def ar_pdf(text):
                        try:
                            import arabic_reshaper
                            from bidi.algorithm import get_display
                            return get_display(arabic_reshaper.reshape(str(text)))
                        except Exception:
                            t = str(text).strip()
                            if any('\u0600' <= c <= '\u06FF' for c in t):
                                return ' '.join(reversed(t.split()))
                            return t

                    title_s = ParagraphStyle("t", fontSize=14, fontName="Helvetica-Bold", textColor=rl_colors.white)
                    stat_s  = ParagraphStyle("st", fontSize=10, fontName="Helvetica-Bold", textColor=TEAL, spaceAfter=4)
                    story   = []

                    ht = Table([[Paragraph(cls["nom"] + " — " + cls["annee"], title_s)]],
                               colWidths=[17*cm])
                    ht.setStyle(TableStyle([
                        ("BACKGROUND",(0,0),(-1,-1), TEAL),
                        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                        ("LEFTPADDING",(0,0),(-1,-1),16),
                        ("TOPPADDING",(0,0),(-1,-1),14),
                        ("BOTTOMPADDING",(0,0),(-1,-1),14),
                    ]))
                    story.append(ht)
                    story.append(Spacer(1, 0.4*cm))

                    scores_all = [e["score"] for e in etudiants.values()]
                    moy_all = sum(scores_all)/len(scores_all) if scores_all else 0
                    story.append(Paragraph(
                        "<b>Effectif :</b> " + str(len(etudiants)) +
                        "  |  <b>Moyenne :</b> " + "{:.2f}".format(moy_all) +
                        "  |  <b>Génération :</b> " + datetime.now().strftime("%d/%m/%Y"), stat_s))
                    story.append(Spacer(1, 0.3*cm))

                    tdata = [["Rang","Nom Étudiant","Score","Mention","Opérations"]]
                    for rang, (eid, e) in enumerate(sorted_etudiants, 1):
                        mention, _ = get_mention(e["score"])
                        tdata.append([str(rang), ar_pdf(e["nom"]), str(e["score"]), mention, str(len(e["historique"]))])
                    tdata.append(["—","MOYENNE CLASSE","{:.2f}".format(moy_all),"—","—"])

                    t = Table(tdata, colWidths=[1.5*cm, 7*cm, 2.5*cm, 3*cm, 3*cm], repeatRows=1)
                    ts_list = [
                        ("BACKGROUND",    (0,0),(-1,0),  TEAL),
                        ("TEXTCOLOR",     (0,0),(-1,0),  rl_colors.white),
                        ("FONTNAME",      (0,0),(-1,0),  "Helvetica-Bold"),
                        ("FONTSIZE",      (0,0),(-1,-1), 9),
                        ("ALIGN",         (0,0),(-1,-1), "CENTER"),
                        ("FONTNAME",      (1,1),(1,-2),  ar_font),
                        ("ALIGN",         (1,1),(1,-2),  "RIGHT"),
                        ("GRID",          (0,0),(-1,-1), 0.4, rl_colors.HexColor("#C8D8D5")),
                        ("TOPPADDING",    (0,0),(-1,-1), 6),
                        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                        ("BACKGROUND",    (0,-1),(-1,-1), GOLD),
                        ("FONTNAME",      (0,-1),(-1,-1), "Helvetica-Bold"),
                    ]
                    for rang, (eid, e) in enumerate(sorted_etudiants, 1):
                        fill = GREEN if e["score"] >= 10 else RED
                        ts_list.append(("BACKGROUND", (0,rang), (-1,rang), fill))
                    t.setStyle(TableStyle(ts_list))
                    story.append(t)
                    doc.build(story)
                    pdf_buf.seek(0)

                    st.download_button("📄 Exporter PDF",
                        data=pdf_buf,
                        file_name=cls["nom"] + "_classement.pdf",
                        mime="application/pdf",
                        key="dl_cls_pdf")
                except ImportError:
                    st.info("Ajoutez `reportlab` à requirements.txt")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # ── SOUS-TAB 3 : Historique ─────────────────────────────────────
        # ========================= PARTIE 3b =========================
# Onglet Gérer la classe – Historique, Gérer et Footer

        # ── SOUS-TAB 3 : Historique ─────────────────────────────────────
        with stab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📜 Historique des notes</div>', unsafe_allow_html=True)

            etudiants = cls["etudiants"]
            etudiant_names = {eid: e["nom"] for eid, e in etudiants.items()}
            selected_etud = st.selectbox("Choisir un étudiant",
                                          options=["Tous"] + list(etudiant_names.keys()),
                                          format_func=lambda x: "Tous les étudiants" if x == "Tous" else etudiant_names[x])

            if selected_etud == "Tous":
                # Historique global
                all_hist = []
                for eid, e in etudiants.items():
                    for h in e["historique"]:
                        all_hist.append({
                            "Date":     h.get("date","—"),
                            "Étudiant": e["nom"],
                            "Note":     h.get("note", 0),
                            "Motif":    h.get("motif","—") or "—",
                            "Type":     "Global" if h.get("type")=="global" else "Individuel"
                        })
                if all_hist:
                    df_hist = pd.DataFrame(all_hist).sort_values("Date", ascending=False)
                    st.dataframe(df_hist, use_container_width=True, hide_index=True)
                else:
                    st.info("Aucune note saisie pour l'instant.")
            else:
                e = etudiants[selected_etud]
                st.markdown(
                    '<b style="font-size:16px">' + e["nom"] + '</b>'
                    ' &nbsp;— Score total : <b style="color:#00796B;font-size:18px">'
                    + str(e["score"]) + '</b>',
                    unsafe_allow_html=True
                )
                if e["historique"]:
                    df_h = pd.DataFrame(e["historique"]).rename(columns={
                        "note":"Note","motif":"Motif","date":"Date","type":"Type"})
                    df_h["Type"] = df_h["Type"].map({"global":"Global","indiv":"Individuel"}).fillna("—")
                    df_h = df_h[["Date","Note","Motif","Type"]].sort_values("Date", ascending=False)
                    st.dataframe(df_h, use_container_width=True, hide_index=True)
                    # Graphique d'évolution
                    cumul = []
                    running = 0
                    for h in reversed(e["historique"]):
                        running += h.get("note", 0)
                        cumul.append(running)
                    st.line_chart(pd.DataFrame({"Score cumulé": cumul}), height=200)
                else:
                    st.info("Aucune note pour cet étudiant.")

            st.markdown('</div>', unsafe_allow_html=True)

        # ── SOUS-TAB 4 : Gérer ─────────────────────────────────────────
        with stab4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">⚙️ Gestion de la classe — ' + cls["nom"] + '</div>', unsafe_allow_html=True)

            etudiants = cls["etudiants"]

            # Modifier un étudiant
            st.markdown("**✏️ Modifier un étudiant**")
            eid_to_edit = st.selectbox("Étudiant à modifier",
                                        options=list(etudiants.keys()),
                                        format_func=lambda x: etudiants[x]["nom"],
                                        key="edit_select")
            col_edit1, col_edit2, col_edit3 = st.columns([3,2,1])
            with col_edit1:
                new_nom = st.text_input("Nouveau nom", value=etudiants[eid_to_edit]["nom"], key="new_nom")
            with col_edit2:
                new_score = st.number_input("Réinitialiser le score", value=etudiants[eid_to_edit]["score"], step=1, key="new_score")
            with col_edit3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Sauver", key="save_edit"):
                    etudiants[eid_to_edit]["nom"]   = new_nom.strip()
                    etudiants[eid_to_edit]["score"] = int(new_score)
                    save_db(db)
                    st.success("✅ Modifié !")
                    st.rerun()

            st.markdown("---")

            # Ajouter un étudiant
            st.markdown("**➕ Ajouter un étudiant**")
            col_add1, col_add2 = st.columns([4,1])
            with col_add1:
                new_student = st.text_input("Nom du nouvel étudiant", key="add_student")
            with col_add2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("➕ Ajouter", key="btn_add"):
                    if new_student.strip():
                        new_id = str(max([int(k) for k in etudiants.keys()], default=-1) + 1)
                        etudiants[new_id] = {"nom": new_student.strip(), "score": 0, "historique": []}
                        save_db(db)
                        st.success("✅ Étudiant ajouté !")
                        st.rerun()

            st.markdown("---")

            # Supprimer un étudiant
            st.markdown("**🗑️ Supprimer un étudiant**")
            eid_to_del = st.selectbox("Étudiant à supprimer",
                                       options=list(etudiants.keys()),
                                       format_func=lambda x: etudiants[x]["nom"],
                                       key="del_select")
            if st.button("🗑️ Supprimer " + etudiants[eid_to_del]["nom"], key="btn_del"):
                st.session_state.confirm_delete = eid_to_del

            if st.session_state.confirm_delete == eid_to_del and eid_to_del in etudiants:
                st.warning("⚠️ Confirmer la suppression de **" + etudiants[eid_to_del]["nom"] + "** ?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Confirmer", key="confirm_del"):
                        del etudiants[eid_to_del]
                        save_db(db)
                        st.session_state.confirm_delete = None
                        st.success("Étudiant supprimé.")
                        st.rerun()
                with c2:
                    if st.button("❌ Annuler", key="cancel_del"):
                        st.session_state.confirm_delete = None
                        st.rerun()

            st.markdown("---")

            # Supprimer toute la classe
            st.markdown("**⛔ Supprimer toute la classe**")
            if st.button("⛔ Supprimer la classe " + cls["nom"], key="del_class"):
                st.session_state.confirm_delete = "CLASS_" + selected
            if st.session_state.confirm_delete == "CLASS_" + selected:
                st.error("⚠️ Cette action est irréversible ! Supprimer la classe **" + cls["nom"] + "** ?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Oui, supprimer", key="confirm_del_class"):
                        del db[selected]
                        save_db(db)
                        st.session_state.selected_class = None
                        st.session_state.confirm_delete = None
                        st.success("Classe supprimée.")
                        st.rerun()
                with c2:
                    if st.button("❌ Annuler", key="cancel_del_class"):
                        st.session_state.confirm_delete = None
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="app-footer">
    <span class="badge">Gestion Classe v1.0</span> &nbsp;|&nbsp;
    Suivi des notes de comportement &nbsp;|&nbsp;
    {datetime.now().strftime('%Y')}
</div>
""", unsafe_allow_html=True)
