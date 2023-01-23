from database.connector import con
import pandas as pd


poll = pd.read_sql(sql="SELECT * FROM survey_poll", con=con)
questions = pd.read_sql(sql="SELECT * FROM survey_question", con=con)
answers = pd.read_sql(sql="SELECT * FROM survey_answer", con=con)

