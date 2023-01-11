#FICHIER MAIN
#S'Occupe de l'administration des autres fichiers
from pre_planifier import pre_planifier
from planifier import planifier
from post_planifier import post_planifier
import classes as cl
from functions import print_table
print('Lancement de PLANR')
'''
flag = True
while True :
    try:
        print('Veuillez entrer la date du premier jour de la semaine à organiser : (un Samedi, au format jj/mm/aaaa)')
        date = input('Date départ planification (samedi): ')
        date = date.split('/')
        annee = date[2]
        mois = date[1]
        jour = date[0]
        a, m, j = len(annee), len(mois),len(jour)
        flag = a != 4 or m != 2 or j != 2
        annee = int(annee)
        mois = int(mois)
        jour = int(jour)
        #print(a, m, j)
        #print(date)
    except:
        print('Exception')
        continue
    if flag :
        print('Flag : ', flag)
        continue
    else:
        print('Ok')
        break
'''    
jour, mois, annee = 12, 3, 2022

perf_aud_col, perf_aud,planning_inv_col,planning_inv,dispo_aud_col,dispo_aud,vehicules,pc, carrefour_col, carrefour =  pre_planifier(jour, mois, annee)


#print(db_dispo_aud.head(10).to_string())
#print('dispoi_aud_col:')
#print(dispo_aud_col)

#print(db_pc.head(10).to_string())
#print(dispo_aud_col)
#print_table(planning_inv)
#print(planning_inv_col)
#print(pc)
inventaires, auditeurs, magasins, parc_auto, parc_sac_pc = planifier(perf_aud_col, perf_aud,planning_inv_col,planning_inv,dispo_aud_col,dispo_aud,vehicules,pc, carrefour_col, carrefour)

def print_infos(inventaires, auditeurs, magasins, parc_auto, parc_sac_pc):
    for inv in inventaires:
        inv.customer.print_mag()
        print('date:'+inv.date+', heure: '+ inv.heure) 
        print(len(inv.auditeurs), inv.people)
        places = 0
        for voiture in inv.vehicules:
            places += voiture.nb_places
        print('places dispos: '+str(places))
        cond = 0
        nb_pcs = 0
        for sac in inv.sacs_PC:
            nb_pcs += sac.nb_pc
        print('pc dispos: '+str(nb_pcs))   
        for aud in inv.auditeurs:
            if aud.conducteur:
                cond += 1
        print('conducteurs dispos:' + str(cond)+', nombre de voitures: '+ str(len(inv.vehicules)))
        print('date:'+inv.date+', heure: '+ inv.heure)
        print('')
        #.print_inventaire()
        
print_infos(inventaires, auditeurs, magasins, parc_auto, parc_sac_pc)
post_planifier(inventaires, auditeurs, magasins, parc_auto, parc_sac_pc)


