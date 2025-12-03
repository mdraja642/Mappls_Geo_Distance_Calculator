import streamlit as st
import pandas as pd
import requests
import urllib3

st.title("Tauheed - Geo Distance Calculator")

uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
        # Load CSV
    df = pd.read_csv(uploaded_file)

    # Access token
    access_token = "sumrzulbpgjlrdefglquolhqatfnelfeoezh"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    results = []

    for _, row in df.iterrows():
        src_lon, src_lat = row["Source Longitude"], row["Source Latitude"]
        dst_lon, dst_lat = row["Destination Longitude"], row["Destination Latitude"]
        
        # Build API URL for each source-destination pair
        url = f"https://route.mappls.com/route/dm/distance_matrix/driving/{src_lon},{src_lat};{dst_lon},{dst_lat}"
        params = {"access_token": access_token}
        
        response = requests.get(url, params=params, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            distances = data.get("results", {}).get("distances", [])
            durations = data.get("results", {}).get("durations", [])
            
            # Since it's one source and one destination, matrix is 1x1
            dist = distances[0][1] if distances else None
            dur = durations[0][1] if durations else None
            
            results.append({
                "Index Attribute": row["Index Attribute"],
                "Source": f"{src_lon},{src_lat}",
                "Destination": f"{dst_lon},{dst_lat}",
                "Distance (km)": dist/1000,
                "Duration (min)": round(dur/60, 2) if dur else None
            })
        else:
            print(f"Error for row {row['Index Attribute']}: {response.status_code} - {response.text}")

    # Convert results to DataFrame
    result_df = pd.DataFrame(results)
    
    st.write("Processed Data Preview:", result_df.head())
    
    # Download button
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Processed CSV", csv, "output.csv", "text/csv")