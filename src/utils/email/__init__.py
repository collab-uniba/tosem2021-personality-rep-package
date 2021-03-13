import nltk
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

nltk.download('punkt')
nltk.download('stopwords')


def training_nlon():
    _nlon = importr('NLoN')
    # Path to NLoN training data
    robjects.r['load']('src/utils/email/training_data.rda')
    return _nlon, _nlon.NLoNModel(robjects.r['text'], robjects.r['rater'])


nlon, nlon_model = training_nlon()
punc = '''()-[]{};:'"\, <>/?@#$%^&*_~'''
