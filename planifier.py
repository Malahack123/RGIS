import pandas as pd  #importation de la bibliothèque PANDAS pour traiter les fichiers excel 
import classes as cl #importation du fichier python qui contient les définitions des classes 
import functions

def planifier(perf_aud_col, perf_aud,planning_inv_col,planning_inv,dispo_aud_col,dispo_aud,vehicules,pc, carrefour_col, carrefour):
    print('Lancement du planifieur..')

    print('Lancement de la récupération des performances')
#Partie 1, on récupère les infos dans nos trois listes    
    magasins = [] #initialiser la liste des magasins
    auditeurs =[]  #initialiser la liste des auditeurs
    rel_aud_mag = []  #initialiser la liste des éléments de relation entre les magasins et les auditeurs
    rel_aud_ray = []
    n = len(carrefour)
    m = len(carrefour[0])
    #print(n, m)
    #print(carrefour_col)
    #functions.print_table(carrefour)
    for k in range(n):
        customer_name = carrefour[k][0]
        store_id = int(carrefour[k][1])
        lieu = carrefour[k][2]
        liste_articles = [int(carrefour[k][j+3])for j in range(15)]
        existence_mag = False
        for mag in magasins:
            if mag.store_number == store_id :
                existence_mag = True
                k_mag = magasins.index(mag)
                break
        if existence_mag:
            for j in range(len(magasins[k_mag].rayon)) :
                magasins[k_mag].rayon[j][1] = (magasins[k_mag].rayon[j][1]*magasins[k_mag].rayon[j][2] + liste_articles[j])/magasins[k_mag].rayon[j][2] + 1
                magasins[k_mag].rayon[j][2] += 1
        else :
            mag = cl.magasin( customer_name, -1, store_id)
            for j in range(len(mag.rayon)) :
                mag.rayon[j][0] = carrefour_col[j+3]
                mag.rayon[j][1] = liste_articles[j]
                mag.rayon[j][2] = 1
            magasins.append(mag)
    for mag in magasins :
        mag.calculate_ratio()
        #mag.print_mag()
    n = len(perf_aud)
    m = len(perf_aud[0])
    for k in range(n): #on parcourt notre dataframe qui contient l'ensemble des magasins
        for j in range(m): #on parcourt les colonnes de notre ligne
            if  perf_aud_col[j] == 'customer name':
                customer_name = str(perf_aud[k][j])
            elif  perf_aud_col[j] == 'auditor_name':
                auditor_name = str(perf_aud[k][j])
            elif  perf_aud_col[j] == 'group name': #pas besoin pour l'instant, voir pour carrefour
                group_name = perf_aud[k][j]
            elif  perf_aud_col[j] == 'score':
                score = float(perf_aud[k][j])
            elif  perf_aud_col[j] == 'customer code':
                customer_code = int(perf_aud[k][j])
            elif  perf_aud_col[j] == 'badge_id':
                badge_id = int(perf_aud[k][j])
        car = False
        if customer_name.lower().find('carrefour') != -1 :#si la ligne de perf concerne un carrefour
            #print('Ping carrefour perfs')
            car = True
            existence_rel_ray = False
            for item in rel_aud_ray:
                if item.rayon == group_name and item.badge_id == badge_id :
                    existence_rel_ray = True
                    k_rel_ray = rel_aud_ray.index(item)
                    break
            existence_mag = True #booléen vrai si le magasin est prsent dans la liste des magasins, faux sinon 
              
        else : 
            existence_mag = False #booléen vrai si le magasin est prsent dans la liste des magasins, faux sinon 
            for mag in magasins:
                if mag.customer_code == customer_code : # le magasin courant a été trouvé dans notre liste de magasins
                    existence_mag = True 
                    k_mag = magasins.index(mag)
                    break
        existence_aud = False #booléen vrai si l'auditeur est prsent dans la liste des auditeurs, faux sinon 
        for aud in auditeurs:
            if aud.badge_id == badge_id: # l'auditeur courant a été trouvé dans la liste des auditeurs
                existence_aud = True
                k_aud = auditeurs.index(aud)
                break
        existence_rel = False #booléen vrai si le triplet de relation aud/mag est prsent dans la liste rel_aud_mag, faux sinon 
        for item in rel_aud_mag:
            if item.badge_id == badge_id and item.customer_code == customer_code: 
                existence_rel = True
                k_rel = rel_aud_mag.index(item)
                break
        if not existence_mag : #si le magasin n'est pas dans notre liste
            magasins.append(cl.magasin(customer_name,customer_code)) #on crée notre magasin
        elif existence_aud : #si l'auditeur est présent dans notre liste
            auditeurs[k_aud].avg_score = (auditeurs[k_aud].avg_score*auditeurs[k_aud].nb_score + score)/auditeurs[k_aud].nb_score+1
            auditeurs[k_aud].nb_score += 1
        elif not existence_aud : #si l'auditeur n'est pas présent
            splitted_name = auditor_name.split(' ')# liste contenant les noms et prénom de l'auditeur
            nom = splitted_name[-1]
            prenom = ' '.join(splitted_name[:-1])
            auditeurs.append(cl.auditeur(nom, prenom, auditor_name, badge_id, conducteur = False, total_score = score, nb_score = 1))
        elif existence_rel : #le triple de relation existe pouyr l'aud et le mag courant
            rel_aud_mag[k_aud].score = (rel_aud_mag[k_aud].score*rel_aud_mag[k_rel].nb_score + score)/rel_aud_mag[k_rel].nb_score+1
            rel_aud_mag[k_rel].nb_score += 1

        elif not existence_rel : #si le triple de relation n'existe pas
            rel_aud_mag.append(cl.audXmag(customer_code, badge_id, nb_score = 1, total_score = score)) #on le rajoute
        elif car and existence_rel_ray :
            rel_aud_ray[k_rel_ray].score = (rel_aud_ray[k_rel_ray].score*rel_aud_ray[k_rel_ray].nb_score +  score)/rel_aud_ray[k_rel_ray].nb_score+1
            rel_aud_ray[k_rel_ray].nb_score += 1

        elif car and not existence_rel_ray :
            rel_aud_ray.append(cl.audXrayon(group_name,badge_id,nb_score = 1, total_score = score))
    print('Récupération des performances terminée. Calcul des scores')
#Partie 2 on calcule les scores moyens 

    print('Récupération des disponibilités')
#Partie 3: on récupère les disponibilités auditeurs
    n = len(dispo_aud)
    m = len(dispo_aud[0])
    for k in range(n): #on parcourt le tableau une ligne à la fois
        badge_id = int(dispo_aud[k][0])
        auditor_name = str(dispo_aud[k][1])
        infos = str(dispo_aud[k][2])

        dispos = dispo_aud[k][3:]
        #samedi = dispo_aud[k][3]
        #lundi = dispo_aud[k][4]
        #mardi = dispo_aud[k][5]
        #mercredi = dispo_aud[k][6]
        #jeudi = dispo_aud[k][7]
        #vendredi = dispo_aud[k][8]*
        conducteur = False
        if infos.lower().find('conducteur') != -1 :
            #print('Ping conducteur')
            conducteur = True
        existence_aud = False
        for aud in auditeurs : #on parcourt notre liste d'auditeurs
            if aud.badge_id == badge_id: #si l'auditeur courant est présent
                #print('Ping auditeur trouvé')
                aud.remplir_planning(dispos) #on remplit son planning à partir des dispos WARNING !!
                existence_aud = True
                aud.conducteur = conducteur #on définit le booléen conducteur
                break
        if not existence_aud: #si l'auditeur n'existe pas
            splitted_name = auditor_name.split(' ')
            nom = splitted_name[-1]
            prenom = ' '.join(splitted_name[:-1])
            aud = cl.auditeur(nom, prenom, auditor_name, badge_id, conducteur)
            aud.remplir_planning(dispos)
            auditeurs.append(aud) #.. on le rajoute
              
    parc_auto = []
    n = len(vehicules)
    for  k in range(n):
        voiture = vehicules[k].split(' ')
        immat = voiture[0]
        modele = voiture[1]
        nb_places = int(voiture[2][:-2])
        parc_auto.append(cl.vehicule(immat, nb_places, modele))
    parc_auto = sorted(parc_auto, key=lambda vehicule: vehicule.nb_places, reverse = False)
    parc_sac_PC = []
    n = len(pc)
    for k in range(n):
        numero = int(pc[k][0])
        nb_PCs = int(pc[k][1])
        parc_sac_PC.append(cl.sac_PC(numero, nb_PCs))

    parc_sac_PC = sorted(parc_sac_PC, key=lambda sac_PC: sac_PC.nb_pc, reverse = False)
    print('La partie récupération de données est effectuée.')
#2eme partie du parser, qui s'occupe de créer les inventaireset de les remplir d'auditeurs
    print('lancement de la planification')
    print('Création des inventaires')
#Partie 1 : on crée les inventaires 
    inventaires = []
    semaine = dispo_aud_col[3:]
    jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']

    n = len(planning_inv)
    m = len(planning_inv) #a retirer ??
    
    for k in range(n): #on itère sur tous les inventaires
        date = str(planning_inv[k][0])
        cust_id = int(planning_inv[k][1])
        client = str(planning_inv[k][2])
        store_number = int(planning_inv[k][3])
        heure =  str(planning_inv[k][4])
        people = int(planning_inv[k][5])
        lieu = str(planning_inv[k][6])
        
        for j in range(len(semaine)):
            if date == str(semaine[j]) : #on fait un matching entre la date de l'inventaire courant et l'un des jours de notre semaine à planifier
                if client.lower().find('carrefour') != -1 :
                    #print('Ping carrefour inventaires')
                    existence_mag = False
                    for mag in magasins: #on itère sur nos magasins
                        if mag.store_number == store_number: #si le magasin de l'inventaire courant est déja dans la liste :
                            k_mag = magasins.index(mag)
                            existence_mag = True
                            break
                else :                                 
                    existence_mag = False
                    for mag in magasins: #on itère sur nos magasins
                        if mag.customer_code == cust_id: #si le magasin de l'inventaire courant est déja dans la liste :
                            k_mag = magasins.index(mag)
                            existence_mag = True
                            break
                
                if existence_mag:
                    inventaires.append(cl.inventaire(date = date, heure =heure, customer = magasins[k_mag], place =lieu , people = people, jour = jours[j]))
                else :
                    mag = cl.magasin(nom = client, customer_code = cust_id) #WARNING ! vérif str ? si un nouveau carrefour arrive ca marche pas
                    magasins.append(mag)
                    inventaires.append(cl.inventaire(date = date, heure = heure, customer = mag, place = lieu, people = people, jour = jours[j]))
    print('Inventaires crées')

#Partie 2 : on ajoute les véhicules, les auditeurs conducteurs, et les auditeurs normaux, les pc
#on attribue les véhicules et les auditeurs conducteurs 
    for k in range(len(inventaires)) : # on parcourt nos inventaires crées
        places = 0 # variable place, qui va nous indiquer combien de places on a affecté à l'inventaire (en terme de voitures)
        while places < int(inventaires[k].people) : # tant qu'il n'y a pas assez de place
            # on va choisir une voiture parmi le parc
            n = len(parc_auto)
            capa = 0
            j =0
            voiture_choisie = -1 #on initalise à -1 dans le cas ou on ne trouve pas de voiture
            while capa < int(inventaires[k].people)-places and   j < n: #tant que le véhicule choisi a une capacité inférieur au nombre de places à ajouter, ou que l'on arrive à la fin de nos véhicules
                voiture = parc_auto[j] #on récupère la voiture courante
                if voiture.est_dispo(inventaires[k]) and voiture.nb_places > capa: #si elle est dispo et son nb de place est le plus grand de tous les véhicules 
                    capa = voiture.nb_places #elle devient notre choix
                    voiture_choisie = voiture
                j += 1
            if voiture_choisie == -1:#pas de voiture == PROBLEME
                print("je n'ai pas trouvé de voiture")
                break
            
            parc_auto[parc_auto.index(voiture_choisie)].remplir_planning(inventaires[k])#on remplit le planning de la voiture
            inventaires[k].vehicules.append(voiture_choisie) # on ajoute la voiture 
            places += int(voiture_choisie.nb_places) # on augment le nombre de places dispo 
            
    
        j = 0
        while j < len(auditeurs) and len(inventaires[k].auditeurs)<len(inventaires[k].vehicules):#tant que on a encore des auditeurs, et qu'on a rajouté moins d'auditeurs que de voiturzes 
            if auditeurs[j].conducteur and auditeurs[j].est_dispo(inventaires[k]) : # si l'auditeur courant a le permis et est dispo 
                auditeurs[j].remplir_planning_inventaire(inventaires[k]) # on remplit son planning 
                inventaires[k].auditeurs.append(auditeurs[j]) # on le rajoute à l'inventaire
            j += 1

#on attribue les autres auditeurs 
    for k in range(len(inventaires)) : # on parcourt nos inventaires crées
        if inventaires[k].customer.nom.lower().find('carrefour') != -1:
            inventaires[k].customer.print_mag()
            for j in range(len(inventaires[k].auditeurs_rayon)):
                inventaires[k].auditeurs_rayon[j][0] =  inventaires[k].customer.rayon[j][0]
                temp = inventaires[k].customer.rayon[j][3]*inventaires[k].people
                if temp - round(temp) > 0:
                    inventaires[k].auditeurs_rayon[j][1] = round(temp) + 1
                else :
                    inventaires[k].auditeurs_rayon[j][1] = round(temp)
            somme = 0
            for j in range(len(inventaires[k].auditeurs_rayon)):
                 somme += inventaires[k].auditeurs_rayon[j][1]
            print('people : '+str(inventaires[k].people)+', somme : ' + str(somme))
            #print(inventaires[k].auditeurs_rayon)
            continue
        
        score_mag = [elem for elem in rel_aud_mag if elem.customer_code == inventaires[k].customer.customer_code]#liste des scores par auditeurs sur le magasin de l'inventaire courant
        sorted_scores = sorted(score_mag, key=lambda audXmag: audXmag.score, reverse = True) #meme liste, triée par score
        m = 0
        n = len(auditeurs)
        while len(inventaires[k].auditeurs) < inventaires[k].people and m < len(sorted_scores): #par magasin 
            for i in range (n):
                if sorted_scores[m].badge_id == auditeurs[i].badge_id and auditeurs[i].est_dispo(inventaires[k]):
                    auditeurs[i].remplir_planning_inventaire(inventaires[k])
                    inventaires[k].auditeurs.append(auditeurs[i])
                    break
            m += 1
        sorted_auditeurs = sorted(auditeurs, key=lambda auditeur: auditeur.avg_score, reverse = True)
        m = 0
        while len(inventaires[k].auditeurs) < inventaires[k].people and m < len(sorted_auditeurs): # par avg_score
            for i in range(n):
                if sorted_auditeurs[m].badge_id == auditeurs[i].badge_id and auditeurs[i].est_dispo(inventaires[k]):
                    auditeurs[i].remplir_planning_inventaire(inventaires[k])
                    inventaires[k].auditeurs.append(auditeurs[i])
                    break
            m += 1
            
# on attribue les sacs de PC
    for k in range(len(inventaires)) : # on parcourt nos inventaires crées
        pc = 0 # variable place, qui va nous indiquer combien de pc on a affecté à l'inventaire
        ppl = inventaires[k].people
        while pc < ppl : # tant qu'il n'y a pas assez de place
            # on va choisir un sac
            n = len(parc_sac_PC)
            capa = 0
            j =0
            sac_choisi = -1 #on initalise à -1 dans le cas ou on ne trouve pas de sac
            while capa < ppl-pc and   j < n: #tant que le sac choisi a une capacité inférieur au nombre de places à ajouter, ou que l'on arrive à la fin de nos sacs
                sac = parc_sac_PC[j] #on récupère le sac courant
                if sac.est_dispo(inventaires[k]) and sac.nb_pc > capa: #si il est dispo et son nb de place est le plus grand de tous les véhicules 
                    capa = sac.nb_pc #il devient notre choix
                    sac_choisi = sac
                j += 1
            if sac_choisi == -1:#pas de sac == PROBLEME
                print("je n'ai pas trouvé de sac")
                break
            
            parc_sac_PC[parc_sac_PC.index(sac_choisi)].remplir_planning(inventaires[k])#on remplit le planning de la voiture
            inventaires[k].sacs_PC.append(sac_choisi) # on ajoute le sac 
            pc += int(sac_choisi.nb_pc) # on augment le nombre de places dispo 
            
    '''
    for aud in auditeurs:
        if aud.conducteur:
            aud.print_auditeur()
  '''
    print("le planifieur s'est correctement exécuté.")
    return inventaires, auditeurs, magasins, parc_auto, parc_sac_PC


 
        
