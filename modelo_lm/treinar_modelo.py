import os
import sys
import django
import pandas as pd 
import joblib
from django_pandas.io import read_frame

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Ajuste caminho e setup django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'caoa.settings')
django.setup()

from apps.acompanhamentosfinanceiroprojeto.models import AcompanhamentoDespesasProjeto

# Consulta os dados do banco e cria dataframe
qs = AcompanhamentoDespesasProjeto.objects.select_related('projeto')
df = read_frame(qs)
df['nome_projeto'] = df['projeto'].astype(str)

# Features e target
x = df[['descricao', 'nome_projeto']]
y = df['valor']

# Codificação das features categóricas
encoder = OneHotEncoder()
x_encoded = encoder.fit_transform(x)

# Divisão treino/teste
x_train, x_test, y_train, y_test = train_test_split(x_encoded, y, test_size=0.2, random_state=42)

# Treina modelo
modelo = RandomForestRegressor()
modelo.fit(x_train, y_train)

# Salva modelo e encoder
joblib.dump(modelo, 'modelo_lm/modelo_previsao_valor.pkl')
joblib.dump(encoder, 'modelo_lm/encoder_descricoes.pkl')

print('Modelo treinado!')
