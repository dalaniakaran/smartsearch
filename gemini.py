import streamlit as st
from google import genai
import pandas as pd

client = genai.Client(api_key="AIzaSyAqtI0hK4ByICbUm1T-6N2Dy01pDYtwNxM")
def generate_brand_prompt(brand_list, search_query):
    return f"""
    Given the following brand list: {brand_list} and the search query '{search_query}',
    return the most relevant brand(s) from the list, considering abbreviations, alternate names, and known parent companies.
    Just return a list of names from my list, no additional text.
    """

def generate_competitor_recommendation_prompt(brand_name, competitor):
    return f"""
    Given the brand '{brand_name}' and overall universe '{competitor}',
    return a list of most relevent potential competitors only for the brand from my universe.
    Just return a list of names from my list, no additional text.
    """

def get_relevant_brands(brand_list, search_query):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=generate_brand_prompt(brand_list, search_query)
        # max_tokens=50
    )
    return response.text

def get_competitor_brands(competitor_dataset, search_query):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=generate_brand_prompt(competitor_dataset, search_query),
        # max_tokens=50
    )
    return response.text

def get_competitor_recommendations(brand_name, competitor):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=generate_competitor_recommendation_prompt(brand_name, competitor),
        # max_tokens=50
    )
    return response.text

# # Predefined brand and competitor lists
# brand_list = ["HP", "Dell", "Apple", "Microsoft", "Google", "Asus","Procter & Gamble","ITC","Tata Consulting Services","Burg King","Wolsvagan","Apple Watch","Apple iPhone","Apple US","Bayerische Motoren Werke","Ingvar Kamprad Elmtaryd Agunnaryd","Minnesota Mining and Manufacturing Company","British Petroleum","Bharat Petroleum"]
# competitor_list = ["HP", "Dell", "Apple", "Microsoft", "Google", "Asus", "Samsung", "IBM", "Lenovo", "Acer","Burger King","KFC"]
vizio = pd.read_csv("/Users/karan.dalania/vscode/vizio_list.csv")
samba = pd.read_csv("/Users/karan.dalania/vscode/samba_list.csv")
master_brands = pd.read_csv("/Users/karan.dalania/vscode/master_brands.csv")


vizio_list = vizio['brands'].dropna().tolist()
samba_list = samba['brands'].dropna().tolist()
master_list = master_brands['MasterBrandName'].dropna().tolist()   # Convert column to a list



# Streamlit UI
st.title("Smart Brand & Competitor Search with GenAI")

# Tabs for Brand Selection and Competitor Search
tab1, tab2 = st.tabs(["Brand Selection", "Competitor Search"])

# User inputs brand list
with tab1:
    st.header("Brand Selection")
    search_query = st.text_input("Enter brand search query:")
    if st.button("Search Brand"):
        if search_query:
            results_vizio = get_relevant_brands(vizio_list, search_query)
            results_samba = get_relevant_brands(samba_list, search_query)
            st.write("### Relevant Vizio Brands:")
            st.write(results_vizio if results_vizio else "No relevant matches found.")
            st.write("### Relevant Samba Brands:")
            st.write(results_samba if results_samba else "No relevant matches found.")
        else:
            st.warning("Please enter a search query.")

# Competitor Search Tab
with tab2:
    st.header("Competitor Search")
    search_query_competitor = st.text_input("Enter competitor search query:")
    enable_competitor_recommendation = st.checkbox("Enable competitor recommendations")
    if st.button("Search Competitor"):
        if search_query_competitor:
            competitor_results = get_competitor_brands(master_list, search_query_competitor)
            st.write("### Competitor Brand:")
            st.write(competitor_results if competitor_results else "No competitor found.")
            
            if enable_competitor_recommendation:
                if search_query:
                    competitor_recommendations = get_competitor_recommendations(search_query, master_list)
                    st.write("### Recommended Competitors:")
                    st.write(competitor_recommendations if competitor_recommendations else "No additional competitors found.")
                else:
                    st.warning("Please enter brand name")
        else:
            st.warning("Please enter a search query.")