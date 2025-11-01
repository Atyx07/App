import streamlit as st
from rembg import remove  # Bibliothèque principale pour le détourage
from PIL import Image     # Pour manipuler les images
import io                 # Pour gérer les bytes (données binaires)
import time               # Pour mesurer le temps de traitement

# --- Configuration de la page ---
st.set_page_config(
    page_title="Suppresseur d'arrière-plan",
    page_icon="✂️",
    layout="wide"
)

# --- Barre Latérale (Sidebar) pour les options ---
st.sidebar.header("⚙️ Options d'amélioration")
st.sidebar.info(
    "Le modèle 'Haute Précision' est plus lent, mais "
    "souvent meilleur pour les détails complexes ou les sujets multiples (comme du texte)."
)

# Choix du modèle IA
model_name = st.sidebar.radio(
    "Choisissez le modèle IA :",
    ["Standard (U-2-Net)", "Haute Précision (IS-Net)"],
    key="model_choice"
)

# Case à cocher pour l'affinage (Alpha Matting)
# C'est une 2e amélioration : affine les bords (cheveux, fourrure)
use_alpha_matting = st.sidebar.checkbox(
    "Affinage des bords (plus lent)", 
    value=False,
    help="Cochez ceci pour des contours plus fins (cheveux, fourrure). Ne l'utilisez que si nécessaire."
)

# --- Titre et description ---
st.title("✂️ Suppresseur d'arrière-plan d'image")
st.markdown(
    "Téléchargez une image et l'IA enlèvera l'arrière-plan automatiquement."
)
st.info(f"Mode sélectionné : **{model_name}** {'avec affinage' if use_alpha_matting else ''}.")

# --- Colonnes pour l'affichage ---
col1, col2 = st.columns(2)

# --- Colonne 1 : Téléchargement et Image Originale ---
with col1:
    st.header("1. Votre Image")
    
    uploaded_file = st.file_uploader("Choisissez une image...", type=["png", "jpg", "jpeg", "webp"])
    
    if uploaded_file is not None:
        input_bytes = uploaded_file.getvalue()
        input_image = Image.open(io.BytesIO(input_bytes))
        
        st.image(input_image, caption="Image Originale", use_column_width=True)

# --- Colonne 2 : Résultat et Téléchargement ---
with col2:
    st.header("2. Résultat")
    
    if uploaded_file is not None:
        
        # Traduire le choix du radio-bouton en paramètre pour rembg
        if model_name == "Standard (U-2-Net)":
            model_param = "u2net"
        else:
            model_param = "isnet-general-use" # C'est le nom du modèle haute précision

        # Si un fichier a été téléchargé, on lance le traitement
        with st.spinner(f"Magie en cours... (Modèle : {model_param})..."):
            try:
                start_time = time.time()
                
                # --- L'OPÉRATION MAGIQUE (AMÉLIORÉE) ---
                output_bytes = remove(
                    input_bytes,
                    model=model_param,               # On utilise le modèle choisi
                    alpha_matting=use_alpha_matting  # On active ou non l'affinage
                )
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                output_image = Image.open(io.BytesIO(output_bytes))
                
                st.image(output_image, caption="Arrière-plan supprimé", use_column_width=True)
                
                # Afficher le temps de traitement
                st.success(f"Traitement terminé en {processing_time:.2f} secondes.")
                
                file_name = f"{uploaded_file.name.split('.')[0]}_no_bg.png"
                
                st.download_button(
                    label="📥 Télécharger le résultat (PNG)",
                    data=output_bytes,
                    file_name=file_name,
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Une erreur est survenue lors du traitement : {e}")
                st.error("L'image est peut-être corrompue ou dans un format non supporté par le modèle.")
                
    else:
        st.info("Veuillez télécharger une image dans le panneau de gauche pour voir le résultat ici.")

# --- Pied de page ---
st.markdown("---")
st.markdown("Créé avec [Streamlit](https://streamlit.io/) & [rembg](https://github.com/danielgatis/rembg).")
