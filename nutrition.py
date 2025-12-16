import streamlit as st
import pandas as pd
import mysql.connector

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(page_title="Nutrition Paradox Dashboard", layout="wide")

st.title("🥗 Nutrition Paradox: Obesity vs Malnutrition")
st.markdown("""
This dashboard presents SQL-based analysis of global obesity and malnutrition
using WHO public health data (2012–2022).
""")

# ---------------------------------------------------
# MySQL Connection
# ---------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0998",
        database="nutrition_db"
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select Section",
    ["Overview", "Obesity Analysis", "Malnutrition Analysis", "Combined Analysis"]
)

# ---------------------------------------------------
# Overview Section
# ---------------------------------------------------
if section == "Overview":
    st.subheader("Project Overview")

    st.markdown("""
    **Domain:** Global Health & Nutrition  
    **Data Source:** WHO Public APIs  
    **Analysis Period:** 2012–2022  

    **Objectives:**
    - Analyze global obesity and malnutrition trends
    - Identify demographic and regional disparities
    - Highlight the nutrition paradox
    """)

# ---------------------------------------------------
# Obesity Analysis
# ---------------------------------------------------
elif section == "Obesity Analysis":
    st.subheader("Obesity Analysis")

    # -------------------------------
    # Q1: Global Obesity Trend
    # -------------------------------
    st.markdown("### Global Average Obesity Trend Over Time")
    q1 = """
    SELECT Year, AVG(Mean_Estimate) AS avg_obesity
    FROM obesity
    GROUP BY Year
    ORDER BY Year;
    """
    df1 = run_query(q1)
    st.line_chart(df1.set_index("Year"))

    with st.expander("Q1 Table: Global average obesity per year"):
        st.dataframe(df1)

    # -------------------------------
    # Q2: Top 5 Countries
    # -------------------------------
    with st.expander("Q2: Top 5 countries with highest obesity"):
        q2 = """
        SELECT Country, AVG(Mean_Estimate) AS avg_obesity
        FROM obesity
        GROUP BY Country
        ORDER BY avg_obesity DESC
        LIMIT 5;
        """
        st.dataframe(run_query(q2))

    # -------------------------------
    # Q3: India Trend
    # -------------------------------
    st.markdown("### Obesity Trend in India")
    q3 = """
    SELECT Year, AVG(Mean_Estimate) AS obesity_trend
    FROM obesity
    WHERE Country = 'India'
    GROUP BY Year
    ORDER BY Year;
    """
    df3 = run_query(q3)
    st.line_chart(df3.set_index("Year"))

    with st.expander("Q3 Table: Obesity trend in India"):
        st.dataframe(df3)

    # -------------------------------
    # Q4: Gender-wise Obesity
    # -------------------------------
    st.markdown("### Average Obesity by Gender")
    q4 = """
    SELECT Gender, AVG(Mean_Estimate) AS avg_obesity
    FROM obesity
    GROUP BY Gender;
    """
    df4 = run_query(q4)
    st.bar_chart(df4.set_index("Gender"))

    with st.expander("Q4 Table: Average obesity by gender"):
        st.dataframe(df4)

    # -------------------------------
    # Q5: Age Group-wise Obesity
    # -------------------------------
    st.markdown("### Average Obesity by Age Group")
    q5 = """
    SELECT Age_Group, AVG(Mean_Estimate) AS avg_obesity
    FROM obesity
    GROUP BY Age_Group;
    """
    df5 = run_query(q5)
    st.bar_chart(df5.set_index("Age_Group"))

    with st.expander("Q5 Table: Average obesity by age group"):
        st.dataframe(df5)

    # -------------------------------
    # Q6: CI Width (Reliability)
    # -------------------------------
    with st.expander("Q6: Top 5 least reliable countries (highest CI width)"):
        q6 = """
        SELECT Country, AVG(CI_Width) AS avg_ci_width
        FROM obesity
        GROUP BY Country
        ORDER BY avg_ci_width DESC
        LIMIT 5;
        """
        st.dataframe(run_query(q6))

    # -------------------------------
    # Q7: Obesity Level Distribution
    # -------------------------------
    with st.expander("Q7: Obesity level distribution"):
        q7 = """
        SELECT obesity_level, COUNT(*) AS count
        FROM obesity
        GROUP BY obesity_level;
        """
        st.dataframe(run_query(q7))

    # -------------------------------
    # Q8: Country Count by Level & Age Group
    # -------------------------------
    with st.expander("Q8: Country count by obesity level and age group"):
        q8 = """
        SELECT obesity_level,
               Age_Group,
               COUNT(DISTINCT Country) AS country_count
        FROM obesity
        GROUP BY obesity_level, Age_Group
        ORDER BY obesity_level;
        """
        st.dataframe(run_query(q8))

    # -------------------------------
    # Q9: Female vs Male Obesity
    # -------------------------------
    with st.expander("Q9: Countries where female obesity exceeds male obesity"):
        q9 = """
        SELECT o1.Country,
               o1.Year,
               o1.Mean_Estimate AS female_obesity,
               o2.Mean_Estimate AS male_obesity
        FROM obesity o1
        JOIN obesity o2
          ON o1.Country = o2.Country
         AND o1.Year = o2.Year
        WHERE o1.Gender = 'Female'
          AND o2.Gender = 'Male'
          AND o1.Mean_Estimate > o2.Mean_Estimate;
        """
        st.dataframe(run_query(q9))

    # -------------------------------
    # Q10: Global Average Obesity (Table)
    # -------------------------------
    with st.expander("Q10: Global average obesity percentage per year (table)"):
        q10 = """
        SELECT Year,
               AVG(Mean_Estimate) AS global_avg_obesity
        FROM obesity
        GROUP BY Year
        ORDER BY Year;
        """
        st.dataframe(run_query(q10))


# ---------------------------------------------------
# Malnutrition Analysis
# ---------------------------------------------------
elif section == "Malnutrition Analysis":
    st.subheader("Malnutrition Analysis")

    # -------------------------------
    # Q1: Global Malnutrition Trend
    # -------------------------------
    st.markdown("### Global Average Malnutrition Trend Over Time")
    q1 = """
    SELECT Year, AVG(Mean_Estimate) AS avg_malnutrition
    FROM malnutrition
    GROUP BY Year
    ORDER BY Year;
    """
    df1 = run_query(q1)
    st.line_chart(df1.set_index("Year"))

    with st.expander("Q1 Table: Global average malnutrition per year"):
        st.dataframe(df1)

    # -------------------------------
    # Q2: Top 5 Countries
    # -------------------------------
    with st.expander("Q2: Top 5 countries with highest malnutrition"):
        q2 = """
        SELECT Country, AVG(Mean_Estimate) AS avg_malnutrition
        FROM malnutrition
        GROUP BY Country
        ORDER BY avg_malnutrition DESC
        LIMIT 5;
        """
        st.dataframe(run_query(q2))

    # -------------------------------
    # Q3: Region-wise Malnutrition
    # -------------------------------
    st.markdown("### Region-wise Average Malnutrition")
    q3 = """
    SELECT Region, AVG(Mean_Estimate) AS avg_malnutrition
    FROM malnutrition
    GROUP BY Region
    ORDER BY avg_malnutrition DESC;
    """
    df3 = run_query(q3)
    st.bar_chart(df3.set_index("Region"))

    with st.expander("Q3 Table: Region-wise malnutrition"):
        st.dataframe(df3)

    # -------------------------------
    # Q4: Gender-wise Malnutrition
    # -------------------------------
    st.markdown("### Average Malnutrition by Gender")
    q4 = """
    SELECT Gender, AVG(Mean_Estimate) AS avg_malnutrition
    FROM malnutrition
    GROUP BY Gender;
    """
    df4 = run_query(q4)
    st.bar_chart(df4.set_index("Gender"))

    with st.expander("Q4 Table: Average malnutrition by gender"):
        st.dataframe(df4)

    # -------------------------------
    # Q5: Age Group-wise Malnutrition
    # -------------------------------
    st.markdown("### Average Malnutrition by Age Group")
    q5 = """
    SELECT Age_Group, AVG(Mean_Estimate) AS avg_malnutrition
    FROM malnutrition
    GROUP BY Age_Group;
    """
    df5 = run_query(q5)
    st.bar_chart(df5.set_index("Age_Group"))

    with st.expander("Q5 Table: Average malnutrition by age group"):
        st.dataframe(df5)

    # -------------------------------
    # Q6: CI Width (Reliability)
    # -------------------------------
    with st.expander("Q6: Top 5 least reliable countries (highest CI width)"):
        q6 = """
        SELECT Country, AVG(CI_Width) AS avg_ci_width
        FROM malnutrition
        GROUP BY Country
        ORDER BY avg_ci_width DESC
        LIMIT 5;
        """
        st.dataframe(run_query(q6))

    # -------------------------------
    # Q7: Malnutrition Level Distribution
    # -------------------------------
    with st.expander("Q7: Malnutrition level distribution"):
        q7 = """
        SELECT malnutrition_level, COUNT(*) AS count
        FROM malnutrition
        GROUP BY malnutrition_level;
        """
        st.dataframe(run_query(q7))

    # -------------------------------
    # Q8: Country Count by Level & Age Group
    # -------------------------------
    with st.expander("Q8: Country count by malnutrition level and age group"):
        q8 = """
        SELECT malnutrition_level,
               Age_Group,
               COUNT(DISTINCT Country) AS country_count
        FROM malnutrition
        GROUP BY malnutrition_level, Age_Group
        ORDER BY malnutrition_level;
        """
        st.dataframe(run_query(q8))

    # -------------------------------
    # Q9: Female vs Male Malnutrition
    # -------------------------------
    with st.expander("Q9: Countries where female malnutrition exceeds male malnutrition"):
        q9 = """
        SELECT m1.Country,
               m1.Year,
               m1.Mean_Estimate AS female_malnutrition,
               m2.Mean_Estimate AS male_malnutrition
        FROM malnutrition m1
        JOIN malnutrition m2
          ON m1.Country = m2.Country
         AND m1.Year = m2.Year
        WHERE m1.Gender = 'Female'
          AND m2.Gender = 'Male'
          AND m1.Mean_Estimate > m2.Mean_Estimate;
        """
        st.dataframe(run_query(q9))

    # -------------------------------
    # Q10: Global Average Malnutrition (Table)
    # -------------------------------
    with st.expander("Q10: Global average malnutrition percentage per year (table)"):
        q10 = """
        SELECT Year,
               AVG(Mean_Estimate) AS global_avg_malnutrition
        FROM malnutrition
        GROUP BY Year
        ORDER BY Year;
        """
        st.dataframe(run_query(q10))


# ---------------------------------------------------
# Combined Analysis
# ---------------------------------------------------
elif section == "Combined Analysis":
    st.subheader("Combined Analysis: Obesity vs Malnutrition")

    # -------------------------------
    # Q1: Global Trend Comparison
    # -------------------------------
    st.markdown("### Global Trend Comparison: Obesity vs Malnutrition")
    q1 = """
    SELECT o.Year,
           AVG(o.Mean_Estimate) AS obesity,
           AVG(m.Mean_Estimate) AS malnutrition
    FROM obesity o
    JOIN malnutrition m
      ON o.Year = m.Year
    GROUP BY o.Year
    ORDER BY o.Year;
    """
    df1 = run_query(q1)
    st.line_chart(df1.set_index("Year"))

    with st.expander("Q1 Table: Global obesity vs malnutrition trend"):
        st.dataframe(df1)

    # -------------------------------
    # Q2: Gender-wise Comparison
    # -------------------------------
    st.markdown("### Gender-wise Comparison")
    q2 = """
    SELECT o.Gender,
           AVG(o.Mean_Estimate) AS obesity,
           AVG(m.Mean_Estimate) AS malnutrition
    FROM obesity o
    JOIN malnutrition m
      ON o.Gender = m.Gender
    GROUP BY o.Gender;
    """
    df2 = run_query(q2)
    st.bar_chart(df2.set_index("Gender"))

    with st.expander("Q2 Table: Gender-wise obesity vs malnutrition"):
        st.dataframe(df2)

    # -------------------------------
    # Q3: Region-wise Comparison
    # -------------------------------
    st.markdown("### Region-wise Comparison")
    q3 = """
    SELECT o.Region,
           AVG(o.Mean_Estimate) AS obesity,
           AVG(m.Mean_Estimate) AS malnutrition
    FROM obesity o
    JOIN malnutrition m
      ON o.Region = m.Region
    GROUP BY o.Region;
    """
    df3 = run_query(q3)
    st.dataframe(df3)

    # -------------------------------
    # Q4: Country-level Comparison (Sample)
    # -------------------------------
    with st.expander("Q4: Country-level obesity vs malnutrition (sample 20)"):
        q4 = """
        SELECT o.Country,
               AVG(o.Mean_Estimate) AS obesity,
               AVG(m.Mean_Estimate) AS malnutrition
        FROM obesity o
        JOIN malnutrition m
          ON o.Country = m.Country
        GROUP BY o.Country
        LIMIT 20;
        """
        st.dataframe(run_query(q4))

    # -------------------------------
    # Q5: High Obesity & High Malnutrition Countries
    # -------------------------------
    with st.expander("Q5: Countries with both high obesity and high malnutrition"):
        q5 = """
        SELECT o.Country,
               AVG(o.Mean_Estimate) AS obesity,
               AVG(m.Mean_Estimate) AS malnutrition
        FROM obesity o
        JOIN malnutrition m
          ON o.Country = m.Country
        GROUP BY o.Country
        HAVING obesity >= 25 AND malnutrition >= 10;
        """
        st.dataframe(run_query(q5))
