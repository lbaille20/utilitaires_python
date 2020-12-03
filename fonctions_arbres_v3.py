class Noeud:
    def __init__(self, g, v, d):
        self.gauche = g
        self.valeur = v
        self.droit  = d
    def __repr__(self):
        return 'Noeud(' + str(self.gauche) + ', ' + str(self.valeur) + ', ' + str(self.droit) +')'

def _hauteur(a):
    """La hauteur de L'arbre a"""
    if a is None:
        return 0
    else:
        return 1 + max(_hauteur(a.gauche), _hauteur(a.droit))

def _complet(h):
    ## cas de base : arbre réduit à un noeud (feuille)
    if h == 0:
        return Noeud(None, 'x', None)
    ## cas général
    return Noeud(_complet(h - 1), 'x', _complet(h - 1))

def _complet_no(h, p = 1):
    ## cas de base : arbre réduit à un noeud (feuille)
    if h == - 1:
        return None
    ## cas général
    return Noeud(_complet_no(h - 1, 2 * p), p, _complet_no(h - 1, 2 * p + 1))

# Principe pour la reprÃ©sentation graphique :  
# - pour un arbre de hauteur $h$, il y a au maximum $2^h$ noeuds (feuilles), Ã  la profondeur $h$, ces noeuds seront centrÃ©s en des points sÃ©parÃ©s d'une distance $d$ ;
# - les diffÃ©rents niveaux de l'arbre seront sÃ©parÃ©s d'une distance $d_v$ ;
# - le parent de deux noeuds gauche et droit sera reprÃ©sentÃ© Ã  l'abscisse milieu de celle de ses fils.

# Dimensions de la figure :  
# - largeur : $2^h-1 \times d$ 
# - hauteur : $h \times d_v$.


#%matplotlib inline
#import matplotlib.pyplot as plt


# no axes  
# https://stackoverflow.com/questions/9295026/matplotlib-plots-removing-axis-legends-and-white-spaces

# * circles   
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Circle.html  
# https://matplotlib.org/3.3.3/gallery/style_sheets/ggplot.html#sphx-glr-gallery-style-sheets-ggplot-py

# %matplotlib inline
# import matplotlib.pyplot as plt
# 
# fig, ax = plt.subplots()
# 
# ax.add_patch(plt.Circle((0, 0), radius=0.3))
# ax.axis('equal')
# 
# plt.show()

# %matplotlib inline
# import matplotlib.pyplot as plt
# 
# fig, ax = plt.subplots()
# 
# ax.add_patch(plt.Circle((0, 0), radius=0.3))
# ax.axis('equal')
# 
# plt.show()

# ![affiche_arbre_prep.png](attachment:affiche_arbre_prep.png)

# $d(prof)=1/2 * d(prof-1)$  
# $d(prof) = 2^{h-prof}\times d$


# In[5]:


def dist(prof, h, d):
    return 2**(h - prof) * d
def x_min(prof, h, d):
    return (2**p - 1) / 2 * dist(prof, h, d)
def x(no, prof, h, d):
    return x_min(prof, h, d) + dist(prof, h, d) * (no - 2**prof)

def affiche_a(ax, a, h, prof = 0, no = 1, d = 4, dv = 2,
              rayon = 0.5,
              edgecolor = 'black', facecolor = 'white', 
              fontsize = 18,
              halign='center',
              valign='center',
              labels = True,
              decoration = True,
              show_empty = False):
    if a is None:
        return None
    #print(a)
    #print(a.gauche)
    x_min = - (2**prof - 1) / 2 * dist(prof, h, d)
    x, y = x_min + dist(prof, h, d) * (no - 2 ** prof), - prof * dv
    #print(a.valeur, prof, 'x_min =', x_min, x, y)
    #plt.scatter(x, y, color = color)
    ## étiquettes
    if labels:
        plt.text(x, y, a.valeur, fontsize = fontsize, horizontalalignment = halign, verticalalignment = valign)
    ## cerclage
    if decoration:
        ax.add_patch(plt.Circle((x, y), radius=rayon, edgecolor = 'black', facecolor = facecolor))
    ## 
    x_ori, y_ori = x, y
    x_ext, y_ext = x - dist(prof, h, d) / 4, y - dv
    xvec, yvec = x_ext - x_ori, y_ext - y_ori
    lg = (xvec**2 + yvec**2)**0.5
    lgr = lg - rayon
    angle = np.arctan(yvec/xvec)
    if a.gauche is not None or show_empty:
        #print(x, y)
        plt.plot([x - np.cos(angle) * rayon, x - np.cos(angle) * lgr],
                 [y - np.sin(angle) * rayon, y - np.sin(angle) * lgr], color = 'black')
    if a.droit is not None or show_empty:
        #print(x, y)
        plt.plot([x + np.cos(angle) * rayon, x + np.cos(angle) * lgr],
                 [y - np.sin(angle) * rayon, y - np.sin(angle) * lgr], color = 'black')
    affiche_a(ax, a.gauche, h, prof + 1, 2 * no,
              d = d, dv = dv,
              rayon = rayon, 
              edgecolor = edgecolor, facecolor = facecolor,
              fontsize = fontsize, halign = halign, valign = valign,
              labels = labels, decoration = decoration, show_empty = show_empty)
    affiche_a(ax, a.droit,  h, prof + 1, 2 * no + 1,
              d = d, dv = dv,
              rayon = rayon, 
              edgecolor = edgecolor, facecolor = facecolor,
              fontsize = fontsize, halign = halign, valign = valign,
              labels = labels, decoration = decoration, show_empty = show_empty)

def affiche_arbre(a, prof = 0, no = 1, d = 1, dv = 2,
                  edgecolor = 'black', facecolor = 'white', rayon = 0.5,
                  fontsize = 18,
                  halign='center',
                  valign='center',
                  cadre = False,
                  padding = 1,
                  labels = True,
                  decoration = True,
                  show_empty = False):
    """affiche un arbre binaire et les étiquettes de ses noeuds"""
    h = _hauteur(a)
    nb_noeuds_max = 2**h
    hauteur_fig = (h + 1) * dv + padding
    largeur_fig = 20
    import matplotlib.pyplot as plt
    import numpy as np
    xmin, xmax, ymin, ymax = -10, 10, 0, - hauteur_fig
    fig, ax = plt.subplots(figsize=(20,4))
    affiche_a(ax, a, h, prof = 0, no = 1, d = d, dv = dv,
              edgecolor = edgecolor, facecolor = facecolor,
              rayon = rayon, fontsize = fontsize, halign = halign, valign = valign,
              labels = labels, decoration = decoration, show_empty = show_empty)
    if cadre:
        plt.plot([xmin, xmax, xmax, xmin, xmin],
                 [ymin, ymin, ymax, ymax, ymin],
                 color = 'black')
    plt.axis('equal')
    plt.axis('off')
    plt.show()

## aliases
aff = lambda a: affiche_arbre(a)
aff1 = lambda a: affiche_arbre(a, decoration = False, show_empty = True)
aff2 = lambda a: affiche_arbre(a, show_empty = True)



## importations nécessaires
import matplotlib.pyplot as plt
import numpy as np



