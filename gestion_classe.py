import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime

st.set_page_config(
    page_title="Gestion de Classe",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
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

/* ── Student card ── */
.student-row {
    display:flex; align-items:center; justify-content:space-between;
    background:#F8FAFA; border:1px solid var(--border); border-radius:12px;
    padding:12px 16px; margin-bottom:8px; gap:10px; flex-wrap:wrap;
}
.student-name { font-weight:800; font-size:15px; color:var(--text); flex:1; min-width:150px; }
.student-score {
    font-size:28px; font-weight:900; color:var(--teal2);
    min-width:50px; text-align:center;
}
.score-pos { color:#2E7D32; }
.score-neg { color:var(--red); }
.score-zero { color:var(--muted); }
.badge-mention {
    display:inline-block; padding:3px 12px; border-radius:20px;
    font-size:11px; font-weight:800; letter-spacing:0.5px;
}
.m-tb  { background:#E8F5E9; color:#1B5E20; border:1px solid #A5D6A7; }
.m-b   { background:#E3F2FD; color:#0D47A1; border:1px solid #90CAF9; }
.m-ab  { background:#FFF8E1; color:#7B5800; border:1px solid #FFE082; }
.m-p   { background:#FFF3E0; color:#E65100; border:1px solid #FFCC80; }
.m-ec  { background:#FFEBEE; color:#B71C1C; border:1px solid #EF9A9A; }

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

# ── Storage helpers ────────────────────────────────────────────────────────────
STORAGE_KEY = "classes_db"

def load_db():
    """Charge la base depuis Streamlit storage."""
    try:
        raw = st.query_params.get("_db_bypass", None)
        data = st.session_state.get("__db__", None)
        if data is None:
            return {}
        return json.loads(data) if isinstance(data, str) else data
    except Exception:
        return {}

def save_db(db):
    """Sauvegarde la base dans session_state (persisté via query params trick)."""
    st.session_state["__db__"] = db

def get_mention(score):
    if score >= 16:   return "Très Bien",  "m-tb"
    elif score >= 14: return "Bien",        "m-b"
    elif score >= 12: return "Assez Bien",  "m-ab"
    elif score >= 10: return "Passable",    "m-p"
    else:             return "Echec",       "m-ec"

# ── Init session state ─────────────────────────────────────────────────────────
if "__db__" not in st.session_state:
    st.session_state["__db__"] = {}
if "selected_class" not in st.session_state:
    st.session_state.selected_class = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None

db = st.session_state["__db__"]

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-tag">Outil Pédagogique</div>
    <div class="app-title">📚 Gestion de Classe</div>
    <div class="app-sub">Suivi des notes de comportement — Accumulation +1 / -1 / 0</div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR : liste des classes ────────────────────────────────────────────────
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

# ── TABS PRINCIPAL ──────────────────────────────────────────────────────────────
tab_home, tab_new, tab_class = st.tabs(["🏠 Accueil", "➕ Créer une classe", "📋 Gérer la classe"])

# ══════════════════════════════════════════════════════
# TAB ACCUEIL
# ══════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════
# TAB CRÉER UNE CLASSE
# ══════════════════════════════════════════════════════
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
                # Première colonne non vide
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
                save_db(db)
                st.session_state.selected_class = cid
                st.success(f"✅ Classe '{nom_classe}' créée avec {len(etudiants_input)} étudiants !")
                st.balloons()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB GÉRER LA CLASSE
# ══════════════════════════════════════════════════════
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
                save_db(db)
                st.success(f"✅ Note {'+1' if note_globale==1 else ('-1' if note_globale==-1 else '0')} appliquée à toute la classe !")
                st.rerun()

            st.markdown("---")
            st.markdown("**Notes individuelles**")

            # Afficher chaque étudiant
            for eid, etudiant in sorted(etudiants.items(), key=lambda x: x[1]["nom"]):
                score = etudiant["score"]
                score_cls = "score-pos" if score > 0 else ("score-neg" if score < 0 else "score-zero")
                mention, m_cls = get_mention(score)

                col_nom, col_score, col_p, col_z, col_m, col_motif = st.columns([3,1,1,1,1,3])
                with col_nom:
                    st.markdown(
                        '<div style="padding:8px 0;font-weight:700">' + etudiant["nom"] + '</div>',
                        unsafe_allow_html=True
                    )
                with col_score:
                    st.markdown(
                        '<div class="' + score_cls + '" style="font-size:24px;font-weight:900;'
                        'text-align:center;padding:4px">' + str(score) + '</div>',
                        unsafe_allow_html=True
                    )
                with col_p:
                    if st.button("➕", key=f"p_{eid}"):
                        motif = st.session_state.get(f"motif_{eid}", "")
                        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                        etudiants[eid]["score"] += 1
                        etudiants[eid]["historique"].append({"note":1,"motif":motif,"date":ts,"type":"indiv"})
                        save_db(db)
                        st.rerun()
                with col_z:
                    if st.button("⓪", key=f"z_{eid}"):
                        motif = st.session_state.get(f"motif_{eid}", "")
                        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                        etudiants[eid]["historique"].append({"note":0,"motif":motif,"date":ts,"type":"indiv"})
                        save_db(db)
                        st.rerun()
                with col_m:
                    if st.button("➖", key=f"m_{eid}"):
                        motif = st.session_state.get(f"motif_{eid}", "")
                        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
                        etudiants[eid]["score"] -= 1
                        etudiants[eid]["historique"].append({"note":-1,"motif":motif,"date":ts,"type":"indiv"})
                        save_db(db)
                        st.rerun()
                with col_motif:
                    st.text_input("Motif", key=f"motif_{eid}", label_visibility="collapsed",
                                  placeholder="Motif (optionnel)")

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

            # Export
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
