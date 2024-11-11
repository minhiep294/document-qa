import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Helper function to display visualization guidance in the sidebar
def display_visualization_guide():
    st.sidebar.header("Directory of Visualizations")
    st.sidebar.markdown("""
    ### 5.1 Amounts
    - **Bar Chart**: Shows values across categories. Can be grouped or stacked.
    - **Dot Plot**: Alternative to bar charts, showing points at end values.
    
    ### 5.2 Distributions
    - **Histogram**: Basic distribution of a numerical variable.
    - **Density Plot**: Smoothed curve of data distribution.
    - **Boxplot**: Summarizes distribution with quartiles and outliers.
    - **Violin Plot**: Combination of boxplot and density plot.
    
    ### 5.3 Proportions
    - **Pie Chart**: Displays parts of a whole.
    - **Stacked Bar Chart**: Shows proportions across multiple categories.
    
    ### 5.4 X–Y Relationships
    - **Scatter Plot**: Shows relationship between two numerical variables.
    - **Line Chart**: Displays trends over time or other ordered data.
    - **Bubble Chart**: Adds a third variable as dot size in scatter plot.
    
    ### 5.5 Uncertainty
    - **Confidence Interval Plot**: Shows range of likely values.
    - **Error Bars**: Represents uncertainty in measurements.
    """)

# Initialize the app and sidebar
st.title("EDA with Streamlit")
st.write("Upload a dataset to explore its variables with various charts.")
display_visualization_guide()

# File upload section
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df.head())

    # Identify numerical and categorical columns
    num_list = []
    cat_list = []
    for column in df:
        if pd.api.types.is_numeric_dtype(df[column]):
            num_list.append(column)
        elif pd.api.types.is_string_dtype(df[column]):
            cat_list.append(column)
    st.write("Numerical Columns:", num_list)
    st.write("Categorical Columns:", cat_list)

    # Define tabs for different analysis types
    tab1, tab2, tab3, tab4 = st.tabs(["Data Cleaning & Descriptive Stats", "Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"])

    with tab1:
        # Data Cleaning
        st.header("1. Data Cleaning")
        st.subheader("Handle Missing Values")
        if st.button("Remove Rows with Missing Data"):
            df.dropna(inplace=True)
            st.write("Rows with missing values removed.")
        
        # Remove Duplicates
        st.subheader("Remove Duplicates")
        if st.button("Remove Duplicate Rows"):
            before = df.shape[0]
            df.drop_duplicates(inplace=True)
            after = df.shape[0]
            st.write(f"Removed {before - after} duplicate rows")

        # Correct Data Types
        st.subheader("Correct Data Types")
        for col in df.columns:
            col_type = st.selectbox(f"Select data type for {col}", ("Automatic", "Integer", "Float", "String", "DateTime"), index=0)
            if col_type == "Integer":
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
            elif col_type == "Float":
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif col_type == "String":
                df[col] = df[col].astype(str)
            elif col_type == "DateTime":
                df[col] = pd.to_datetime(df[col], errors='coerce')
        st.write("Data Cleaning Complete.")
        st.write(df.head())

        # Descriptive Statistics
        st.header("2. Descriptive Statistics")
        st.write(df.describe(include='all'))
        if st.checkbox("Show Mode"):
            st.write(df.mode().iloc[0])
    
    with tab2:
        # Univariate Analysis
        st.header("Univariate Analysis")

        # Numerical Data Visualization
        st.subheader("Numerical Data Visualization")
        num_col = st.selectbox("Select a numerical variable:", num_list)
        if num_col:
            fig, ax = plt.subplots(1, 3, figsize=(18, 5))

            # Histogram
            sns.histplot(df[num_col], kde=True, ax=ax[0])
            ax[0].set_title(f"Histogram of {num_col}")

            # Box Plot
            sns.boxplot(x=df[num_col], ax=ax[1])
            ax[1].set_title(f"Box Plot of {num_col}")

            # Density Plot
            sns.kdeplot(df[num_col], fill=True, ax=ax[2])
            ax[2].set_title(f"Density Plot of {num_col}")

            st.pyplot(fig)

        # Categorical Data Visualization
        st.subheader("Categorical Data Visualization")
        cat_col = st.selectbox("Select a categorical variable:", cat_list)
        if cat_col:
            fig, ax = plt.subplots(1, 3, figsize=(18, 5))

            # Count Plot
            sns.countplot(x=df[cat_col], ax=ax[0])
            ax[0].set_title(f"Count Plot of {cat_col}")

            # Bar Chart
            sns.barplot(x=df[cat_col].value_counts().index, y=df[cat_col].value_counts().values, ax=ax[1])
            ax[1].set_title(f"Bar Chart of {cat_col}")

            # Pie Plot
            df[cat_col].value_counts().plot.pie(ax=ax[2], autopct='%1.1f%%', startangle=90)
            ax[2].set_ylabel('')
            ax[2].set_title(f"Pie Plot of {cat_col}")

            st.pyplot(fig)
    
    with tab3:
        # Bivariate Analysis
        st.header("Bivariate Analysis")

        # Numerical vs. Numerical
        st.subheader("Numerical vs. Numerical")
        num_x = st.selectbox("Select X-axis numerical variable:", num_list, key="biv_num_x")
        num_y = st.selectbox("Select Y-axis numerical variable:", num_list, key="biv_num_y")
        if num_x and num_y:
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[num_x], y=df[num_y], ax=ax)
            ax.set_title(f"Scatter Plot of {num_x} vs {num_y}")
            st.pyplot(fig)

            # Correlation
            corr = df[num_x].corr(df[num_y])
            st.write(f"Correlation between {num_x} and {num_y}: {corr:.2f}")

        # Categorical vs. Numerical
        st.subheader("Categorical vs. Numerical")
        cat_col = st.selectbox("Select a categorical variable:", cat_list, key="biv_cat")
        num_col = st.selectbox("Select a numerical variable:", num_list, key="biv_num")
        if cat_col and num_col:
            fig, ax = plt.subplots()
            sns.barplot(x=cat_col, y=num_col, data=df, ax=ax)
            ax.set_title(f"Bar Plot of {num_col} by {cat_col}")
            st.pyplot(fig)

        # Categorical vs. Categorical
        st.subheader("Categorical vs. Categorical")
        cat_x = st.selectbox("Select X-axis categorical variable:", cat_list, key="biv_cat_x")
        cat_y = st.selectbox("Select Y-axis categorical variable:", cat_list, key="biv_cat_y")
        if cat_x and cat_y:
            fig, ax = plt.subplots()
            sns.countplot(x=cat_x, hue=cat_y, data=df, ax=ax)
            ax.set_title(f"Stacked Bar Chart of {cat_x} by {cat_y}")
            st.pyplot(fig)
    
    with tab4:
        # Multivariate Analysis
        st.header("Multivariate Analysis")

        # Numerical vs. Numerical
        st.subheader("Correlation Matrix for Numerical Variables")
        if num_list:
            corr_matrix = df[num_list].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
            ax.set_title("Correlation Matrix")
            st.pyplot(fig)

        # Pair Plot
        st.subheader("Pair Plot for Numerical Variables")
        if num_list:
            sns.pairplot(df[num_list])
            st.pyplot()

        # Numerical vs. Categorical
        st.subheader("Numerical vs. Categorical with Pair Plot")
        if num_list and cat_list:
            hue_cat = st.selectbox("Select a categorical variable for hue:", cat_list)
            sns.pairplot(df, vars=num_list, hue=hue_cat)
            st.pyplot()
else:
    st.write("Please upload a dataset to begin.")
