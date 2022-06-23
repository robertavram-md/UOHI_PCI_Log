#!/usr/bin/env python
# coding: utf-8

# In[48]:

import sys
import pandas as pd
import numpy as np
def compute_lesion_vessels(df, column='L1'):
    lesion = column + ' Lesion Vessel'
    segment = column + ' Segment Number'
    stent = column + ' Total Number of Stents Placed'
    df[lesion] = np.where(df[segment]==5, 'Left Main', np.where(df[segment].isin([6,7,8,9,10]),'LAD',np.where(df[segment].isin([11,12,13,14,15]),'LCx',np.where(df[segment].isin([1,2,3,4,5]),'RCA','NA'))))
    df[stent] = pd.to_numeric(df[stent], errors='coerce').fillna(0)
    return df
def init(file):
    df = pd.read_excel(file)
    df['Procedure_Date'] = df['Procedure Date']
    df2_columns = df.filter(like='Number of Stents Placed').columns.values
    df2 = df[df2_columns]
    df['stent_placed'] = ['Yes' if x >= 1 else 'No' for x in np.sum(((df2.values == 1)|(df2.values == 2)), 1)]
    df['stent_number_lesions'] = [x if x >= 1 else 'No' for x in np.sum(((df2.values == 1)|(df2.values == 2)), 1)]
    df2_columns = df.filter(like='Intervention Performed').columns.values
    df2 = df[df2_columns]

    df['ffr_or_ivus_or_oct_or_pci'] = ['Yes' if x >= 1 else 'No' for x in np.sum(df2.values == 'Yes', 1)]
    df2_columns = df.filter(like='Balloon Angioplasty').columns.values
    df2 = df[df2_columns]
    df['balloon_angioplasty'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]
    #df3 = df2.loc[df2.apply(lambda x: 'Yes' in x.values, axis=1).any()]
    df['intervention_performed'] = np.where((df['stent_placed']=='Yes')|(df['balloon_angioplasty']=='Yes'), 1, 0)


    df2_columns = df.filter(like='FFR').columns.values
    df2 = df[df2_columns]
    df['ffr_performed'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]

    df2_columns = df.filter(like='IVUS').columns.values
    df2 = df[df2_columns]
    df['ivus_performed'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]

    df2_columns = df.filter(like='OCT').columns.values
    df2 = df[df2_columns]
    df['oct_performed'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]


    df2_columns = df.filter(like='Guideliner Used').columns.values
    df2 = df[df2_columns]
    df['guideliner_used'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]



    df['hemodynamic_instability'] = np.where(((df['Intubated pre-cath']=='yes')|(df['ROSC']!='no')|(df['Procedural Complications Arrest']=='Yes')|(df['Procedural Complications Shock']=='Yes')), 'Yes','No')
    #Defined as ROSC, or intubated or periprocedural arrest or shock


    df2_columns = df.filter(like='Thrombectomy').columns.values
    df2 = df[df2_columns]
    df['thrombectomy_used'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]
    df2_columns = df.filter(like='Distal protection').columns.values
    df2 = df[df2_columns]
    df['distal_protection_used'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]
    df2_columns = df.filter(like='Rotablator').columns.values
    df2 = df[df2_columns]
    df['rotablator_used'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]
    df2_columns = df.filter(like='Cutting balloon').columns.values
    df2 = df[df2_columns]
    df['cutting_balloon_used'] = ['Yes' if x >= 1 else 'No' for x in np.sum((df2.values == 'Yes'), 1)]
    for lesions in ['L1', 'L2', 'L3','L4','L5','L6','L7','L8','L9','L10']:
        df = compute_lesion_vessels(df, lesions)

    print(df.stent_placed.value_counts())
    print(df.ffr_performed.value_counts())
    print(df.ivus_performed.value_counts())
    print(df.oct_performed.value_counts())

    print(df.balloon_angioplasty.value_counts())
    print(df.intervention_performed.value_counts())
    print(df.STEMI.value_counts())
    #print(df.STEMI_Type.value_counts())
    print(df.ffr_or_ivus_or_oct_or_pci.value_counts())

    print(df.hemodynamic_instability.value_counts())
    #print(df.Procedural_Complications_Present.value_counts())
    return df

# In[330]:


#print("Values between the two dates", df.Procedure_Date.min(),  df.Procedure_Date.max())
#print("Vascular Access", df.Access_Site_Utilized.value_counts())


# ## Diagnostics vs PCI

# In[331]:

def compute_multi_vessel(df_intervention):
    column_list =  ['L1','L2', 'L3','L4','L5','L6','L7','L8','L9','L10']
    for index, row in df_intervention.iterrows():
        for column in column_list:
            lesion = column + ' Lesion Vessel'
            stent = column + ' Total Number of Stents Placed'
            balloon = column + ' Balloon Angioplasty?'
            if (row[stent]==1) | (row[stent]==2)|(row[balloon]=='Yes'):
                #found a vessel that was stented
                list_copy = column_list
                list_copy.remove(column)
                vessel_stented = row[lesion]

                for filtered_column in list_copy:
                    filtered_lesion = filtered_column + ' Lesion Vessel'
                    filtered_stent = filtered_column + ' Total Number of Stents Placed'
                    filtered_balloon = filtered_column + ' Balloon Angioplasty?'
                    if (row[filtered_stent] == 1) | (
                        row[filtered_stent] == 2
                    ) | (row[filtered_balloon] == 'Yes') and (
                        vessel_stented
                    ) != row[
                        filtered_lesion
                    ]:
                        df_intervention.at[index,'multi_vessel'] = True
                        break
    return df_intervention

# In[319]:

def compute_bifurcation(df_intervention):
    column_list =  ['L1','L2', 'L3','L4','L5','L6','L7','L8','L9','L10']
    #TODO : CLASSIFY MEDINA FOR BIFURCATIONS
    #TODO : CLASSIFY TECHNIQUE

    for index, row in df_intervention.iterrows():
        for column in column_list:
            lesion = column + ' Lesion Vessel'
            stent = column + ' Total Number of Stents Placed'
            balloon = column + ' Balloon Angioplasty?'
            bifurcation = column + ' Bifurcation Lesion'

            if (row[stent]==1) | (row[stent]==2)|(row[balloon]=='Yes'):
                if (row[bifurcation]=='Yes'):
                    df_intervention.at[index,'bifurcation_interv'] = True
                    break
                elif column=='L10':
                    df_intervention.at[index,'bifurcation_interv'] = False
    return df_intervention

def compute_left_main(df_intervention):
    column_list =  ['L1','L2', 'L3','L4','L5','L6','L7','L8','L9','L10']
    #TODO : CLASSIFY MEDINA FOR BIFURCATIONS
    #TODO : CLASSIFY TECHNIQUE

    for index, row in df_intervention.iterrows():
        for column in column_list:
            lesion = column + ' Lesion Vessel'
            stent = column + ' Total Number of Stents Placed'
            balloon = column + ' Balloon Angioplasty?'
            bifurcation = column + ' Bifurcation Lesion'

            if (row[stent]==1) | (row[stent]==2)|(row[balloon]=='Yes'):
                if (row[lesion]=='Left Main'):
                    df_intervention.at[index,'lm_interv'] = True
                    break
                elif column=='L10':
                    df_intervention.at[index,'lm_interv'] = False
    return df_intervention

# In[320]:


def generate_intervention_dataframe(df):
    df_intervention = df.loc[df['intervention_performed']==1].reset_index()

    df_intervention = compute_multi_vessel(df_intervention)
    df_intervention = compute_bifurcation(df_intervention)
    df_intervention = compute_left_main(df_intervention)
    df_intervention['complex_cad_case'] = np.where(((df_intervention['guideliner_used']=='Yes') | (df_intervention['thrombectomy_used']=='Yes') | (df_intervention['distal_protection_used']=='Yes') | (df_intervention['rotablator_used']=='Yes') | (df_intervention['cutting_balloon_used']=='Yes')| (df_intervention['lm_interv']==True) | (df_intervention['bifurcation_interv']==True)), 1, 0)
    return df_intervention

# In[321]:

def generate_summary_dataframe(df, df_intervention):
    objective = [
        'Radial Access',
        'Femoral Access',
        'Brachial Access',
        'Number of diagnostic cases',
        'Number of FFR, IVUS, OCT or PCI cases',
        'Number of FFR, IVUS, OCT or PCI cases',
        'FFR cases',
        'IVUS cases',
        'OCT cases',
        'PCI cases',
        'STEMI',
        'Hemodynamic Instability [Shock, Arrest, ROSC, Intubated]',
        'Multivessel PCI',
        'Bifurcation PCI',
        'Left Main PCI',
        'Complex CAD [Bifurcation, Calcifried, LM, CTO or thrombotic]',
    ]

    count = [
        len(df.loc[df['Access Site Utilized'] == 'Radial']),
        len(df.loc[df['Access Site Utilized'] == 'Femoral']),
        len(df.loc[df['Access Site Utilized'] == 'Brachial']),
        len(df.loc[df['ffr_or_ivus_or_oct_or_pci'] == 'No']),
        len(df.loc[df['ffr_or_ivus_or_oct_or_pci'] == 'Yes']),
        len(df.loc[df['ffr_or_ivus_or_oct_or_pci'] == 'Yes']),
        len(df.loc[df['ffr_performed'] == 'Yes']),
        len(df.loc[df['ivus_performed'] == 'Yes']),
        len(df.loc[df['oct_performed'] == 'Yes']),
        len(df.loc[df['stent_placed'] == 'Yes']),
        len(df.loc[df['STEMI'] == 'yes']),
        len(df.loc[df['hemodynamic_instability'] == 'Yes']),
        len(df_intervention.loc[df_intervention['multi_vessel'] == True]),
        len(
            df_intervention.loc[df_intervention['bifurcation_interv'] == True]
        ),
        len(df_intervention.loc[df_intervention['lm_interv'] == True]),
        len(df_intervention.loc[df_intervention['complex_cad_case'] == True]),
    ]

    return pd.DataFrame(
        list(zip(objective, count)), columns=['Objective', 'Number']
    )

# In[322]:


def save_files(df, df_intervention, df_count):
    from datetime import date

    today = date.today()
    output_count = f'condensed_summary_{str(today)}.csv'
    intervention_output = f'interventions_{str(today)}.csv'
    overall_output = f'overall_{str(today)}.csv'
    df.to_csv(overall_output)
    df_intervention.to_csv(intervention_output)
    df_count.to_csv(output_count)


# In[342]:


def generate_summary(path):
    import sys
    try:
        file = open(path, 'r')
        df = init(path)
        df_intervention = generate_intervention_dataframe(df)
        df_count = generate_summary_dataframe(df, df_intervention)
        save_files (df, df_intervention, df_count)
        return print('Files generated successfully')
    except IOError:
        return print('There was an error opening the file', path)



# In[344]:


if __name__ == '__main__':
    #globals()[sys.argv[1]](sys.argv[2])
    generate_summary(sys.argv[1])

# In[ ]:
