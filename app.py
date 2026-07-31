
import streamlit as st
import requests

# Set page configuration
st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="wide"
)

# App title and description
st.title("🛒 SuperKart - Sales Prediction")
st.markdown("### Predict product store sales based on product and store attributes")
st.markdown("---")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Product Details")
    
    # Input fields for product data
    Product_Weight = st.number_input(
        "Product Weight (kg)", 
        min_value=0.0, 
        max_value=50.0, 
        value=12.66,
        step=0.01,
        help="Weight of the product in kilograms"
    )
    
    Product_Sugar_Content = st.selectbox(
        "Product Sugar Content",
        options=["Low Sugar", "Regular", "No Sugar"],
        help="Sugar content level of the product"
    )
    
    Product_Allocated_Area = st.number_input(
        "Product Allocated Area (sq ft)",
        min_value=0.0,
        max_value=100.0,
        value=25.0,
        step=0.5,
        help="Shelf space allocated to the product"
    )
    
    Product_MRP = st.number_input(
        "Product MRP (₹)",
        min_value=0.0,
        max_value=5000.0,
        value=150.0,
        step=5.0,
        help="Maximum Retail Price of the product"
    )
    
    Product_Id_char = st.text_input(
        "Product ID",
        value="P001",
        max_chars=10,
        help="Unique product identifier"
    )
    
    Product_Type_Category = st.selectbox(
        "Product Type Category",
        options=["Dairy", "Beverages", "Snacks", "Grocery", "Health", "Household", "Others"],
        help="Category of the product"
    )

with col2:
    st.subheader("🏪 Store Details")
    
    Store_Size = st.select_slider(
        "Store Size",
        options=["Small", "Medium", "Large"],
        value="Medium",
        help="Size category of the store"
    )
    
    Store_Location_City_Type = st.selectbox(
        "Store Location - City Type",
        options=["Tier 1", "Tier 2", "Tier 3"],
        help="City tier classification of the store location"
    )
    
    Store_Type = st.selectbox(
        "Store Type",
        options=["Supermarket", "Hypermarket", "Convenience", "Specialty"],
        help="Type of retail store"
    )
    
    Store_Age_Years = st.number_input(
        "Store Age (years)",
        min_value=0,
        max_value=50,
        value=5,
        step=1,
        help="Age of the store in years"
    )

# Divider
st.markdown("---")

# Prepare data for API call
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# Display input summary
with st.expander("📊 Input Summary", expanded=False):
    st.json(product_data)

# Predict button
if st.button("🔮 Predict Sales", type="primary", use_container_width=True):
    with st.spinner("Making prediction..."):
        try:
            # API endpoint - REPLACE with your deployed endpoint
            # For local testing: http://localhost:8000/predict
            # For Render: https://your-app-name.onrender.com/predict
            # For Hugging Face: https://username-space-name.hf.space/predict
            endpoint = "https://superkart-sales-prediction.onrender.com/predict"
            
            response = requests.post(
                endpoint, 
                json=product_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                predicted_sales = result.get("Sales", 0)
                st.success(f"✅ Predicted Product Store Sales Total: **₹{predicted_sales:,.2f}**")
                
                # Display additional metrics if available
                if "confidence" in result:
                    st.metric("Prediction Confidence", f"{result['confidence']:.1%}")
                    
            else:
                st.error(f"❌ Error in API request. Status code: {response.status_code}")
                st.write("Response:", response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Please make sure the backend server is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px;'>
        SuperKart Sales Predictor v1.0 | Powered by Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
