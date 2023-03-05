# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 13:47:31 2020

@author: mnelz
"""

# LeadProfiler 

# Profile

import numpy as np
import pandas as pd
from GoogleNews import GoogleNews
import wikipedia
from lxml import html

class LeadProfile():
    
    def __init__(self, lead_person, lead_company, topic, branch, 
                 start='01/01/2018', end='12/31/2020'):
        self.lead_person = lead_person
        self.lead_company = lead_company
        self.topic = topic
        self.branch = branch
        self.start = start
        self.end = end
        
        wikipedia.set_lang("de")  
        
    def get_company_info(self, return_value = 'dict'):#
    
        self.page = wikipedia.page(self.lead_company)
        #print(page.content)
        #print(page.links)
        #print(page.images)
        #print(page.summary)
        self.page.categories
        tree = html.fromstring(self.page.html())
        
        z = tree.xpath('//table[@id="Vorlage_Infobox_Unternehmen"]/tbody/descendant::*/text()')
        
        z = [i.replace('\n','').replace('\xa0','') for i in z if i not in ['\n', '\xa0', ', ', '[1]']]
        
        self.company_info = {}
        self.company_info['comp_name'] = z.pop(0)
        self.company_info['infostand'] = z.pop(len(z)-1)
        
        company_info = self.split_at_values(z)
        company_info = [i for i in company_info if i] # delete empty lists from list
        for info in company_info:
            key, value = info[0], info[1:]
            self.company_info[key] = value
        # Handelsregister Anreicherungen:
        # matchparam: company_id:
        #companies = pd.read_csv('E:/Braincourt/LeadProfiler/Data/company.csv')
        #officers = pd.read_csv('E:/Braincourt/LeadProfiler/Data/officer.csv')
        return self.company_info
        
     
    def get_company_summary(self):
        
        self.page = wikipedia.page(self.lead_company)
        self.company_summary = self.page.summary
        return self.company_summary
    
    def split_at_values(self, lst, 
                        values = ['Rechtsform', 'ISIN', 'Gründung', 
                                  'Sitz', 'Leitung', 'Mitarbeiterzahl', 
                                  'Umsatz', 'Branche', 'Website']):
        # Teile liste an den values auf:
            
        indices = [i for i, x in enumerate(lst) if x in values]
        result_list = []
        for start, end in zip([0, *indices], [*indices, len(lst)]):
            result_list.append(lst[start:end])
            
        return result_list
    
    def get_person_info(self):
        # from xing, linkedin, google 
        pass
    
    def get_company_news(self, return_value = 'data'): 

        gn = GoogleNews(start = self.start, end = self.end)
        gn.set_lang('de')
        gn.search(self.lead_company) # Seite 1 wird automatisch geladen.
        
        # Überprüfe Seite 2 bis 10
        for i in range(2,10): 
            gn.getpage(i)
            
        self.company_news = pd.DataFrame(gn.result())
        
        return self.company_news
    
    def get_topic_news(self, return_value = 'data'): 

        gn = GoogleNews(start = self.start, end = self.end)
        gn.set_lang('de')
        searchterm = self.topic + ' ' + self.branch
        gn.search(searchterm) # Seite 1 wird automatisch geladen.
        
        # Überprüfe Seite 2 bis 10
        for i in range(2,10): 
            gn.getpage(i)
            
        self.topic_news = pd.DataFrame(gn.result())
        
        return self.topic_news  
            
    
        

    
if __name__ == '__main__':
    lead_profile = LeadProfile('Michael Nelz', 'Gühring', 'Data Science', 'Innovation')
    company_news = lead_profile.get_company_news()    
    print(company_news)
    company_info = lead_profile.get_company_info()
    print(company_info)
    topic_news = lead_profile.get_topic_news()
    print(topic_news)
    # get knowledgegraph:
    # request auf:
    # 'https://kgsearch.googleapis.com/v1/entities:search?query=taylor+swift&key=' + my_api_key + '&limit=1&indent=True'
 
