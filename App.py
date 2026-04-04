# ========================= GESTION DE CLASSE PRO =========================
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Gestion de Classe PRO",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────── LOAD CSS ────────────
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ──────────── SESSION STATE INIT ────────────
if "classes" not in st.session_state:
    st.session_state.classes = {
        "1A": {
            "nom": "1ère Année — Informatique",
            "etudiants": {
                "1A-1": {
                    "nom": "Ahmed Benali",
                    "score": 12,
                    "historique": [
                        {"note": 3, "date": "01/04/2026 09:15"},
                        {"note": 5, "date": "02/04/2026 10:30"},
                        {"note": 4, "date": "03/04/2026 08:00"},
                    ],
                },
                "1A-2": {
                    "nom": "Fatima Zahra",
                    "score": 3,
                    "historique": [
                        {"note": 2, "date": "01/04/2026 09:20"},
                        {"note": 1, "date": "02/04/2026 10:35"},
                    ],
                },
                "1A-3": {
                    "nom": "Youssef Alami",
                    "score": 18,
                    "historique": [
                        {"note": 6, "date": "01/04/2026 09:10"},
                        {"note": 5, "date": "02/04/2026 10:25"},
                        {"note": 4, "date": "03/04/2026 08:05"},
                        {"note": 3, "date": "04/04/2026 11:00"},
                    ],
                },
            },
        },
        "2B": {
            "nom": "2ème Année — Mathématiques",
            "etudiants": {
                "2B-1": {
                    "nom": "Sara Mansouri",
                    "score": 7,
                    "historique": [
                        {"note": 4, "date": "02/04/2026 11:00"},
                        {"note": 3, "date": "03/04/2026 09:15"},
                    ],
                },
                "2B-2": {
                    "nom": "Karim Haddad",
                    "score": 14,
                    "historique": [
                        {"note": 7, "date": "01/04/2026 08:00"},
                        {"note": 7, "date": "03/04/2026 10:00"},
                    ],
                },
            },
        },
    }

classes = st.session_state.classes


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


def export_csv():
    lines = ["Classe,Nom,Score,Mention"]
    for cid, c in classes.items():
        for eid, e in c["etudiants"].items():
            mention, _ = get_mention(e["score"])
            lines.append(f'"{c["nom"]}","{e["nom"]}",{e["score"]},{mention}')
    return "\n".join(lines).encode("utf-8")


def export_history_csv():
    lines = ["Classe,Nom,Note,Date"]
    for cid, c in classes.items():
        for eid, e in c["etudiants"].items():
            for h in e["historique"]:
                lines.append(f'"{c["nom"]}","{e["nom"]}",{h["note"]},"{h["date"]}"')
    return "\n".join(lines).encode("utf-8")


# ──────────── SIDEBAR ────────────
with st.sidebar:
    st.markdown("## Gestion")

    # ── Ajouter une classe ──
    with st.expander("Ajouter une classe", expanded=True):
        with st.form("form_add_class", clear_on_submit=True):
            class_id = st.text_input("Code classe", placeholder="Ex: 3C")
            class_name = st.text_input("Nom de la classe", placeholder="Ex: 3ème Année — Physique")
            if st.form_submit_button("Créer la classe"):
                if class_id.strip() and class_name.strip():
                    cid = class_id.strip().upper()
                    if cid not in classes:
                        classes[cid] = {"nom": class_name.strip(), "etudiants": {}}
                        st.success(f"Classe **{cid}** créée !")
                        st.rerun()
                    else:
                        st.error(f"La classe **{cid}** existe déjà.")

    # ── Ajouter un étudiant ──
    if classes:
        with st.expander("Ajouter un étudiant", expanded=True):
            with st.form("form_add_student", clear_on_submit=True):
                target_class = st.selectbox(
                    "Classe",
                    options=list(classes.keys()),
                    format_func=lambda x: f"{x} — {classes[x]['nom']}",
                )
                new_name = st.text_input("Nom complet", placeholder="Ex: Karim Haddad")
                new_score = st.number_input("Score initial", value=0, step=1)
                if st.form_submit_button("Ajouter l'étudiant"):
                    if new_name.strip():
                        etuds = classes[target_class]["etudiants"]
                        new_eid = f"{target_class}-{len(etuds) + 1}"
                        etuds[new_eid] = {
                            "nom": new_name.strip(),
                            "score": int(new_score),
                            "historique": [],
                        }
                        st.success(f"**{new_name.strip()}** ajouté en **{target_class}** !")
                        st.rerun()

    # ── Supprimer une classe ──
    if classes:
        with st.expander("Supprimer une classe"):
            del_class = st.selectbox(
                "Choisir la classe",
                options=list(classes.keys()),
                format_func=lambda x: f"{x} — {classes[x]['nom']}",
                key="del_class_select",
            )
            if st.button("Supprimer cette classe", type="primary"):
                del classes[del_class]
                st.success(f"Classe **{del_class}** supprimée.")
                st.rerun()

    st.markdown("---")

    # ── Export ──
    st.markdown("## Exporter")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.markdown('<div class="dl-excel">', unsafe_allow_html=True)
        st.download_button(
            "Scores (CSV)",
            data=export_csv(),
            file_name="scores.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col_dl2:
        st.markdown('<div class="dl-pdf">', unsafe_allow_html=True)
        st.download_button(
            "Historique (CSV)",
            data=export_history_csv(),
            file_name="historique.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ──────────── COMPUTE GLOBAL STATS ────────────
all_students = []
for c in classes.values():
    for e in c["etudiants"].values():
        all_students.append(e)

total_students = len(all_students)
avg_score = sum(e["score"] for e in all_students) / total_students if total_students else 0
passed = sum(1 for e in all_students if e["score"] >= 10)
failed = total_students - passed

# ──────────── HEADER ────────────
st.markdown(
    f"""
    <div class="app-header">
        <div class="app-tag">Système de gestion</div>
        <div class="app-title">Gestion de Classe PRO</div>
        <div class="app-sub">Suivi des scores et performances — {len(classes)} classe(s), {total_students} étudiant(s)</div>
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
                <div class="header-stat-val">{failed}</div>
                <div class="header-stat-label">Échec</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ──────────── TABS ────────────
tab_classes, tab_stats, tab_history = st.tabs(
    ["Classes & Étudiants", "Statistiques", "Historique"]
)


# ════════════════════════════════════════════
# TAB 1 : CLASSES & ÉTUDIANTS
# ════════════════════════════════════════════
with tab_classes:
    if not classes:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-text">Aucune classe enregistrée</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for cid, classe in classes.items():
            etudiants = classe["etudiants"]
            nb = len(etudiants)
            moyenne = sum(e["score"] for e in etudiants.values()) / nb if nb else 0

            st.markdown(
                f"""
                <div class="card-title">{cid} — {classe["nom"]}
                    <span style="margin-left:auto; font-size:12px; font-weight:600; color:var(--muted);">
                        {nb} étudiant(s) · Moyenne {moyenne:.1f}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if not etudiants:
                st.info("Aucun étudiant dans cette classe.")
                continue

            sorted_etuds = sorted(etudiants.items(), key=lambda x: x[1]["score"], reverse=True)

            for rank, (eid, etudiant) in enumerate(sorted_etuds, 1):
                score = etudiant["score"]
                mention, mention_class = get_mention(score)
                initials = get_initials(etudiant["nom"])

                # ── Card HTML ──
                st.markdown(
                    f"""
                    <div class="student-card {mention_class}">
                        <div class="student-info">
                            <div class="student-avatar">{initials}</div>
                            <div class="student-details">
                                <div class="student-name">#{rank} {etudiant["nom"]}</div>
                                <div class="student-meta">ID : {eid}</div>
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

                # ── Boutons +1 et -1 sur la même ligne ──
                col_plus, col_moins = st.columns(2)
                with col_plus:
                    st.markdown('<div class="btn-plus">', unsafe_allow_html=True)
                    if st.button("+1", key=f"plus_{eid}", use_container_width=True):
                        etudiants[eid]["score"] += 1
                        etudiants[eid]["historique"].append(
                            {"note": 1, "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
                        )
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with col_moins:
                    st.markdown('<div class="btn-moins">', unsafe_allow_html=True)
                    if st.button("−1", key=f"moins_{eid}", use_container_width=True):
                        etudiants[eid]["score"] -= 1
                        etudiants[eid]["historique"].append(
                            {"note": -1, "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
                        )
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 2 : STATISTIQUES
# ════════════════════════════════════════════
with tab_stats:
    if not all_students:
        st.info("Ajoutez des étudiants pour voir les statistiques.")
    else:
        scores = [e["score"] for e in all_students]
        max_score = max(scores)
        min_score = min(scores)
        sorted_scores = sorted(scores)
        median_score = sorted_scores[len(sorted_scores) // 2]

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

        # ── Classement global ──
        st.markdown('<div class="card-title">Classement global</div>', unsafe_allow_html=True)
        ranked = sorted(all_students, key=lambda x: x["score"], reverse=True)
        for pos, e in enumerate(ranked, 1):
            medal = "🥇" if pos == 1 else ("🥈" if pos == 2 else ("🥉" if pos == 3 else f"#{pos}"))
            st.markdown(f"**{medal}** &nbsp; {e['nom']} — **{e['score']} pts**")


# ════════════════════════════════════════════
# TAB 3 : HISTORIQUE
# ════════════════════════════════════════════
with tab_history:
    if not all_students:
        st.info("Aucun historique disponible.")
    else:
        # Build a flat list for the selectbox
        student_options = []
        for cid, c in classes.items():
            for eid, e in c["etudiants"].items():
                student_options.append((eid, f"{e['nom']} ({cid})"))

        selected = st.selectbox(
            "Sélectionner un étudiant",
            options=[opt[0] for opt in student_options],
            format_func=dict(student_options).get,
        )

        # Find the student
        target = None
        for c in classes.values():
            if selected in c["etudiants"]:
                target = c["etudiants"][selected]
                break

        if target:
            mention, _ = get_mention(target["score"])

            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                st.metric("Score actuel", target["score"])
            with col_h2:
                st.metric("Total opérations", len(target["historique"]))
            with col_h3:
                st.metric("Mention", mention)

            st.markdown("---")

            if not target["historique"]:
                st.info("Aucune opération enregistrée.")
            else:
                st.markdown('<div class="card-title">Dernières opérations</div>', unsafe_allow_html=True)
                for h in reversed(target["historique"]):
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
        Gestion de Classe PRO · Année scolaire 2025–2026 · Développé avec Streamlit
    </div>
    """,
    unsafe_allow_html=True,
        )
                        
