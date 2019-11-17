#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:07:58 2019

@author: federivadeneira@gmail.com
"""
import pandas as pd

# Leemos la info de las categorias de Ebay
DATA_CATEGORIES = pd.read_csv('./data/DE_New_Structure_(Oct2019).csv')
FIRST_LEVEL_INDEXES = [i for i, row in enumerate(DATA_CATEGORIES['lv1']) if type(row) == str]
SECOND_LEVEL_INDEXES = [i for i, row in enumerate(DATA_CATEGORIES['lv2']) if type(row) == str]

class categoryMapper: 

    def __init__(self): 
        pass
    
    def __str__(self):
        return 'Ebay Class Category Mapper (lv1 >> lv2 >> lv ... to Ebay_Cat_Id)'
        
    def map_first_level(self, first_level_name): 
        '''
        This method maps the first level according to the category name
    
        Parameters
        ----------
        name_in : string
            Category's name
    
        Returns
        -------
        Category ID
    
        '''    
        first_level_name = first_level_name.lower()
        # Filtering
        categories = [i for i, x in enumerate(DATA_CATEGORIES['lv1']) if type(x) == str and x.lower() == first_level_name]
        if len(categories) == 1: 
            return DATA_CATEGORIES['id'].iloc[categories[0]]
        else:
            raise Exception('Error: Either was found any or more than one category id for: {}'.format(first_level_name))
        
    def get_margins_indexes_first_level(self, category_id): 
        '''
        This method returns the limits (indexes in the dataframe) that wraps the
        possible downstream ids given a first level category
    
        Parameters
        ----------
        category_id : Int
            ID of the first level category
    
        Returns
        -------
        lower_index : Int
            Lower index in which we can search for the second level
        upper_index: Int
            Upper index in which we can search for the second level
    
        '''
        lower_index = DATA_CATEGORIES[DATA_CATEGORIES['id'] == category_id].index.tolist()
        if len(lower_index) == 1: 
            lower_index = lower_index[0]
        else:
            raise Exception('Error: It was not found any index for the category ID {}'.format(category_id))
        # Looking fot the next index in FIRST_LEVEL_INDEXES
        indice_cat_in = [i for i, x in enumerate(FIRST_LEVEL_INDEXES) if x == lower_index]
        if len(indice_cat_in) == 1: 
            indice_cat_in = indice_cat_in[0]
        else:
            raise Exception('Error: The index {} was not found in the FIRST_LEVEL_INDEXES object'.format(lower_index))
        upper_index = FIRST_LEVEL_INDEXES[indice_cat_in+1]
        return lower_index, upper_index
    
    def map_second_level(self, parent_id_name, second_level_name):
        '''
        This method maps the id for the second level category
        
        Parameters
        ----------
        parent_id: string
            First level category name
        second_level_name: string
            Second level category name
            
        Returns
        -------
        tuple : (id_second_level, lower_index, upper_index)
        '''
        second_level_name = second_level_name.lower()
        lower_index, upper_index = self.get_margins_indexes_first_level(self.map_first_level(parent_id_name))
        data_categories_subset = DATA_CATEGORIES.iloc[lower_index:upper_index]
        
        categories_second_level = [(x['id'], x['lv2'].lower()) for index, x in data_categories_subset[['id', 'lv2']].iterrows() if type(x['lv2']) == str]
        id_second_level = [id_lv2 for id_lv2, name in categories_second_level if name == second_level_name]
        if len(id_second_level) == 1: 
            id_second_level = id_second_level[0]
            # Obtenemos los margenes del segundo nivel para mapear tercero y cuarto
            index_second_level = DATA_CATEGORIES[DATA_CATEGORIES['id'] == id_second_level].index.tolist()[0]
            lower_index = index_second_level
            indice_en_lista = [i for i, x in enumerate(SECOND_LEVEL_INDEXES) if x == lower_index][0]
            upper_index = SECOND_LEVEL_INDEXES[indice_en_lista+1]
            return(id_second_level, lower_index, upper_index)
            
        else:
            raise Exception('More than one id was found for the corresponding name: {}'.format(second_level_name))
    
    def map_n_level(self, n_level_name, n_level, lower_margin, upper_margin):
        '''
        This method maps n_categories from the third level onwards. 
        Recommended is to map up to the fourth level because E-Commerces taxonomies
        are usually not real taxonomies in the phylogenetic sense. 
        
        Parameters
        ----------
        n_level_name: string
            Name of the category to search for
        
        n_level: string
            Level of the taxonomy on which the category lies
            
        lower_margin: Int
            Lower index, coming from the execution of map_second_level()
            
        upper_margin: Int
            Upper index, coming from the execution of map_second_level()
            
        Returns
        -------
        id_category_n_level: int/str
            Ebay's category ID
        '''
        
        n_level_name = n_level_name.lower()
        data_subset = DATA_CATEGORIES.iloc[lower_margin:upper_margin]
        categorias_n_level = [(x['id'], x[n_level].lower()) for index, x in data_subset[['id', n_level]].iterrows() if type(x[n_level]) == str]
        data_result = [id_cat for id_cat, name in categorias_n_level if name.lower() == n_level_name]
        if len(data_result) == 1:
            return(data_result[0])
        else:
            raise Exception('Error in map_n_level when looking for {}'.format(n_level_name))
    
    def get_level(self, category_in):
        '''
        This method takes a category as input, for example:
            Beauty & Gesundheit>> Make-up>> Augen>> Augenbrauenstift & -farbe
        And returns each one of the categories levels as elements of an ordered
        list (1st level > Last level) and also the number of levels detected

        Parameters
        ----------
        category_in : string
            Ebay Category following the format:
            Beauty & Gesundheit>> Make-up>> Augen>> Augenbrauenstift & -farbe

        Returns
        -------
        splitted : list
            Striped lowercase category names in ascending level order
        level : int
            Amount of levels (Natural numbers)

        '''
        splitted = category_in.split('>>')
        splitted = [x.lower().strip() for x in splitted]
        level = len(splitted)
        return splitted, level

    def map_category_to_id(self, category_in):
        '''
        This is the main method of the class. It uses the other methods to determine
        the id of a complete ebay category
        
        Parameters
        ----------
        category_in : string
            Ebay's Category following the format:
                Beauty & Gesundheit>> Make-up>> Augen>> Lidschatten
        
        Returns
        -------
        id_category : Int
            Ebay's category ID
            
        Usage
        -----
        mapper = categoryMapper()
        category_in = 'Beauty & Gesundheit>> Make-up>> Augen>> Lidschatten'
        id_category_in = mapper.map_category_to_id(category_in)
        print(id_category_in)
        '''
        splitted, level = self.get_level(category_in)
        if level > 2: 
            id_second_level, lower_index , upper_index = self.map_second_level(parent_id_name= splitted[0], second_level_name= splitted[1])
            id_category_out = self.map_n_level(n_level_name= splitted[level-1], n_level='lv{}'.format(level), lower_margin= lower_index, upper_margin=upper_index)
            return(id_category_out)
        elif level == 1:
            first_level_id = self.map_first_level(first_level_name= splitted[0])
            return(first_level_id)
        elif level == 2:
            id_second_level, lower_index, upper_index = self.map_second_level(parent_id_name= splitted[0], second_level_name= splitted[1])
            return(id_second_level)
        else:
            raise Exception('Error running map_category_id for {}'.format(category_in))

