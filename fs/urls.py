from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from fs.forms import AuthenticationFormWithContact


urlpatterns = [

    path('tableau/', views.Dashboard, name="tableau"),
    path('', views.Accueil, name="accueil"),

    #-----------------CONNEXION----------------#

    path('connexion', auth_views.LoginView.as_view(template_name='default/auth-signin.html', authentication_form=AuthenticationFormWithContact), name='connexion'),
    path('accounts/logout/', auth_views. LogoutView.as_view(), name='deconnexion'),


     #-----------------AGENCE----------------#

    path('profil_agence/<str:pkey>', views.ProfilAgence, name="profil_agence"),
    path('ajouter_agence/', views.AjouterAgence, name="ajouter_agence"),
    path('modifier_agence/<str:pkey>', views.ModifierAgence, name="modifier_agence"),
    path('liste_agence/', views.ListeAgence, name="liste_agence"),
    path('supprimer_agence/<str:pkey>', views.SupprimerAgence, name="supprimer_agence"),

 
    #---------------CONTRIBUABLES-------------------#

    path('liste_contribuable/', views.ListeContribuable, name="liste_contribuable"),
    path('ajouter_contribuable/', views.AjouterContribuable, name="ajouter_contribuable"),
    path('ajouter_contribuable/<int:id>', views.AjouterContribuable, name="ajouter_contribuable"),
    path('modifier_contribuable/<str:pkey>', views.ModifierContribuable, name="modifier_contribuable"),
    path('supprimer_contribuable/<str:pkey>', views.SupprimerContribuable, name="supprimer_contribuable"),
    path('profil_contribuable/<str:pkey>', views.ProfilContribuable, name="profil_contribuable"),
    path('imprimer_contribuable/<int:pkey>', views.ImprimerContribuable, name="imprimer_contribuable"),


]

