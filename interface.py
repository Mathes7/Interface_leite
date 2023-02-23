#%% interface.
import streamlit as st   
import pandas as pd
from sklearn.model_selection import train_test_split #divide o modelo em modelo de teste e treino.
from sklearn.ensemble import RandomForestClassifier # modelo de machine random forest.

st.set_page_config(
    page_title = 'Predições da qualidade do leite',
    page_icon = '🐮',
)

df = pd.read_csv("dados/milknew.csv")

#treinamento dos dados.

# em x estão todas as informações e em y estão as respostas para serem alcançadas
x = df.drop(columns=['Grade','Colour'])
y = df['Grade']

[x_train, x_test, y_train, y_test] = train_test_split( x,y, test_size = 0.2 )

random_forest_df = RandomForestClassifier(n_estimators = 10, criterion = 'gini', max_features = 'sqrt',random_state = 0)
random_forest_df.fit(x_train, y_train)

previsoes = random_forest_df.predict(x_test) # jogando os dados de teste para tentar prever.

#%% interface.


def get_user_data():
    pH = st.sidebar.slider('pH do leite', 0, 9, 1)
    Temprature = st.sidebar.slider('Temperatura do leite', 1, 50, 1)
    Taste = st.selectbox('Sabor do leite', ['0','1'])
    Odor = st.selectbox('Odor do leite', ['0','1'])
    Fat = st.selectbox('Nível de gordura leite', ['0','1'])
    Turbidity = st.selectbox('Nível de turbidez leite', ['0','1'])
    
    user_data = {'pH do leite': pH,
                'Temperatura do leite': Temprature,
                'Sabor do leite': Taste,
                'Odor do leite': Odor,
                'Nível de gordura leite': Fat,
                'Nível de turbidez leite': Turbidity
                }
    
    features = pd.DataFrame(user_data, index=[0])
    
    return features 

user_input_variables = get_user_data()


predict = random_forest_df.predict(user_input_variables)

st.subheader('Qualidade: ')
st.write(predict)
