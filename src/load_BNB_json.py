import pickle
import pandas as pd

def load_BNB_data():
    '''
    Loads json data from listings at Airbnb.com and returns a clean Pandas DF
    '''
    with open('/Users/isaaccampbell-smith/gal/AirBNB_Rentals/data/Tacomabnb.pkl', 'rb') as f:
        j_dict_list = pickle.load(f)
        
    out = pd.DataFrame()
    
    for j_dict in j_dict_list:
        #most of the data seems to be located in the 1st 'sections' index, some in the 0th
        #this try/except function resolves that
        try:
            clean_dict = clean_and_convert(j_dict, 1)
        except:
            clean_dict = clean_and_convert(j_dict, 0)
            
        out = pd.concat([out, pd.DataFrame(clean_dict)], ignore_index=True)
        
    return out

def clean_and_convert(j_dict, idx):
    #isolates relevant section before grabbing specific keys
    d = j_dict['data']['dora']['exploreV3']['sections'][idx]['items']
    #d = dic['data']['dora']['exploreV3']['sections'][idx]['items']
    #explicitly call out the fields we want to extract
    out = {'id':[], 'neighborhood':[], 'host_id':[],
           'name':[], 'avgRating':[], 'reviewsCount':[],
           'bathrooms':[], 'bedrooms':[], 'beds':[],
           'roomAndPropertyType': [],
           'roomTypeCategory': [],
           'roomType': [],
           'price': [],
           'lat':[], 'lng':[]}
    #loop through every rental on page
    for i in range(len(d)):
        sub = d[i]['listing']
        #loop through every key we want
        for k in out.keys():
            if k in sub:
                out[k].append(sub[k])

        #go several levels deeper for this information        
        out['host_id'].append(sub['user']['id'])
        out['price'].append(d[i]['pricingQuote']['rate']['amount'])

    return out