    round_mult = 100000
    rampen_df['Intensity'] = 0
    for i in range(len(rampen_df)):
        a = Population[Population['Country Code']==rampen_df['ISO'][i]]
        if len(a) == 1:
            rampen_df['Intensity'][i] = (rampen_df['Total Deaths'][i]+Total_affected_mult*rampen_df['Total Affected new'][i])/(a[str(rampen_df['Year'][i])].values[0])


    rampen_df = rampen_df[rampen_df['Intensity'] >= Intensity_threshold].reset_index(drop=True)
    rampen_df = rampen_df[['Year', 'ISO', 'Country', 'Disaster Group', 'Disaster Subgroup', 'Disaster Type',
           'Disaster Subtype', 'Total Deaths', 'Total Affected new', 'Intensity', 'Jaar 0', 'Jaar 1', 'Jaar 2', 'Jaar 3']]




    quantiles = rampen_df.groupby(['Disaster Group', 'Disaster Subgroup', 'Disaster Type','Disaster Subtype'])['Intensity'].quantile([0.25, 0.75]).reset_index()
    quantiles = quantiles.pivot(index=['Disaster Group', 'Disaster Subgroup', 'Disaster Type','Disaster Subtype'], 
                                columns = 'level_4', values='Intensity').reset_index()
    test = rampen_df.merge(quantiles, left_on=['Disaster Group', 'Disaster Subgroup', 'Disaster Type','Disaster Subtype'], 
                           right_on=['Disaster Group', 'Disaster Subgroup', 'Disaster Type','Disaster Subtype'], how='left')
    test.columns = ['Year','ISO','Country','Disaster Group','Disaster Subgroup','Disaster Type',
                    'Disaster Subtype','Total Deaths','Total Affected new','Intensity','Jaar 0','Jaar 1','Jaar 2','Jaar 3',"0.25",'0.75']
    test['Category']=0
    for index, row in test.iterrows():
        test.iloc[index, test.columns.get_loc('Category')] = 3 if row['Intensity']>row['0.75'] else (1 if row['Intensity']<row['0.25'] else 2)
    rampen_df['Category'] = test['Category']

    rampen_df = rampen_df.sort_values(by='Year').reset_index(drop=True)
