# SmartStock API Contract

This document defines the API/data contract between the SmartStock backend and other team members.

## Backend Base URL

http://127.0.0.1:8000

---

# 1. Medicines API

## GET /medicines

Returns all medicines.

### Response fields

- medicine_id
- medicine_name
- category
- unit
- unit_price
- criticality

---

# 2. Inventory API

## GET /inventory

Returns inventory information for all medicines.

### Response fields

- medicine_id
- current_stock
- reorder_level
- safety_stock
- expiry_date
- supplier_id
- last_restock_date

---

## GET /inventory/{medicine_id}

Returns inventory information for one medicine.

### Example

GET /inventory/MED001

---

## GET /inventory/low-stock

Returns medicines where:

current_stock <= reorder_level

Useful for low-stock and risk analysis.

---

# 3. Consumption API

## GET /consumption

Returns historical consumption records.

### Response fields

- id
- date
- medicine_id
- quantity_consumed
- demand_type

---

## GET /consumption/{medicine_id}

Returns historical consumption for one medicine.

### Example

GET /consumption/MED001

---

# 4. Supplier APIs

## GET /suppliers

Returns information for all suppliers.

### Response fields

- supplier_id
- supplier_name
- contact_email
- lead_time_days
- reliability_score
- location

---

## GET /suppliers/{supplier_id}

Returns information for one supplier.

### Example

GET /suppliers/SUP001

### Response fields

- supplier_id
- supplier_name
- contact_email
- lead_time_days
- reliability_score
- location

---

# 5. Supplier Data

Supplier information available in the database:

- supplier_id
- supplier_name
- contact_email
- lead_time_days
- reliability_score
- location

The following fields are particularly useful for risk and reorder analysis:

- lead_time_days
- reliability_score

---

# 6. Current Dataset

| Data | Records |
|---|---:|
| Medicines | 40 |
| Suppliers | 8 |
| Inventory | 40 |
| Consumption | 14,600 |

Consumption period:

2025-01-01 to 2025-12-31

---

# 7. Member 2 Usage

Member 2 is responsible for:

Historical Consumption
        ↓
Forecasting
        ↓
Risk Analysis
        ↓
Reorder Recommendation

### Forecasting

Use:

- date
- medicine_id
- quantity_consumed

### Risk Analysis

Use:

- current_stock
- reorder_level
- safety_stock
- lead_time_days
- reliability_score
- forecasted_demand

### Reorder Recommendation

Use:

- current_stock
- forecasted_demand
- safety_stock
- lead_time_days

---

# 8. Important Naming Rules

Use these exact names throughout the project:

- medicine_id
- current_stock
- reorder_level
- safety_stock
- supplier_id
- lead_time_days
- reliability_score
- quantity_consumed
- forecasted_demand

Do not rename these fields without discussing with the team.

---

# 9. API Testing

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

Examples:

GET /consumption/MED001
GET /suppliers/SUP001

---

# 10. Team Branches

member1-backend      → Backend + Database + Inventory
member2-ml           → Forecasting + Risk + Reorder
member3-rag          → RAG + Documents
member4-integration  → MCP + Procurement + Integration
member5-frontend     → Streamlit Frontend

Each member should work on their own branch.

---

# 11. Integration Rule

Do not directly modify another member's branch.

If a new backend API or database field is required, discuss it with Member 1 before changing the shared API contract.