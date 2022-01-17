#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title=" 14 saisons d'actus sur www.asm-rugby.com - A.Ferlac ",
                   layout='centered',
                   initial_sidebar_state='auto')
st.markdown(
    """
    <style>
    .main {
        background-color:#FFFFC2
        }
    </style>
    """,
    unsafe_allow_html=True
    )
background_color = '#FFFFC2'

# Chargement des dataframes contenant les données
# Actus nettoyées et processées
df1 = pd.read_csv('/.actus_asm_cleaned_1.csv', index_col=0, parse_dates=['date'])
df2 = pd.read_csv('/.actus_asm_cleaned_2.csv', index_col=0)
df=df1.join(df2)
# Actus regroupées par mois sur les 14 saisons
df_douzemois = pd.read_csv('/.moyenne_articles_mois.csv', index_col=0)
# Actus regroupées par mois de l'année
df_stat_mois = pd.read_csv('/.stat_articles_mois.csv', index_col=0)
# Actus regroupées par jour de la semaine
df_stat_semaine = pd.read_csv('/.moyenne_articles_jour.csv', index_col=0)
# Nombre de citations par joueur et par saison
df_joueurasm_actu = pd.read_csv('/.joueur_actuASM_saison.csv', index_col=0)

# Début de la présentation
st.title("14 saisons d'actus sur www.asm-rugby.com")
st.write("""
Depuis septembre 2008, plus de **6400 articles** ont été diffusés sur le site du l'ASM. 
Ils contiennent l'histoire officielle des dernières années de ce club historique du rugby français. \n
Une opération de webscrapping a permis de récupérer la date, le titre, 
le texte de chaque actu ainsi que la catégorie de l'actu et la présence ou non de photo ou vidéo dans l'article.\n
Après la nécessaire opération de nettoyage des données (suppression des actus en double et en japonais), 
un data processing a permis d'ajouter la longueur (nombre de caractères et de mots) du titre et de l'article, 
des listes de mots composant le titre et l'article et des informations complémentaires sur la date 
(jour, mois, année, nombre de jours depuis la première actu) ainsi que la saison rugbystique. Le tableau des données obtenues est visible ci-dessous.""")
# Affichage caché des actus nettoyée et processées
with st.expander('Données'):
        st.write(df)
st.write('---')

# Paragraphe 1
st.header("Que faire de toutes ces données ?")
st.subheader("Regardons tout d'abord la date et la taille des articles")

# Construction du graphe 'fig' : Tailles article et titre vs date
fig = px.scatter(df,
                 x='date',
                 y='nbmot_texte',
                 size='nbmot_titre', 
                 hover_name='titre',
                 hover_data={'date':True,
                             'nbmot_texte':True,
                             'nbmot_titre':True,
                            },
                 labels={'nbmot_texte':"Taille de l'article (mots)",
                         'nbmot_titre':"Taille du titre (mots)",
                        },
                 title="",
                 opacity=0.2,
                 #width=1300, height=800,
                )
fig.update_traces(marker={'line':{'width':0}})
fig.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

st.write("""
Chaque article est représenté par un point 
dont l'ordonnée indique la date de diffusion 
et l'abscisse donne la longueur de l'article, 
la taille du point est fonction de la longueur du titre.\n
Vous pouvez voir le titre de l'article ainsi que sa longueur au survol.\n
Vous pouvez zoomer et vous déplacer dans le graphe avec le menu situé en haut à droite du graphe. 
""") 
st.write(fig)
st.write("""
**La taille des points donc la longueur des articles augmente depuis 2008.**\n
**On remarque également qu'il y a moins de points donc moins d'actus l'été.**""")
st.write('---')

# Paragraphe 2

# Construction du graphe 'fig1' : Tailles article et titre vs mois 
fig1 = px.scatter(df_stat_mois, x='annee_mois', y='moy_mot_texte',
                size='moy_mot_titre',  
                hover_name='annee_mois',
                 hover_data={'annee_mois':False,
                            'moy_mot_texte':True,
                            'moy_mot_titre':True},
                labels={'moy_mot_texte':'longueur article',
                        'moy_mot_titre':'longueur titre',
                        'annee_mois':''},
                 width=800, height=600,
                )
fig1.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

# Construction du graphe 'fig2' : Tailles titre et article vs mois 
fig2 = px.scatter(df_stat_mois, x='annee_mois', y='moy_mot_titre',
                  size='moy_mot_texte', 
                  hover_name='annee_mois',
                  hover_data={'annee_mois':False,
                              'moy_mot_texte':True,
                              'moy_mot_titre':True},
                  range_y=[0,13],
                  labels={'moy_mot_titre':'longueur du titre',
                          'moy_mot_texte':'longueur article',
                          'annee_mois':''},
                  width=800, height=600,
                 )
fig2.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

# Ecriture texte paragraphe 2 et tracé des graphes 'fig1' et 'fig2'
st.write('Un nouveau traitement est effectué pour regrouper les données par mois')
with st.expander('Données par mois'):
        st.write(df_stat_mois)
st.subheader('La longueur du titre augmente puis se stabilise')
st.write(fig2)
st.write("""**La longueur du titre évolue de environ 3 mots en 2008 jusqu'à plus de 6 mots en 2014.** \n
**On constate une rupture de la progression début 2015. 
Depuis cette date la longueur est stable et s'établit la plupart du temps au dessus de 8 mots.**""")
st.subheader("La longueur de l'article augmente régulièrement")
st.write(fig1)
st.write("""**La longueur du texte progresse régulièrement depuis 2008 de environ 300 mots jusqu'à plus de 500 mots.**\n
**On observe que les mois d'été (juin ou juillet) sont souvent plus faibles que les autres points.**""")

st.write('---')

# Paragraphe 3

fig3m = px.bar(df_douzemois, x='mois', y='moy_nbarticle', hover_data={'mois':False, 'moy_nbarticle':True}, labels={'moy_nbarticle':"N", 'mois':''},
             title="Nombre moyen d'articles par mois",)
fig3m.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig4m = px.bar(df_douzemois, x='mois', y='moy_mot_texte', hover_data={'mois':False, 'moy_mot_texte':True}, labels={'moy_mot_texte':"mots",'mois':''},
             title="Moyenne des longueurs d'article par mois",)
fig4m.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig5m = px.bar(df_stat_semaine, x='jour', y='moy_nbarticle',hover_data={'jour':False, 'moy_nbarticle':True},labels={'moy_nbarticle':"N",'jour':''},
              title="Nombre moyen d'articles par jour",)
fig5m.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig6m = px.bar(df_stat_semaine, x='jour', y='moy_mot_texte',hover_data={'jour':False,'moy_mot_texte':True},labels={'moy_mot_texte':'mots','jour':''},
              title="Moyenne des longueurs d'article par jour",)
fig6m.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig3t = px.bar(df_douzemois, x='mois', y='som_nbarticle', hover_data={'mois':False, 'som_nbarticle':True}, labels={'som_nbarticle':"N", 'mois':''},
             title="Nombre total d'articles par mois",)
fig3t.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig4t = px.bar(df_douzemois, x='mois', y='som_mot_texte', hover_data={'mois':False, 'som_mot_texte':True}, labels={'som_mot_texte':"mots",'mois':''},
             title="Somme des longueurs d'article par mois",)
fig4t.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig5t = px.bar(df_stat_semaine, x='jour', y='nbarticle',hover_data={'jour':False, 'nbarticle':True},labels={'nbarticle':"N",'jour':''},
              title="Nombre total d'articles par jour",)
fig5t.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

fig6t = px.bar(df_stat_semaine, x='jour', y='som_mot_texte',hover_data={'jour':False,'som_mot_texte':True},labels={'som_mot_texte':'mots','jour':''},
              title="Somme des longueurs d'article par jour",)
fig6t.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

st.write('''Pour confirmer les observations précédentes, un nouveau traitement est effectué afin d'obtenir des statistiques pour chaque mois de l'année et chaque jour de la semaine.''')
with st.expander("Données par mois de l'année"):
        st.write(df_douzemois)
with st.expander("Données par jour de la semaine"):
        st.write(df_stat_semaine)

st.subheader("En juillet, moins d'actus et actus plus courtes !")
choix1 = st.radio(
     "Choisissez",
     ('Moyenne', 'Total'))

if choix1=='Moyenne':
        st.write(fig3m)
        st.write(fig4m)
else:
        st.write(fig3t)
        st.write(fig4t)
st.subheader("Le week-end, moins d'actus mais actus plus longues !")

if choix1=='Moyenne':
        st.write(fig5m)
        st.write(fig6m)
else:
        st.write(fig5t)
        st.write(fig6t)
st.write('---')
st.write('En utilisant une liste de 161 joueurs, on extrait le nombre de citations de chaque joueur pour chaque saison.')
with st.expander("données des citations par joueur et saison"):
        st.write(df_joueurasm_actu)
st.subheader('Quel joueur est cité le plus souvent depuis 2008 ?')
A=df_joueurasm_actu.groupby('joueur').sum().sort_values(by='occurence_titre',ascending=True).tail(10)
A['joueur']=A.index
B=df_joueurasm_actu.groupby('joueur').sum().sort_values(by='occurence_texte',ascending=True).tail(10)
B['joueur']=B.index
fig7 = px.bar(A, y='joueur', x="occurence_titre", orientation='h',
             title='Les 10 joueurs les plus cités dans le titre depuis 2008',
             labels={'joueur':'','occurence_titre':'Nombre de citations'},
             hover_data={'joueur':False,
                         'occurence_titre':True,
                        },
             height=400,
            )
fig7.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')
fig8 = px.bar(B, y='joueur', x="occurence_texte", orientation='h',
             title='Les 10 joueurs les plus cités dans le texte depuis 2008',
             labels={'joueur':'','occurence_texte':'Nombre de citations'},
             hover_data={'joueur':False,
                         'occurence_texte':True,
                        },
             height=400,
            )
fig8.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')

st.write(fig7)
st.write(fig8)
st.write("**C'est Morgan Parra le numéro 1. Il est cité dans environ une actus sur trois.**")
st.write('---')
st.subheader('Et chaque saison ?')
saison = st.selectbox(
     'Choisir une saison',
     ('2008-2009', '2009-2010','2010-2011','2011-2012','2012-2013','2013-2014','2014-2015',
      '2015-2016','2016-2017','2017-2018','2018-2019','2019-2020','2020-2021','2021-2022'))
selec_titre = df_joueurasm_actu[df_joueurasm_actu['saison']==saison].sort_values(by='occurence_titre', ascending=True).tail(10)
selec_texte = df_joueurasm_actu[df_joueurasm_actu['saison']==saison].sort_values(by='occurence_texte', ascending=True).tail(10)
title_titre = 'Les 10 joueurs les plus cités dans le titre en '+ saison
title_texte = 'Les 10 joueurs les plus cités dans le texte en '+ saison
fig9 = px.bar(selec_titre, y='joueur', x="occurence_titre", orientation='h',
             title=title_titre,
             labels={'joueur':'','occurence_titre':'Nombre de citations'},
             hover_data={'joueur':False,
                         'occurence_titre':True,
                        },
             height=400,
            )
fig9.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')
st.write(fig9)
fig10 = px.bar(selec_texte, y='joueur', x="occurence_texte", orientation='h',
             title=title_texte,
             labels={'joueur':'','occurence_texte':'Nombre de citations'},
             hover_data={'joueur':False,
                         'occurence_texte':True,
                        },
             height=400,
            )
fig10.update_layout(paper_bgcolor=background_color, plot_bgcolor='#d7fffe')
st.write(fig10)
st.write('---')
st.write('''Cette application a été construite sous Python avec les librairies Streamlit, Pandas et Plotly.\n
Les données ont été scrappées et traitées sous Python avec les librairies Request, Beautifulsoup, nlkt, re, numpy et pandas.\n
A. FERLAC - Janvier 2022.''')
st.write('---')
