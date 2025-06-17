import os
import sys
import django
import pandas as pd
import joblib

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from django.db.models import F


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caoa.settings")
django.setup()

from apps.acompanhamentosfinanceiroprojeto.models import AcompanhamentoDespesasProjeto

qs = AcompanhamentoDespesasProjeto.objects.select_related('projeto').annotate(
    nome_projeto=F('projeto__cliente'),
    tipo_servico=F('projeto__tipo_serviço')
).values('descricao', 'valor', 'nome_projeto', 'tipo_servico')

df = pd.DataFrame.from_records(qs)

x = df[['descricao', 'nome_projeto', 'tipo_servico']]
y = df['valor']

encoder = OneHotEncoder()
x_encoded = encoder.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(
    x_encoded, y, test_size=0.2, random_state=42
)

modelo = RandomForestRegressor()
modelo.fit(x_train, y_train)

os.makedirs('modelo_lm', exist_ok=True)
joblib.dump(modelo, 'modelo_lm/modelo_previsao_valor.pkl')
joblib.dump(encoder, 'modelo_lm/encoder_descricoes.pkl')

print('Modelo treinado!')
