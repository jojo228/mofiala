from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth.models import User

from . models import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, resolve_url

import random
from django.db.models import Q, F





def Accueil(request):

    return render(request, 'accueil.html', locals())



def Dashboard(request):

    if request.user.is_staff:

        agence = Agence.objects.filter(user__is_superuser = 0).all().count()
        contribuable =Contribuable.objects.all().count()
        
    

    else:

       contribuable =Contribuable.objects.filter(Q(agence=request.user.agence)).all().count()

    return render(request, 'dashboard/tableau.html', locals())



#--------------------------AGENCE----------------------------#

@login_required(login_url='connexion')
def AjouterAgence(request):
    #Invoquer les 2 formulaires, et les afficher comme un seul formulaire sur la page html
    form_user = FormeUser(data=request.POST)
    form_employe = AgenceForm(data=request.POST)
    if request.method == 'POST':
        #Verifier la concordance des deux mots de passe
        password1 = request.POST.get('password')
        password2 = request.POST.get('passwordCheck')
        
        contact = request.POST.get('contact')
        if password1 != password2:
            passwordDontMatch = True
            return render(request, 'default/ajouter_agence.html', 
            )

        #Verifier la validité des 2 formulaire
        if form_user.is_valid() and form_employe.is_valid():
            nom = form_employe.cleaned_data['nom_agence']
            #Verifier que le code est unique
            if Agence.objects.filter(contact=contact):
                ContactExist = True
                return render(request, 'default/ajouter_agence.html', 
            {'Le code existe':ContactExist})

            username = nom + str(random.randint(0,100))
            while User.objects.filter(username=username):
                username = nom + str(random.randint(0,100))
        
            #Ajouter une agence et enregistrer
            user = User.objects.create_user(username=username, password=password1)
            group = Group.objects.get(name='agence')
            user.groups.add(group)
            user.save()

            #Pour les informations supplémentaire
            employe = form_employe.save(commit=False)

            #Set One to One relationship between FormeUser and FormeEmploye
            employe.user = user

            #Maintenant enregistrons le model
            employe.save()

            #Ajout réussi
            return HttpResponseRedirect(reverse('liste_agence'))
    
    context = {'form':form_employe, 'form2':form_user}

    #Si ca n'a pas été un post Http, on va alors afficher une page blanche
    return render(request,'ajouter_agence.html', context)



@login_required(login_url='connexion')
def ModifierAgence(request, pkey):
   
    agence = get_object_or_404(Agence, id=pkey)
    if request.method == 'POST':
        user_form = FormeUser(request.POST, instance=agence.user)
        employe_form = AgenceForm(
            request.POST, instance=agence)
        if user_form.is_valid() and employe_form.is_valid():
            user = user_form.save()
            user.set_password(request.POST.get('password'))
            user.save()
            employe_form.save()
            #Rediriger vers la liste des employés
            return redirect('liste_agence')
    else:
        user_form = FormeUser(instance=request.user)
        employe_form = AgenceForm(instance=request.user.agence)

    context = {
        'user_form': user_form,
        'employe_form': employe_form,
    }
    return render(request, 'maj_agence.html', locals())        

@login_required(login_url='connexion')
def SupprimerAgence(request, pkey):

    structure = Agence.objects.get(id=pkey)
    if request.method == 'POST':
        structure.delete()
        return redirect('liste_agence')

    context = {'structure':structure}
    return render(request, 'supprimer_agence.html', context)


@login_required(login_url='connexion')
def ProfilAgence(request, pkey):
    
    profile = Agence.objects.get(id=pkey)
    
    

    nbr_Contribuable = profile.Contribuable_set.all().count()
    

    Contribuable = profile.Contribuable_set.all()
    sos = profile.soscredit_set.all()

    context = {'profil':profile,'Contribuable':Contribuable,'sos':sos,
            'nbr_Contribuable':nbr_Contribuable,}


    
    return render(request, 'profil_agence.html', context)


@login_required(login_url='connexion')
def ListeAgence(request):
    
    agence = Agence.objects.filter(Q(user__is_superuser = 0))

    myfilter = AgenceFilter(request.GET, queryset=agence)
    agence = myfilter.qs

    return render(request, 'liste_agence.html', {'agence':agence, 'myfilter':myfilter})




#--------------------------CONTRIBUABLE----------------------------#

def AjouterContribuable(request, id=None):

    if id != None:
        c  = Contribuable.objects.get(id=id)

    else:
        c = Contribuable.objects.create()
        c.save()
        return render(request, 'location_form.html', locals())


    if request.method == 'POST':

        contribuable  = Contribuable.objects.get(id=id)

        form = ContribuableForm(request.POST, request.FILES, instance=contribuable)
        
        """ first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        title = request.POST.get('identity')
        nif = request.POST.get('nif')
        denomination = request.POST.get('denomination')
        is_owner = request.POST.get('is_owner')
        quarter = request.POST.get('quarter')
        rue = request.POST.get('rue')
        door_number = request.POST.get('door_number')
        lot_number = request.POST.get('lot_number')
        parcel_number = request.POST.get('parcel_number')
        land_title_number = request.POST.get('land_title_number')
        tel = request.POST.get('tel')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        geo_situation = request.POST.get('geo_situation') """

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse(ImprimerContribuable, args=(id,)))

    context = {'form':form}

    return render(request, 'location_form.html', locals())


def ImprimerContribuable(request, pkey):
   
    contribuable  = Contribuable.objects.get(id=pkey)
    
    context = {'form':contribuable}
    return render(request, 'imprimer_contribuable.html', context)



def ModifierContribuable(request, pkey):
   
    contribuable  = Contribuable.objects.get(id=pkey)
    form = ContribuableForm(instance=contribuable)
    if request.method == 'POST':
        form = ContribuableForm(request.POST, instance=contribuable)
        if form.is_valid():
            form.save()
        return redirect('profil_contribuable', contribuable.id)
            
    context = {'form':form}
    return render(request, 'ajouter_contribuable.html', context)        


@login_required(login_url='connexion')
def SupprimerContribuable(request, pkey):

    contribuable = Contribuable.objects.get(id=pkey)
    if request.method == 'POST':
        contribuable.delete()
        return redirect('liste_contribuable')

    context = {'Contribuable':contribuable}
    return render(request, 'dashboard/supprimercontribuable.html', context) 


@login_required(login_url='connexion')
def ProfilContribuable(request, pkey):
    profile = Contribuable.objects.get(id=pkey)

    context = {'profil':profile,}

    return render(request, 'dashboard/profil_contribuable.html', context)



@login_required(login_url='connexion')
def ListeContribuable(request):
    

    if request.user.is_staff:
        contribuable = Contribuable.objects.all().order_by('-first_name')
        myfilter = ContribuableFilter(request.GET, queryset=contribuable)
        contribuable = myfilter.qs
    else:
        contribuable = Contribuable.objects.filter().order_by('-first_name')
        myfilter = ContribuableFilter(request.GET, queryset=contribuable)
        contribuable = myfilter.qs
    

    context =  {'contribuable':contribuable, 'myfilter':myfilter}
    return render(request, 'dashboard/liste_contribuable.html', context)




 


