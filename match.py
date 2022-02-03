'''
    Octavian Tabacaru
'''

import warnings
warnings.filterwarnings('ignore')
from pymatch.Matcher import Matcher
import pandas as pd
import numpy as np
from flask import Flask

app = Flask(__name__)

''' path '''
path = "sales_data/MARS 9.xlsx"

''' load data, activity stores '''
data = pd.read_excel(path, sheet_name=0)
act_stores = pd.read_excel(path, sheet_name=1)
act_stores = pd.DataFrame(act_stores['dist'].unique())

''' label test stores'''
data['Test'] = data['Store'].apply(lambda x: True if x in act_stores.values else False)

''' sample data'''
data = data[data.Test == True].sample(20000, random_state=42) \
    .append(data[data.Test == False].sample(2000, random_state=42))
test = data[data.Test == True]
control = data[data.Test == False]

''' relabel sample test col '''
test['Test'] = 1
control['Test'] = 0

''' begin matching '''
m = Matcher(test, control, yvar="Test", exclude=[])
np.random.seed(20170925)
# m.fit_scores(balance=True, nmodels=10)
# m.predict_scores()
m.tune_threshold(method='random')
plot = m.plot_scores()
plot
m.match(method="min", nmatches=1, threshold=1)
m.record_frequency()
m.assign_weight_vector()
matched = m.matched_data.sort_values("match_id")

# matched.to_excel("results__.xlsx")

@app.route("/")
def home():
    html = matched.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    top = '<!doctype html>' \
          '<html lang="en">' \
          '<head>' \
          '<meta charset="utf-8">' \
          '<meta name="viewport" content="width=device-width, initial-scale=1">' \
          '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">' \
          '</head>'
    body = '<body>' \
           f'{r_string}' \
           '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>' \
           '</body>' \
           '</html>'
    return top + body

app.run()
