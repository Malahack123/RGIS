class audXrayon: # création de classe intermédiaire pour les scores des auditeurs par rayon


    def __init__(self, rayon, badge_id, nb_score = 0, total_score = 0): #fonction prédéfini pour construire les objets magasin et auditeur
        self.nb_score = nb_score #nombre de scores réalisés sur ce magasin 
        self.total_score = total_score #total des scores réalisés par auditeur par magasin
        self.score = 0 #score moyen des auditeurs (total_score/nb_score)
        self.rayon = rayon #code unique par magasin
        self.badge_id = badge_id #code unique par auditeur

    #def print_score(self): #fonction qui permet l'affichage du score des auditeurs par magasin en pourcentage
     #   print('magasin n°: ' + self.customer_code+ ', auditeur: '+ self.auditeur_prenom +' '+ self.auditeur_nom+', score '+ str(self.score*100)+ '%'+ '\n')

    def calculate_score(self): #fonction qui permet de calculer le score moyen des auditeurs
        if self.nb_score ==0:
            return
        self.score = self.total_score/self.nb_score

class audXmag: # création de classe intermédiaire pour les scores des auditeurs par magasin


    def __init__(self, customer_code, badge_id, nb_score = 0, total_score = 0): #fonction prédéfini pour construire les objets magasin et auditeur
        self.nb_score = nb_score #nombre de scores réalisés sur ce magasin 
        self.total_score = total_score #total des scores réalisés par auditeur par magasin
        self.score = 0 #score moyen des auditeurs (total_score/nb_score)
        self.customer_code = customer_code #code unique par magasin
        self.badge_id = badge_id #code unique par auditeur

    #def print_score(self): #fonction qui permet l'affichage du score des auditeurs par magasin en pourcentage
     #   print('magasin n°: ' + self.customer_code+ ', auditeur: '+ self.auditeur_prenom +' '+ self.auditeur_nom+', score '+ str(self.score*100)+ '%'+ '\n')

    def calculate_score(self): #fonction qui permet de calculer le score moyen des auditeurs
        if self.nb_score ==0:
            return
        self.score = self.total_score/self.nb_score

class magasin: #classe créée pour récupérer les magasins listés dans le fichier Excel à l'aide d'une fonction dataparser
    def __init__(self, nom, customer_code, store_number=0):
        self.nom = nom
        self.customer_code = customer_code
        self.store_number = store_number
        self.rayon = [['',0,0,0] for k in range(15)] # TODO remplacer ca par des classes
    def print_mag(self): #fonction pour l'affichage des magasins
        print('magasin '+ self.nom + ' cust_id : '+str(self.customer_code)  +', store_id : '+str(self.store_number) +'\n')

    def calculate_ratio(self):
        somme = 0

        for elem in self.rayon :
            somme += elem[1]
        if somme == 0 :
            return
        for elem in self.rayon :
            elem[3] = elem[1]/somme

class auditeur: #classe créée pour récupérer les auditeurs listés dans le fichier Excel avec leurs scores à l'aide de dataparser

    def __init__(self, nom, prenom, nom_complet, badge_id, conducteur=False, total_score = 0, nb_score = 0):  #fonction prédéfini pour construire l'objet auditeur
        self.total_score = total_score
        self.nb_score = nb_score
        self.avg_score = 0
        self.planning = [[False for i in range(6)] for k in range(24)]
        self.possible = [True for k in range (6)]
        self.nom = nom
        self.prenom = prenom
        self.nom_complet = nom_complet
        self.badge_id = badge_id
        self.conducteur = conducteur 

    def calculate_avg_score(self): #fonction qui permet de calculer le score moyen
        if self.nb_score == 0:
            return 
        self.avg_score = self.total_score/self.nb_score
        
    def print_auditeur(self):  #fonction qui permet l'affichage des auditeurs avec leurs scores
        #print(type(self.prenom), type(self.nom), type(self.nom_complet))
        print('auditeur '+ self.prenom +' '+ self.nom+', nom complet : '+self.nom_complet+', badge_id: '+str(self.badge_id)+', score '+ str(self.avg_score*100)+ '%'+ '\n')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in self.planning]))
        

    def remplir_planning(self, dispos):#fonction qui remplit l'attribut planning d'un auditeur à partir d'une slice du tableau des disponibilites
        n = len(dispos)
        if n != 6 :
            print('Erreur ! le tableau des dispos ne contient pas exactement 6 éléments')
            return
        #print(self.planning[0])
        m = len(self.planning)
        #print(m)
        for k in range(n): #on itère sur tous les jours de la semaine 
            if len(str(dispos[k])) == 8:#si on a une heure, on va remplir le tableau à partir de cette heure
                #print('Ping heure')
                
                
                index = int(str(dispos[k])[:2])
                for j in range(m):
                    self.planning[j][k] =  j >= index
            elif dispos[k] == 'D': #si l'auditeur est dispo, on met True partout
                #print('Ping dispo')
                for j in range(m):
                    self.planning[j][k] = True

            else : # sinon on met false partout 
                for j in range(m):
                    self.planning[j][k] = False
    def est_dispo(self, inv):
        jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        h = int(inv.heure[:2])
        j = -1
        for jour in jours:
            if jour == inv.jour:
                j = jours.index(jour)
                break
        if j == -1 :
            print("erreur est-dispo : pas trouvé le jour..")
            return
        else :
            if j == 5 :
                if h <= 18:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[h+5][j]
                elif h == 19:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] 
                elif h ==20:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] 
                elif h == 21:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] 
                elif h == 22:
                    return self.planning[h][j] and  self.planning[h+1][j] 
                elif h == 23:
                    return self.planning[h][j] 
            else :
                if h <= 18:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[h+5][j]
                elif h == 19:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[0][j+1]
                elif h ==20:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[0][j+1] and  self.planning[1][j+1]
                elif h == 21:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1]
                elif h == 22:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1] and  self.planning[3][j+1]
                elif h == 23:
                    return self.planning[h][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1] and  self.planning[3][j+1] and  self.planning[4][j+1]
               
    def remplir_planning_inventaire(self, inv):
        jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        h = int(inv.heure[:2])
        j = -1
        for jour in jours:
            if jour == inv.jour:
                j = jours.index(jour)
                break
        if j == -1 :
            return
        else :
            if j == 5:
                if h <= 18:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[h+5][j] = [False for k in range(6)]
                elif h == 19:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j] = [False for k in range(5)]
                elif h ==20:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j] = [False for k in range(4)]
                elif h == 21:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j]= [False for k in range(3)]
                elif h == 22:
                    self.planning[h][j], self.planning[h+1][j]= [False for k in range(2)]
                elif h == 23:
                    self.planning[h][j] = [False for k in range(1)] 
            else:
                if h <= 18:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[h+5][j] = [False for k in range(6)]
                elif h == 19:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[0][j+1] = [False for k in range(6)]
                elif h ==20:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[0][j+1],  self.planning[1][j+1] = [False for k in range(6)]
                elif h == 21:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[0][j+1], self.planning[1][j+1],  self.planning[2][j+1] = [False for k in range(6)]
                elif h == 22:
                    self.planning[h][j], self.planning[h+1][j], self.planning[0][j+1], self.planning[1][j+1], self.planning[2][j+1],  self.planning[3][j+1] = [False for k in range(6)]
                elif h == 23:
                    self.planning[h][j], self.planning[0][j+1], self.planning[1][j+1], self.planning[2][j+1], self.planning[3][j+1],  self.planning[4][j+1] = [False for k in range(6)]

    """
def remplir_planning(self, inventaire): #doit remplir le planning de notre auditeur car il participe à l'inventaire
        jour = inventaire.jour
        periode = inventaire.periode
        if jour == 'Lundi':
            if periode == 'AM':
                self.planning[0][0] = True
            else :
                self.planning[0][1] = True
                
        elif jour == 'Mardi':
            if periode == 'AM':
                self.planning[1][0] = True
            else :
                self.planning[1][1] = True
        elif jour == 'Mercredi':
            if periode == 'AM':
                self.planning[2][0] = True
            else :
                self.planning[2][1] = True
        elif jour == 'Jeudi':
            if periode == 'AM':
                self.planning[3][0] = True
            else :
                self.planning[3][1] = True
        else :
            if periode == 'AM':
                self.planning[4][0] = True
            else :
                self.planning[4][1] = True

    """          
    """
    def est_indispo(self, inventaire):
        jour = inventaire.jour
        periode = inventaire.periode
        if jour == 'Lundi':
            if periode == 'AM':
                return self.planning[0][0] 
            else :
                return self.planning[0][1]
                
        elif jour == 'Mardi':
            if periode == 'AM' :
                return self.planning[1][0]
            else :
                return self.planning[1][1]
        elif jour == 'Mercredi':
            if periode == 'AM' :
                return self.planning[2][0]
            else :
                return self.planning[2][1]
        elif jour == 'Jeudi':
            if periode == 'AM' :
                return self.planning[3][0]
            else :
                return self.planning[3][1]
        elif jour == 'Vendredi':
            if periode == 'AM' :
                return self.planning[4][0]
            else:
                return self.planning[4][1]
     """       

class inventaire:
    
    def __init__(self, date, heure, customer, place, people, jour):
        self.auditeurs = []
        self.vehicules = []
        self.sacs_PC = []
        self.auditeurs_rayon = [['',0] for k in range(15)]
        self.date = date
        self.heure = heure
        self.customer = customer
        self.place = place
        self.people = people
        self.jour = jour

    def print_inventaire(self):
        print('inventaire à '+ str(self.customer) +', situé à '+ str(self.place)+', le '+self.jour+' '+ str(self.date)[:-9]+ ' à '+ str(self.heure)+', avec '+str(self.people)+' auditeurs \n')
        for elem in self.auditeurs:
            elem.print_auditeur()

class vehicule:
    def __init__(self, immat, nb_places, modele):
        self.immat = immat
        self.nb_places = nb_places
        self.modele = modele
        self.planning = [[True for i in range(6)] for k in range(24)]
    def print_vehicule(self):
        print('modèle '+ self.modele +', avec  '+ self.nb_places+' places, immatriculé '+self.immat+'\n')

    def est_dispo(self, inv):
        jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        h = int(inv.heure[:2])
        j = -1
        for jour in jours:
            if jour == inv.jour:
                j = jours.index(jour)
                break
        if j == -1 :
            return
        else :
            if j == 5 :
                if h <= 18:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[h+5][j]
                elif h == 19:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] 
                elif h ==20:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] 
                elif h == 21:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] 
                elif h == 22:
                    return self.planning[h][j] and  self.planning[h+1][j] 
                elif h == 23:
                    return self.planning[h][j] 
            else :
                if h <= 18:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[h+5][j]
                elif h == 19:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[0][j+1]
                elif h ==20:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[0][j+1] and  self.planning[1][j+1]
                elif h == 21:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1]
                elif h == 22:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1] and  self.planning[3][j+1]
                elif h == 23:
                    return self.planning[h][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1] and  self.planning[3][j+1] and  self.planning[4][j+1]
               
    def remplir_planning(self, inv):
        jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        h = int(inv.heure[:2])
        j = -1
        for jour in jours:
            if jour == inv.jour:
                j = jours.index(jour)
                break
        if j == -1 :
            return
        else :
            if j == 5:
                if h <= 18:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[h+5][j] = [False for k in range(6)]
                elif h == 19:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j] = [False for k in range(5)]
                elif h ==20:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j] = [False for k in range(4)]
                elif h == 21:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j]= [False for k in range(3)]
                elif h == 22:
                    self.planning[h][j], self.planning[h+1][j]= [False for k in range(2)]
                elif h == 23:
                    self.planning[h][j] = [False for k in range(1)] 
            else:
                if h <= 18:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[h+5][j] = [False for k in range(6)]
                elif h == 19:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[0][j+1] = [False for k in range(6)]
                elif h ==20:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[0][j+1],  self.planning[1][j+1] = [False for k in range(6)]
                elif h == 21:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[0][j+1], self.planning[1][j+1],  self.planning[2][j+1] = [False for k in range(6)]
                elif h == 22:
                    self.planning[h][j], self.planning[h+1][j], self.planning[0][j+1], self.planning[1][j+1], self.planning[2][j+1],  self.planning[3][j+1] = [False for k in range(6)]
                elif h == 23:
                    self.planning[h][j], self.planning[0][j+1], self.planning[1][j+1], self.planning[2][j+1], self.planning[3][j+1],  self.planning[4][j+1] = [False for k in range(6)]
    
class sac_PC:
    def __init__(self, numero, nb_pc):
        self.numero = numero
        self.nb_pc = nb_pc
        self.planning = [[True for i in range(6)] for k in range(24)]
    def print_sac_PC(self):
        print('Sac n° '+ self.numero +', avec  '+ self.nb_pc+' PCs'+'\n')
    def est_dispo(self, inv):
        jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        h = int(inv.heure[:2])
        j = -1
        for jour in jours:
            if jour == inv.jour:
                j = jours.index(jour)
                break
        if j == -1 :
            return
        else :
            if j == 5 :
                if h <= 18:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[h+5][j]
                elif h == 19:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] 
                elif h ==20:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] 
                elif h == 21:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] 
                elif h == 22:
                    return self.planning[h][j] and  self.planning[h+1][j] 
                elif h == 23:
                    return self.planning[h][j] 
            else :
                if h <= 18:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[h+5][j]
                elif h == 19:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[h+4][j] and  self.planning[0][j+1]
                elif h ==20:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[h+3][j] and  self.planning[0][j+1] and  self.planning[1][j+1]
                elif h == 21:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[h+2][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1]
                elif h == 22:
                    return self.planning[h][j] and  self.planning[h+1][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1] and  self.planning[3][j+1]
                elif h == 23:
                    return self.planning[h][j] and  self.planning[0][j+1] and  self.planning[1][j+1] and  self.planning[2][j+1] and  self.planning[3][j+1] and  self.planning[4][j+1]
               
    def remplir_planning(self, inv):
        jours = ['Samedi','Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        h = int(inv.heure[:2])
        j = -1
        for jour in jours:
            if jour == inv.jour:
                j = jours.index(jour)
                break
        if j == -1 :
            return
        else :
            if j == 5:
                if h <= 18:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[h+5][j] = [False for k in range(6)]
                elif h == 19:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j] = [False for k in range(5)]
                elif h ==20:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j] = [False for k in range(4)]
                elif h == 21:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j]= [False for k in range(3)]
                elif h == 22:
                    self.planning[h][j], self.planning[h+1][j]= [False for k in range(2)]
                elif h == 23:
                    self.planning[h][j] = [False for k in range(1)] 
            else:
                if h <= 18:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[h+5][j] = [False for k in range(6)]
                elif h == 19:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[h+4][j],  self.planning[0][j+1] = [False for k in range(6)]
                elif h ==20:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[h+3][j], self.planning[0][j+1],  self.planning[1][j+1] = [False for k in range(6)]
                elif h == 21:
                    self.planning[h][j], self.planning[h+1][j], self.planning[h+2][j], self.planning[0][j+1], self.planning[1][j+1],  self.planning[2][j+1] = [False for k in range(6)]
                elif h == 22:
                    self.planning[h][j], self.planning[h+1][j], self.planning[0][j+1], self.planning[1][j+1], self.planning[2][j+1],  self.planning[3][j+1] = [False for k in range(6)]
                elif h == 23:
                    self.planning[h][j], self.planning[0][j+1], self.planning[1][j+1], self.planning[2][j+1], self.planning[3][j+1],  self.planning[4][j+1] = [False for k in range(6)]        
    
            
            
