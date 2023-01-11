import pandas as pd
import glob as gb
import os
import datetime

#PRE_PLANIFIER
#Ce programme récupère les fichiers et les transforme en base de données Pandas.
#IL est configuré pour la robustesse 
def pre_planifier(jour, mois, annee):

    print('Lancement du préplanifieur')
    #on récupère la liste des fichiers dans chaque sous dossier de nos inputs
    perf_aud = gb.glob('./input/performances auditeurs/**') # fichier de performances auditeurs
    planning_inv = gb.glob('./input/planning inventaires/**') # le planning des inventaires
    dispo_aud = gb.glob('./input/disponibilités auditeurs/**') # le tableau des disponibilités auditeurs
    infos_vehicules = gb.glob('./input/véhicules/**') # la liste des véhicules du parc 
    infos_pc = gb.glob('./input/PC/**') # la liste des sacs avec leur nombre de PC
    carrefour = gb.glob('./input/carrefour/**') # le fichier contenant les infos carrefour 
    #vérifier la taille des listes /==0, >1 et retourner des messages d'erreurs
    if len(perf_aud) == 0 :
        raise Exception('le dossier PERFORMANCES AUDITEURS est vide.')
    elif len(planning_inv) == 0 :
        raise Exception('le dossier PLANNING INVENTAIRES est vide.')
    elif len(dispo_aud) == 0 :
        raise Exception('le dossier DISPONIBILITES AUDITEURS est vide.')
    elif len(infos_vehicules) == 0 :
        raise Exception('le dossier VEHICULES est vide.')
    elif len(infos_pc) == 0 :
        raise Exception('le dossier PC est vide.')
    elif len(carrefour) == 0 :
        raise Exception('le dossier carrefour est vide.')
   

    if len(perf_aud) > 1 :
        raise Warning('le dossier PERFORMANCES AUDITEURS contient plus dun élément.(ou vous avez un fichier douvert)')
    elif len(planning_inv) > 1:
        raise Warning('le dossier PLANNING INVENTAIRES contient plus dun élément.(ou vous avez un fichier douvert)')
    elif len(dispo_aud) > 1 :
        raise Warning('le dossier DISPONIBILITES AUDITEURS contient plus dun élément.(ou vous avez un fichier douvert)')
    elif len(infos_vehicules) > 1 :
        raise Warning('le dossier VEHICULES contient plus dun élément.(ou vous avez un fichier douvert)')
    elif len(infos_pc) > 1 :
        raise Warning('le dossier PC contient plus dun élément.(ou vous avez un fichier douvert)')
    elif len(carrefour) > 1 :
        raise Warning('le dossier carrefour contient plus dun élément.(ou vous avez un fichier douvert)')
    #TODO else format inconnu
                        

    #on vérifie le format des fichiers et on transfère les données dans une BDD

    #pour les performances auditeurs..
    if perf_aud[0][-3:]=='xls':
        db_perf_aud = pd.ExcelFile(perf_aud[0]) # lire le contenu du fichier DATAS_PERFORMANCE
    elif perf_aud[0][-4:]=='xlsx':
        db_perf_aud = pd.read_excel(perf_aud[0]) # lire le contenu du fichier DATAS_PERFORMANCE
    elif perf_aud[0][-3:]=='txt' :
        db_perf_aud = open(perf_aud[0]) # lire le contenu du fichier DATAS_PERFORMANCE
    #pour le planning inventaire..
    if planning_inv[0][-3:]=='xls':
        db_planning_inv = pd.read_excel(planning_inv[0], header=None, engine = 'xlrd')
        db_planning_inv.to_excel(planning_inv[0]+'x', index=False, header=False)
        if os.path.exists(planning_inv[0]):
            os.remove(planning_inv[0])
    elif planning_inv[0][-4:]=='xlsx' or planning_inv[0][-4:]=='xlsb':
        db_planning_inv = pd.read_excel(planning_inv[0]) # lire le contenu du fichier inventaires à categoriser.xlsx
    elif planning_inv[0][-3:]=='txt':
        db_planning_inv = open(planning_inv[0]) # lire le contenu du fichier inventaires à categoriser.xlsx
    #pour les disponibilités auditeurs..
    if dispo_aud[0][-3:]=='xls':
        db_dispo_aud = pd.ExcelFile(dispo_aud[0]) # lire le contenu du fichier tableau disponibilites.xls
    elif dispo_aud[0][-4:]=='xlsx':
        db_dispo_aud = pd.read_excel(dispo_aud[0]) # lire le contenu du fichier tableau disponibilites.xlsx
    elif dispo_aud[0][-3:]=='txt' :
        db_dispo_aud = open(dispo_aud[0]) # lire le contenu du fichier tableau disponibilites.txt
    #pour les véhicules..
    if infos_vehicules[0][-3:]=='xls':
        db_vehicules = pd.ExcelFile(infos_vehicules[0]) # lire le contenu du fichier vehicules.xls
    elif infos_vehicules[0][-4:]=='xlsx':
        db_vehicules = pd.read_excel(infos_vehicules[0]) # lire le contenu du fichier vehicules.xlsx
    elif infos_vehicules[0][-3:]=='txt':
         db_vehicules = open(infos_vehicules[0]) # lire le contenu du fichier vehicules.txt
    #et pour les PCs
    if infos_pc[0][-3:]=='xls':
        db_pc = pd.ExcelFile(infos_pc[0]) # lire le contenu du fichier PC.xlsx
    elif infos_pc[0][-4:]=='xlsx':
        db_pc = pd.read_excel(infos_pc[0]) # lire le contenu du fichier PC.xlsx
    elif infos_pc[0][-3:]=='txt':
        db_pc = open(infos_pc[0]) # lire le contenu du fichier PC.txt

    if carrefour[0][-3:]=='xls':
        db_carrefour = pd.ExcelFile(carrefour[0]) # lire le contenu du fichier carrefour
    elif carrefour[0][-4:]=='xlsx' or carrefour[0][-4:]=='xlsm':
        db_carrefour = pd.read_excel(carrefour[0], sheet_name= 'Détail 2016 à 2020') # lire le contenu du fichier carrefour
    elif carrefour[0][-3:]=='txt':
        db_carrefour = open(carrefour[0]) # lire le contenu du fichier carrefour



    #Traitement de la BDD
    #idée long terme : faire une recherche par mot clé dans la BDD pour être plus robuste 

    #des perfs auditeurs..
    #on retire les scores enregistrés (une ligne) qui on un total rm time inférieur à 10 minutes
    db_perf_aud = db_perf_aud.loc[(db_perf_aud["total rm time"]>=1/6), ['customer name','name auditor','group name','score', 'customer code','badge id']]

    #on renomme des colonnes
    db_perf_aud = db_perf_aud.rename(columns={"name auditor": "auditor_name"}) #renommer la colonne
    db_perf_aud = db_perf_aud.rename(columns={"badge id": "badge_id"}) #renommer la colonne

    #retirer les scores supérieurs à 500%
    db_perf_aud = db_perf_aud.loc[(db_perf_aud["score"]<=500), ['customer name','auditor_name','group name','score','customer code','badge_id']]

    #on enlève les performances sur les comptes invités
    badge_id = db_perf_aud["badge_id"]
    badge_id_list = badge_id.tolist()
    added_col = pd.Series([str(badge_id_list[k])[0:2] != '99' for k in range(len(badge_id_list))])
    db_perf_aud = db_perf_aud.assign(added_col = added_col .values)
    db_perf_aud = db_perf_aud[db_perf_aud.added_col]
    db_perf_aud = db_perf_aud.drop(columns=['added_col'])

    #db_perf_aud = db_perf_aud[pd.Series([str(badge_id_list[k])[0:2] != '99' for k in range(len(badge_id_list))])]
    #le planning inventaire..
    #on retire les colones inutiles
    db_planning_inv = db_planning_inv.drop(columns=["Auth#'s", 'Est Length', 'Split', 'Estimated Inventory','Act Split','Req Split','Dist # of People','RGIS Manager','Event Desc.','Cycle Name','Phone Number','Support Dists'])
    db_planning_inv = db_planning_inv.drop(columns=['B/R  Time','Tot Sched'])
    #print(db_planning_inv.head(10).to_string())

    #les disponibiltés auditeurs, on retire les colonnes qui ne servent pas
    dispo_aud_col = db_dispo_aud.columns.to_list()
    index = -1
    #print(db_dispo_aud_col)

    for elem in dispo_aud_col:
        if elem ==  datetime.datetime(annee, mois, jour, 0, 0):
            index = dispo_aud_col.index(elem)
    if index == -1:
        raise Exception('désolé, je nai pas réussi à trouver la date dans le tableau des disponibilités')
  
    #print(index)
    db_dispo_aud = db_dispo_aud.iloc[1:,[1,2,8,index, index+1, index +2, index +3, index +4, index +5]] #voici la sélection qui nous intéresse...
    #db_dispo_aud = db_dispo_aud.iloc[1:,[1,2,8,28,29,30,31,32,33]] #mais pour mes tests de dois aller cherche plus loin dans le tableau
    #db_dispo_aud = db_dispo_aud.iloc[1:,[1,2,8,16,17,18,19,20,21]] #voici la sélection qui nous intéresse...
    db_dispo_aud = db_dispo_aud.rename(columns={'Unnamed: 1': "badge_id"})
    db_dispo_aud = db_dispo_aud.rename(columns={'Unnamed: 2': "auditor_name"})
    db_dispo_aud = db_dispo_aud.rename(columns={'Unnamed: 8': "infos"})
    dispo_col = db_dispo_aud.columns[3:]
    print(dispo_col)

    #processing tableau disponibilités

    
    for ind in db_dispo_aud.index: #on itère sur la bdd des dispos et on capte les infos pour les transmettre sur une seul case du tableau 
        
        if type(db_dispo_aud['infos'][ind])==type('a'):
    
            if (ind-1)%4==1:
                db_dispo_aud['infos'][ind-1] = str(db_dispo_aud['infos'][ind-1])+ ' - '+ db_dispo_aud['infos'][ind] 
            elif (ind-1)%4==2:
                db_dispo_aud['infos'][ind-2] = str(db_dispo_aud['infos'][ind-2])+ ' - '+ db_dispo_aud['infos'][ind]
            elif (ind-1)%4==3:
                db_dispo_aud['infos'][ind-3] = str(db_dispo_aud['infos'][ind-3])+ ' - '+ db_dispo_aud['infos'][ind]

     
    db_dispo_aud = db_dispo_aud.dropna(how = 'all', subset=['badge_id']) #on supprime 3 lignes sr 4, car on en n'a plus besoin 

    #processing tableau PC :
    db_pc = db_pc.dropna() # on enlève la colonne NaN du tableur

    db_carrefour = db_carrefour.iloc[:,[0,2,3,5,6,7,8,9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]
    
    perf_aud_col = db_perf_aud.columns.tolist()
    perf_aud = db_perf_aud.to_numpy()

    planning_inv_col = db_planning_inv.columns.tolist()
    planning_inv = db_planning_inv.to_numpy()

    dispo_aud_col = db_dispo_aud.columns.tolist()
    dispo_aud = db_dispo_aud.to_numpy()

    vehicules = db_vehicules.to_numpy().flatten()
    pc = db_pc.to_numpy()

    carrefour = db_carrefour.to_numpy()
    carrefour_col = carrefour[0]
    carrefour = carrefour[1:]
    print("Le préplanifieur s'est correctement déroulé")
    #print(carrefour_col)
    #print(carrefour[0])
    #print(len(db_carrefour.columns))
    return perf_aud_col, perf_aud,planning_inv_col,planning_inv,dispo_aud_col,dispo_aud,vehicules,pc, carrefour_col, carrefour # on retourne les 8 bases de données 


