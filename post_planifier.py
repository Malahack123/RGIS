

import pandas as pd
import classes as c1
import os

def post_planifier(inventaires, auditeurs, magasins, parc_auto, parc_sac_PC) :
   
    if os.path.exists('./output/import oracle/import_oracle.xlsx'):
        os.remove('./output/import oracle/import_oracle.xlsx')


    columns = ['DISTRICT','SCHEDULEDEVENTID','BADGE_ID','FULL_NAME','STORE_NUMBER','INVENTORY_DATE','INVENTORY_TIME','CUSTOMER_NAME','CUSTOMER_NUMBER','BACKROOM_FLAG','ADDER_CODE','SUPERVISOR','MEET_SITE','MEET_DATE','MEET_TIME','START_TIME','MEET_SITE_NOTE','VILLE']

    df_import_oracle = pd.DataFrame(columns=columns)
    
    for inv in inventaires :
        for aud in inv.auditeurs:
            df = pd.DataFrame([[740,None, aud.badge_id, aud.nom_complet, inv.customer.store_number, inv.date,''.join(str(inv.heure).split(':')[:-1]), inv.customer.nom, inv.customer.customer_code, None, None, None, None, None, None, None, None,inv.place]],columns=columns)
            df_import_oracle = pd.concat([df_import_oracle, df])

    import_data = pd.ExcelWriter('./output/import oracle/import_oracle.xlsx')
    df_import_oracle.to_excel(import_data, index=False)
    import_data.save()
    
    if os.path.exists('./output/planning/planning_pc.xlsx'):
        os.remove('./output/planning/planning_pc.xlsx')
    columns = [k for k in range(7)]
    ppc = pd.DataFrame(columns=[])
    for sac in parc_sac_PC:
        header = 'n° '+str(sac.numero)+'-'+str(sac.nb_pc)+' PC'
        columns = [header, 'Samedi', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
        plann = [columns]
        for k in range(6):
            line = [str(k*4)+'h-'+str((k+1)*4)+'h','ND','ND','ND','ND','ND','ND']
            for j in range(6):
                if sac.planning[k*4][j] and sac.planning[k*4+1][j] and sac.planning[k*4+2][j] and sac.planning[k*4+3][j]:
                    line[j+1] = 'D'
            plann.append(line)
        plann.append([])
        df = pd.DataFrame(plann)
        ppc = pd.concat([ppc,df])

    import_data = pd.ExcelWriter('./output/planning/planning_pc.xlsx')

    def highlight_green_val (stringo) :
    
        critere_dispo = stringo == 'D'
        return ['background-color: green' if i else '' for i in critere_dispo]

    def highlight_red_val (stringo) :
    
        critere_non_dispo = stringo == 'ND'
        return ['background-color: red' if i else '' for i in critere_non_dispo]
      
    ppc = ppc.reset_index(drop=True).style.apply(highlight_green_val)
    ppc = ppc.apply(highlight_red_val)
    ppc.to_excel(import_data, index=False)
    import_data.save()

    if os.path.exists('./output/planning/planning_vehicules.xlsx'):
        os.remove('./output/planning/planning_vehicules.xlsx')
    columns = [k for k in range(7)]
    p_vehicule = pd.DataFrame(columns=[])
    for vehicule in parc_auto:
        header = 'n° '+str(vehicule.immat)+'-'+str(vehicule.nb_places)+' PL'
        columns = [header, 'Samedi', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
        plann = [columns]
        for k in range(6):
            line = [str(k*4)+'h-'+str((k+1)*4)+'h','ND','ND','ND','ND','ND','ND']
            for j in range(6):
                if vehicule.planning[k*4][j] and vehicule.planning[k*4+1][j] and vehicule.planning[k*4+2][j] and vehicule.planning[k*4+3][j]:
                    line[j+1] = 'D'
            plann.append(line)
        plann.append([])
        df = pd.DataFrame(plann)
        p_vehicule = pd.concat([p_vehicule,df])

    import_data = pd.ExcelWriter('./output/planning/planning_vehicules.xlsx')
    p_vehicule = p_vehicule.reset_index(drop=True).style.apply(highlight_green_val)
    p_vehicule = p_vehicule.apply(highlight_red_val)
    p_vehicule.to_excel(import_data, index=False)
    import_data.save()
