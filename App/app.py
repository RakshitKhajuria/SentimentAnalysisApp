# Core Pkgs
import streamlit as st 
import altair as alt
import plotly.express as px 

# EDA Pkgs
import pandas as pd 
import numpy as np 
from datetime import datetime

# Utils
import joblib 
pipe_lr = joblib.load(open("models/emotion_classifier_pipe_lr_03_june_2021.pkl","rb"))


# # Track Utils
# from track_utils import create_page_visited_table,add_page_visited_details,view_all_page_visited_details,add_prediction_details,view_all_prediction_details,create_emotionclf_table

# Fxn
def predict_emotions(docx):
	results = pipe_lr.predict([docx])
	return results[0] #string

def get_prediction_proba(docx):
	results = pipe_lr.predict_proba([docx])
	return results

emotions_emoji_dict = {"anger":"😠","disgust":"🤮", "fear":"😨😱", "happy":"🤗", "joy":"😂", "neutral":"😐", "sad":"😔", "sadness":"😔", "shame":"😳", "surprise":"😮"}
from streamlit_option_menu import option_menu

# with st.sidebar:
#     selected = option_menu("Main Menu", ["Home", 'Settings'], 
#         icons=['house', 'gear'], menu_icon="cast", default_index=1)
#     selected

# Main Application
menu = ["Home","About"]
with st.sidebar:	
    choice = option_menu("Menu",menu)
def main():
	st.image('https://i.ibb.co/rsbYCsN/senttext-low-resolution-logo-white-on-black-background.png', width=500)
	
	st.title("SentText")
	# create_page_visited_table()
	# create_emotionclf_table()
	if choice == "Home":
		with st.form(key='emotion_clf_form'):
			raw_text = st.text_area("Type your text here .....")
			submit_text = st.form_submit_button(label='Submit')

		if submit_text:
			
			col1,col2  = st.columns(2)

			# Apply Fxn Here
			prediction = predict_emotions(raw_text)
			probability = get_prediction_proba(raw_text)
			
			#add_prediction_details(raw_text,prediction,np.max(probability),datetime.now())
			with col1:
				st.success("Original Text")
				st.write(raw_text)
				st.success("Prediction Probability")
				#st.write(probability)
				proba_df = pd.DataFrame(probability,columns=pipe_lr.classes_) # converting into the classes data drame
				st.write(proba_df.T) # t is transpose
				proba_df_clean = proba_df.T.reset_index()
				proba_df_clean.columns = ["emotions","probability"]
				
				
			with col2:

				st.success("Prediction")
				#st.write(prediction)
				emoji_icon = emotions_emoji_dict[prediction]
				st.write("PREDICTION   |  {}{}".format(prediction,emoji_icon))
				st.write("CONFIDENCE  |  {}".format(np.max(probability)))
				
				
				fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions',y='probability',color='emotions')
				st.altair_chart(fig,use_container_width=True)
				

				

		
		


	# elif choice == "Monitor":
	# 	add_page_visited_details("Monitor",datetime.now())
	# 	st.subheader("Monitor App")

	# 	with st.beta_expander("Page Metrics"):
	# 		page_visited_details = pd.DataFrame(view_all_page_visited_details(),columns=['Pagename','Time_of_Visit'])
	# 		st.dataframe(page_visited_details)	

	# 		pg_count = page_visited_details['Pagename'].value_counts().rename_axis('Pagename').reset_index(name='Counts')
	# 		c = alt.Chart(pg_count).mark_bar().encode(x='Pagename',y='Counts',color='Pagename')
	# 		st.altair_chart(c,use_container_width=True)	

	# 		p = px.pie(pg_count,values='Counts',names='Pagename')
	# 		st.plotly_chart(p,use_container_width=True)

	# 	with st.beta_expander('Emotion Classifier Metrics'):
	# 		df_emotions = pd.DataFrame(view_all_prediction_details(),columns=['Rawtext','Prediction','Probability','Time_of_Visit'])
	# 		st.dataframe(df_emotions)

	# 		prediction_count = df_emotions['Prediction'].value_counts().rename_axis('Prediction').reset_index(name='Counts')
	# 		pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction',y='Counts',color='Prediction')
	# 		st.altair_chart(pc,use_container_width=True)	



	else:
	    st.markdown('Sentiment Analysis is the most common text classification tool that analyses an incoming message and tells whether the underlying sentiment is positive, negative our neutral. You can input a sentence of your choice and gauge the underlying sentiment by playing with the demo here.')	

    





if __name__ == '__main__':
	main()