import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

gw_text = '''
**According to Pew Research, the gender wage gap in 2020 was 16% - 
meaning that for every one dollar a man makes, a woman makes 84 
cents. There are several factors that contribute to this gap - 
one of the most notable is the over representation of women in 
lower paying jobs. Many factors could attribute to this - blatent 
sexism and discrimination, slowed or stunted career trajectories 
due to family leave, and education level. However, according to the 
US Depatment of Labor (USDL), women ear less than men in each race 
and education level. So not only are women over represented in lower 
paying jobs, they are also paid less than men for those jobs. This is 
especially relevant coming out of the pandemic, which the USDL reports 
has set the gender wage gap back about 30 years.**
'''

gss_text = '''
**GSS stands for the General Social Survey. The GSS is a survey conducted 
in the United States to determine trends in mindset and opinions on political 
and societal issues. This survey provides reliable data to many stakeholders, 
including students, policy makers, media, and more. The GSS questions are frequently 
adapted to provide relevant, up to date information on societal trends. Many 
papershave been published using this data, and much can be deduced from this information.**
'''

'''
**Pew Research: https://www.pewresearch.org/fact-tank/2021/05/25/gender-pay-gap-facts/**

**US Dept Labor: https://blog.dol.gov/2021/03/19/5-facts-about-the-state-of-the-gender-pay-gap**
'''

gss2 = gss_clean[['sex', 'income', 'job_prestige', 'socioeconomic_index', 'education']]
gss2 = gss2.groupby('sex').agg({'income':'mean', 
                         'job_prestige':'mean', 
                         'socioeconomic_index':'mean', 
                         'education':'mean'})
gss2 = gss2.round(2).reset_index()
gss2 = gss2.rename({'sex':'Sex', 
                    'income':'Mean Income', 
                    'job_prestige':'Mean Occupational Prestige', 
                    'socioeconomic_index':'Mean Socioeconomic Index', 
                    'education':'Mean Years of Education'}, axis=1)

table2 = ff.create_table(gss2)

gss3 = gss_clean[['sex', 'male_breadwinner']]

colpercent = round(100*pd.crosstab(gss3.male_breadwinner, gss3.sex, normalize='columns'),2).reset_index()
colpercent = pd.melt(colpercent, id_vars = 'male_breadwinner', value_vars = ['male','female'])
colpercent = colpercent.rename({'value':'colpercent'}, axis=1)
colpercent

fig3 = px.bar(colpercent, x='male_breadwinner', y='colpercent', color='sex',
            labels={'male_breadwinner':'Response to Question', 'colpercent':'Percent'},
            barmode = 'group')
fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))

fig4 = px.scatter(gss_clean, x='job_prestige', y='income',
                 trendline='ols',
                 color='sex',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                        'income':'Annual Income (USD)'},
                 hover_data=['education', 'socioeconomic_index'])
fig4.update(layout=dict(title=dict(x=0.5)))

fig51 = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Annual Income (USD)', 'sex':''},
            color_discrete_map = {'male':'orange', 'female':'pink'})
fig51.update(layout=dict(title=dict(x=0.5)))
fig51.update_layout(showlegend=False)

fig52 = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Occupational Prestige', 'sex':''},
            color_discrete_map = {'male':'orange', 'female':'pink'})
fig52.update(layout=dict(title=dict(x=0.5)))
fig52.update_layout(showlegend=False)

gss6 = gss_clean[['income', 'sex', 'job_prestige']]
gss6['job_prestige_cat'] = pd.cut(gss6.job_prestige, bins=6, labels=[1,2,3,4,5,6])
gss6 = gss6[gss6.income.notnull() & gss6.sex.notnull() & gss6.job_prestige.notnull() & gss6.job_prestige_cat.notnull()]

fig6 = px.box(gss6, x='income', y = 'sex', color = 'sex',
             facet_col='job_prestige_cat', facet_col_wrap=2,
             labels={'income':'Annual Income (USD)', 'job_prestige_cat':''},
            color_discrete_map = {'male':'orange', 'female':'pink'})

fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("=", "")))
fig6.update(layout=dict(title=dict(x=0.5)))





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

    
app.layout = html.Div([
    
    html.H1("GSS Findings"),
    dcc.Markdown(gw_text),
    dcc.Markdown(gss_text),
    
    html.H4("Mean Statistics for Men Vs. Women"),
    dcc.Graph(figure=table2),
    
    html.H4("Response to \"It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.\" for Men Vs. Women"),
    dcc.Graph(figure = fig3),
    
    html.H4("Occupational Prestige Vs. Income for Men & Women"),
    dcc.Graph(figure = fig4),
    
    html.H4("Distribution of Income and Occupational Prestige Status for Men & Women"),
    dcc.Graph(figure = fig51),
    dcc.Graph(figure = fig52),
    
    html.H4("Distribution of Income for each Occupational Prestige category for Men & Women"),
    dcc.Graph(figure=fig6)    
    ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
