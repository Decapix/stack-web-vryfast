import streamlit as st




from supabase import create_client, Client

# Configuration de Supabase
SUPABASE_URL = 'votre_supabase_url'
SUPABASE_KEY = 'votre_supabase_anon_key'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Gestion de la session utilisateur
if 'user' not in st.session_state:
    st.session_state.user = None

def login(email, password):
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if response.user:
        st.session_state.user = response.user
        st.success("Connexion réussie !")
    else:
        st.error("Échec de la connexion. Veuillez vérifier vos informations.")

def signup(email, password):
    response = supabase.auth.sign_up({"email": email, "password": password})
    if response.user:
        st.success("Inscription réussie ! Veuillez vérifier votre email pour confirmer votre compte.")
    else:
        st.error("Échec de l'inscription. Veuillez réessayer.")

def logout():
    st.session_state.user = None
    st.success("Déconnexion réussie !")

# Interface utilisateur
st.title("Application To Do avec Authentification")

if st.session_state.user:
    st.write(f"Bienvenue, {st.session_state.user.email}!")
    if st.button("Déconnexion"):
        logout()
else:
    st.write("Veuillez vous connecter ou créer un compte.")

    tab1, tab2 = st.tabs(["Connexion", "Inscription"])

    with tab1:
        st.header("Connexion")
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            login(email, password)

    with tab2:
        st.header("Inscription")
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("S'inscrire"):
            signup(email, password)





# Initialisation de la session state pour stocker les tâches
if 'todos' not in st.session_state:
    st.session_state.todos = []

def add_todo():
    todo = st.session_state.new_todo
    if todo:
        st.session_state.todos.append(todo)
        st.session_state.new_todo = ""

def delete_todo(index):
    if 0 <= index < len(st.session_state.todos):
        del st.session_state.todos[index]

# Interface utilisateur
st.title("To Do App")

st.text_input("Ajouter une nouvelle tâche", key="new_todo")
st.button("Ajouter", on_click=add_todo)

st.write("Liste des tâches:")
for index, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([0.8, 0.2])
    col1.write(todo)
    if col2.button("Supprimer", key=f"delete_{index}"):
        delete_todo(index)
