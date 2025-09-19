# Zambia Budget Analysis App

**Author:** Kampamba Shula  
**Platform:** Python + Streamlit + Plotly  
**Purpose:** Analyze and visualize Zambia’s budget (2007–2025), including revenue, expenditure, fiscal deficit, and government budget constraints.  

---

## Overview

This app provides a **comprehensive analysis of Zambia’s national budget**, allowing policymakers, analysts, and researchers to explore trends in revenue, expenditure, deficit, and funding composition over time. The app is modular, with separate pages for revenue, expenditure, combined analysis, and policy analysis.  

Key insights include:  

- Revenue trends by category (tax, non-tax, grants, and financing)  
- Expenditure trends by major sectors (health, education, defense, social protection, etc.)  
- Fiscal deficit calculations (absolute and as a share of total revenue)  
- Budget constraint visualization showing the relationship between expenditure, domestic revenue, and deficit funding  
- Administration-specific analysis (MMD 2007–2011, PF 2011–2021, UPND 2021–Present)  

---

## Data Sources

1. **Revenue CSV** (`REVENUE.csv`)  
   - Columns: Domestic Revenue, Tax Revenue, Non-Tax Revenue, Grants, Domestic Financing, Foreign Financing, and subcategories (Income Tax, VAT, Company Tax, Mineral Royalties, etc.)  
   - Years: 2007–2025  

2. **Expenditure CSV** (`EXPENDITURE.csv`)  
   - Columns: Major and subcategories of expenditure (General Public Services, Health, Education, Defense, Roads, Farmer Input Support, Strategic Reserves, Debt Service, etc.)  
   - Total Expenditure column included  
   - Years: 2007–2025  

---

## Features

### 1. Revenue Analysis Page

- Trends of Domestic Revenue, Tax Revenue, Non-Tax Revenue  
- Breakdown of tax revenue components (PAYE, Company Tax, VAT, Customs, Excise)  
- Breakdown of non-tax revenue components (Mineral Royalties, Fees, Levies)  
- Grants and financing trends (Domestic, Foreign, Programme & Project Grants)  
- Policy ratios:
  - Tax / Total Revenue (%)  
  - Mineral Royalties / Total Revenue (%)  
  - Grants / Total Revenue (%)  
  - Domestic vs Foreign Financing (%)  

---

### 2. Expenditure Analysis Page

- Trends of Total Expenditure and major sectors over time  
- Sector breakdown charts (stacked charts for major and subcategories)  
- Administration-level insights (MMD, PF, UPND)  
- Spike detection to highlight sudden changes in expenditure  

---

### 3. Combined Revenue & Expenditure Analysis Page

- Revenue vs Expenditure vs Fiscal Deficit line chart  
- Fiscal Deficit (absolute and as % of Domestic Revenue)  
- Administration markers for easy comparison of government priorities  
- Stacked composition charts showing revenue sources funding the deficit  

---

### 4. Policy Analysis Page

- **Government Budget Constraint:** Visualizes how Total Expenditure is funded by Domestic Revenue, Grants, Domestic Borrowing, and Foreign Borrowing  
- Highlights gaps where expenditure exceeds funding  
- Fiscal deficit funding composition (%)  
- Quick policy insights for latest budget year  
- Data download for further analysis  

---

## Installation & Setup

1. **Clone the repository**:

```bash
git clone <repository-url>
cd budget_app