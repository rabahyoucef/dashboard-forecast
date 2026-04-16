# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:39:33 2026

@author: ELITEBOOK
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG PAGE
st.set_page_config(page_title="Dashboard Prévision", layout="wide")

# TITRE
st.title("📊 Dashboard Prévision Produits")

# LOAD DATA
df = pd.read_excel(r"C:\Users\ELITEBOOK\Desktop\Travail Esquirol\Prévisionnel_Mois_De_Mai_2026 .xlsx")

# NETTOYAGE
df["Palettes_calc"] = (df["Forecast Qté"] / df["Qté/Palette"]).round(0)

# KPI
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Forecast", int(df["Forecast Qté"].sum()))
col2.metric("Total Palettes", int(df["Palettes"].sum()))
col3.metric("Nb Produits", df["Produit"].nunique())
col4.metric("Nb Catégories", df["Catégorie"].nunique())

# FILTRES
st.sidebar.header("Filtres")

marque = st.sidebar.multiselect(
    "Marque",
    options=df["Marque"].unique(),
    default=df["Marque"].unique()
)

categorie = st.sidebar.multiselect(
    "Catégorie",
    options=df["Catégorie"].unique(),
    default=df["Catégorie"].unique()
)

df_filtered = df[
    (df["Marque"].isin(marque)) &
    (df["Catégorie"].isin(categorie))
]

# GRAPHIQUE 1
st.subheader("📊 Forecast par catégorie")
fig1 = px.bar(
    df_filtered.groupby("Catégorie")["Forecast Qté"].sum().reset_index(),
    x="Catégorie",
    y="Forecast Qté",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# GRAPHIQUE 2
st.subheader("📦 Palettes par catégorie")
fig2 = px.bar(
    df_filtered.groupby("Catégorie")["Palettes"].sum().reset_index(),
    x="Catégorie",
    y="Palettes",
    text_auto=True,
    color="Palettes"
)
st.plotly_chart(fig2, use_container_width=True)

# SCATTER (🔥 pro)
st.subheader("🎯 Analyse Volume vs Palettes")
fig3 = px.scatter(
    df_filtered,
    x="Forecast Qté",
    y="Palettes",
    size="Forecast Qté",
    color="Marque",
    hover_name="Produit"
)
st.plotly_chart(fig3, use_container_width=True)

# TOP PRODUITS
st.subheader("🏆 Top Produits")
top = df_filtered.sort_values(by="Forecast Qté", ascending=False)
st.dataframe(top, use_container_width=True)