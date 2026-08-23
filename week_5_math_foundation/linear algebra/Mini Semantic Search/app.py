import streamlit as st
import numpy as np
import embedding as em

st.title("Cosine Similarity")

# ----------------------------
# Load model only once
# ----------------------------
@st.cache_resource
def load_model():
    return em.Cosine_similarity()
sem = load_model()

# ----------------------------
# Session State
# ----------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "query_emb" not in st.session_state:
    st.session_state.query_emb = None

if "query_norm" not in st.session_state:
    st.session_state.query_norm = None

if "query_shape" not in st.session_state:
    st.session_state.query_shape = None

# ----------------------------
# User Input
# ----------------------------
query = st.text_input("Enter the sentence:")

# ----------------------------
# If query changes after submit,
# invalidate previous results
# ----------------------------
if (
    st.session_state.submitted
    and query != st.session_state.last_query
):
    st.session_state.submitted = False

# ----------------------------
# Submit Button
# ----------------------------
if st.button("Submit"):

    if query.strip() == "":
        st.warning("Please enter a valid sentence.")

    else:

        # Expensive computation
        sem.search(query)

        # Store results only once
        st.session_state.query_emb = sem.query_emb
        st.session_state.query_norm = sem.query_norm
        st.session_state.query_shape = np.shape(sem.query_emb)

        st.session_state.last_query = query
        st.session_state.submitted = True

# ----------------------------
# Display Section
# ----------------------------
if st.session_state.submitted:

    st.success("Sentence converted successfully!")

    if st.button("View Query Embedding"):
        st.write(st.session_state.query_emb)

    if st.button("View Query Shape"):
        st.write(st.session_state.query_shape)

    if st.button("View Query Norm"):
        st.write(st.session_state.query_norm)

else:
    if query != "":
        st.info("Click Submit to generate embedding.")