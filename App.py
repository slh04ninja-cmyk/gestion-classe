# ========================= APP VERSION PRO =========================
import streamlit as st
from datetime import datetime
import io

st.set_page_config(
    page_title="Gestion de Classe PRO",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────── LOAD CSS ────────────
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ──────────── SESSION STATE INIT ────────────
if "etudiants" not in st.session_state:
    st.session_state.etudiants = {
        "1": {
            "nom": "Ahmed Benali",
            "score": 12,
            "historique": [
                {"note": 3, "date": "01/04/2026 09:15"},
                {"note": 5, "date": "02/04/2026 10:30"},
                {"note": 4, "date": "03/04/2026 08:00"},
            ],
        },
        "2": {
            "nom": "Fatima Zahra",
            "score": 3,
            "historique": [
                {"note": 2, "date": "01/04/2026 09:20"},
                {"note": 1, "date": "02/04/2026 10:35"},
            ],
        },
        "3": {
            "nom": "Youssef Alami",
            "score": 18,
            "historique": [
                {"note": 6, "date": "01/04/2026 09:10"},
                {"note": 5, "date": "02/04/2026 10:25"},
                {"note": 4, "date": "03/04/2026 08:05"},
                {"note": 3, "date": "04/04/2026 11:00"},
            ],
        },
        "4": {
            "nom": "Sara Mansouri",
            "score": 7,
            "historique": [
                {"note": 4, "date": "02/04/2026 11:00"},
                {"note": 3, "date": "03/04/2026 09:15"},
            ],
        },
    }

etudiants = st.session_state.etudiants


# ──────────── HELPERS ────────────
def get_mention(score):
    if score >= 15:
        return "Excellent", "excellent"
    elif score >= 10:
        return "Passable", "passable"
    return "Échec", "echec"


def get_initials(nom):
    parts = nom.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return nom[0:2].upper()


def get_total_positive(eid):
    return sum(h["note"] for h in etudiants[eid]["historique"] if h["note"] > 0)


def get_total_negative(eid):
    return sum(h["note"] for h in etudiants[eid]["historique"] if h["note"] < 0)


def export_csv():
    lines = ["Nom,Score,Mention"]
    for eid, e in etudiants.items():
        mention, _ = get_mention(e["score"])
        lines.append(f'"{e["nom"]}",{e["score"]},{mention}')
    return "\n".join(lines).encode("utf-8")


def export_history_csv():
    lines = ["Nom,Note,Date"]
    for eid, e in etudiants.items():
        for h in e["historique"]:
            lines.append(f'"{e["nom"]}",{h["note"]},"{h["date"]}"')
    return "\n".join(lines).encode("utf-8")


# ──────────── SIDEBAR ────────────
with st.sidebar:
    st.markdown("## Ajouter un étudiant")
    with st.form("add_student_form", clear_on_submit=True):
        new_name = st.text_input("Nom complet", placeholder="Ex: Karim Haddad")
        new_score = st.number_input("Score initial", value=0, step=1)
        submitted = st.form_submit_button("Ajouter")

        if submitted and new_name.strip():
            new_id = str(max(int(k) for k in etudiants.keys()) + 1) if etudiants else "1"
            etudiants[new_id] = {
                "nom": new_name.strip(),
                "score": int(new_score),
                "historique": [],
            }
            st.success(f"**{new_name.strip()}** ajouté avec succès !")
            st.rerun()

    st.markdown("---")
    st.markdown("## Exporter les données")

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.markdown('<div class="dl-excel">', unsafe_allow_html=True)
        st.download_button(
            label="Scores (CSV)",
            data=export_csv(),
            file_name="scores.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col_dl2:
        st.markdown('<div class="dl-pdf">', unsafe_allow_html=True)
        st.download_button(
            label="Historique (CSV)",
            data=export_history_csv(),
            file_name="historique.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Réinitialiser")
    if st.button("Tout effacer", use_container_width=True):
        st.session_state.etudiants = {}
        st.rerun()


# ──────────── HEADER ────────────
total_students = len(etudiants)
avg_score = sum(e["score"] for e in etudiants.values()) / total_students if total_students else 0
passed = sum(1 for e in etudiants.values() if e["score"] >= 10)

st.markdown(
    f"""
    <div class="app-header">
        <div class="app-tag">Système de gestion</div>
        <div class="app-title">Gestion de Classe PRO</div>
        <div class="app-sub">Suivi des scores et performances des étudiants</div>
        <div class="header-stats">
            <div class="header-stat">
                <div class="header-stat-val">{total_students}</div>
                <div class="header-stat-label">Étudiants</div>
            </div>
            <div class="header-stat">
                <div class="header-stat-val">{avg_score:.1f}</div>
                <div class="header-stat-label">Moyenne</div>
            </div>
            <div class="header-stat">
                <div class="header-stat-val">{passed}</div>
                <div class="header-stat-label">Réussite</div>
            </div>
            <div class="header-stat">
                <div class="header-stat-val">{total_students - passed}</div>
                <div class="header-stat-label">Échec</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────── TABS ────────────
tab_list, tab_stats, tab_history = st.tabs(
    ["Liste des étudiants", "Statistiques", "Historique complet"]
)


# ════════════════════════════════════════════
# TAB 1 : LISTE DES ÉTUDIANTS
# ════════════════════════════════════════════
with tab_list:
    if not etudiants:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-text">Aucun étudiant enregistré</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Sort by score descending
        sorted_students = sorted(etudiants.items(), key=lambda x: x[1]["score"], reverse=True)

        for rank, (eid, etudiant) in enumerate(sorted_students, 1):
            score = etudiant["score"]
            mention, mention_class = get_mention(score)
            initials = get_initials(etudiant["nom"])
            total_pos = get_total_positive(eid)
            total_neg = get_total_negative(eid)
            last_activity = etudiant["historique"][-1]["date"] if etudiant["historique"] else "—"

            st.markdown(
                f"""
                <div class="student-card {mention_class}">
                    <div class="student-info">
                        <div class="student-avatar">{initials}</div>
                        <div class="student-details">
                            <div class="student-name">#{rank} {etudiant["nom"]}</div>
                            <div class="student-meta">
                                Dernière activité : {last_activity}
                                &nbsp;·&nbsp;
                                <span style="color:#2E7D32">+{total_pos}</span>
                                &nbsp;/&nbsp;
                                <span style="color:#D32F2F">{total_neg}</span>
                            </div>
                        </div>
                    </div>
                    <div class="student-right">
                        <div class="student-score-wrap">
                            <div class="student-score">{score}</div>
                            <div class="student-score-label">points</div>
                        </div>
                        <span class="mention-badge mention-{mention_class}">{mention}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Action buttons
            col_btn1, col_btn2, col_spacer, col_del = st.columns([1, 1, 4, 1.5])

            with col_btn1:
                if st.button("+1", key=f"plus_{eid}", use_container_width=True):
                    etudiants[eid]["score"] += 1
                    etudiants[eid]["historique"].append(
                        {"note": 1, "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
                    )
                    st.rerun()

            with col_btn2:
                if st.button("−1", key=f"moins_{eid}", use_container_width=True):
                    etudiants[eid]["score"] -= 1
                    etudiants[eid]["historique"].append(
                        {"note": -1, "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
                    )
                    st.rerun()

            with col_del:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button("Supprimer", key=f"del_{eid}", use_container_width=True):
                    del etudiants[eid]
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 : STATISTIQUES
# ════════════════════════════════════════════
with tab_stats:
    if not etudiants:
        st.info("Ajoutez des étudiants pour voir les statistiques.")
    else:
        scores = [e["score"] for e in etudiants.values()]
        max_score = max(scores)
        min_score = min(scores)
        median_score = sorted(scores)[len(scores) // 2]

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Moyenne", f"{avg_score:.1f}")
        with col_m2:
            st.metric("Maximum", str(max_score))
        with col_m3:
            st.metric("Minimum", str(min_score))
        with col_m4:
            st.metric("Médiane", str(median_score))

        st.markdown("---")

        # Distribution
        st.markdown('<div class="card-title">Répartition des mentions</div>', unsafe_allow_html=True)
        excellent_count = sum(1 for s in scores if s >= 15)
        passable_count = sum(1 for s in scores if 10 <= s < 15)
        echec_count = sum(1 for s in scores if s < 10)

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.markdown(
                f"""
                <div style="background:#E8F5E9; border-radius:16px; padding:20px; text-align:center; border:1px solid rgba(46,125,50,0.2);">
                    <div style="font-size:36px; font-weight:900; color:#2E7D32; font-family:'Space Mono',monospace;">{excellent_count}</div>
                    <div style="font-size:12px; font-weight:700; color:#2E7D32; text-transform:uppercase; letter-spacing:1px;">Excellent (≥15)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_d2:
            st.markdown(
                f"""
                <div style="background:#E0F2F1; border-radius:16px; padding:20px; text-align:center; border:1px solid rgba(0,121,107,0.2);">
                    <div style="font-size:36px; font-weight:900; color:#00796B; font-family:'Space Mono',monospace;">{passable_count}</div>
                    <div style="font-size:12px; font-weight:700; color:#00796B; text-transform:uppercase; letter-spacing:1px;">Passable (10-14)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_d3:
            st.markdown(
                f"""
                <div style="background:#FFEBEE; border-radius:16px; padding:20px; text-align:center; border:1px solid rgba(211,47,47,0.2);">
                    <div style="font-size:36px; font-weight:900; color:#D32F2F; font-family:'Space Mono',monospace;">{echec_count}</div>
                    <div style="font-size:12px; font-weight:700; color:#D32F2F; text-transform:uppercase; letter-spacing:1px;">Échec (&lt;10)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Classement
        st.markdown('<div class="card-title">Classement</div>', unsafe_allow_html=True)
        ranked = sorted(etudiants.items(), key=lambda x: x[1]["score"], reverse=True)
        for pos, (eid, e) in enumerate(ranked, 1):
            medal = "🥇" if pos == 1 else ("🥈" if pos == 2 else ("🥉" if pos == 3 else f"#{pos}"))
            st.markdown(
                f"**{medal}** &nbsp; {e['nom']} — **{e['score']} pts**"
            )


# ════════════════════════════════════════════
# TAB 3 : HISTORIQUE COMPLET
# ════════════════════════════════════════════
with tab_history:
    if not etudiants:
        st.info("Aucun historique disponible.")
    else:
        eid_selected = st.selectbox(
            "Sélectionner un étudiant",
            options=list(etudiants.keys()),
            format_func=lambda x: etudiants[x]["nom"],
        )

        if eid_selected:
            e = etudiants[eid_selected]
            mention, _ = get_mention(e["score"])

            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                st.metric("Score actuel", e["score"])
            with col_h2:
                st.metric("Total opérations", len(e["historique"]))
            with col_h3:
                st.metric("Mention", mention)

            st.markdown("---")

            if not e["historique"]:
                st.info("Aucune opération enregistrée pour cet étudiant.")
            else:
                st.markdown(
                    '<div class="card-title">Dernières opérations</div>',
                    unsafe_allow_html=True,
                )
                # Show history in reverse chronological order
                for h in reversed(e["historique"]):
                    css_class = "positive" if h["note"] > 0 else "negative"
                    sign = "+" if h["note"] > 0 else ""
                    st.markdown(
                        f"""
                        <div class="history-entry {css_class}">
                            <span>{sign}{h["note"]} point(s)</span>
                            <span class="history-date">{h["date"]}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ──────────── FOOTER ────────────
st.markdown(
    """
    <div class="app-footer">
        Gestion de Classe PRO &nbsp;·&nbsp; Année scolaire 2025–2026 &nbsp;·&nbsp; Développé avec Streamlit
    </div>
    """,
    unsafe_allow_html=True,
    )
                         
