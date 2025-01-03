from time import sleep
import streamlit as st
from api import FastAPIClient
import logging

# Initialize API Client
api = FastAPIClient(base_url="http://fastapi_app:8000")  # Update base_url as required

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize session state for navigation and authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "auth_action" not in st.session_state:
    st.session_state.auth_action = "Login"  # Default to "Login"

def logoutFunc():
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.current_page = "login"

def formsubmitted():
    sleep(2)
    st.session_state.submitted = True

# Function to set the current page
def set_page(page):
    st.session_state.current_page = page
    # st.rerun()  # Trigger rerun

def handle_unauthorized():
    st.warning("Session expired. Redirecting to login...")
    st.session_state.authenticated = False
    st.session_state.current_page = "login"
    st.rerun()

# Function to toggle between Login and Register
def toggle_auth_action():
    st.session_state.auth_action = "Register" if st.session_state.auth_action == "Login" else "Login"
    # st.rerun()  # Trigger rerun

# Sidebar Navigation
if st.session_state.authenticated:
    st.sidebar.title("Navigation")
    st.sidebar.button("Leads", on_click=set_page, args=("leads",))
    st.sidebar.button("POCs", on_click=set_page, args=("pocs",))
    st.sidebar.button("Interactions", on_click=set_page, args=("interactions",))
    st.sidebar.button("Performance Metrics", on_click=set_page, args=("performance",))
    st.sidebar.button("Logout", on_click= logoutFunc)

# --------------------------------
# Authentication
# --------------------------------
def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if not username or not password:
            st.error("Username and password cannot be empty.")
        else:
            token = api.login_user(username, password)
            if token:
                st.session_state.authenticated = True
                st.session_state.token = token
                st.session_state.current_page = "leads"
                st.success("Logged in successfully!")
                st.rerun()  # Trigger rerun to show the logged-in page
            else:
                st.error("Invalid credentials")
    st.button("Go to Register", on_click=toggle_auth_action)

def register():
    st.title("Register")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register"):
        if not username or not password:
            st.error("Username and password cannot be empty.")
        else:
            response = api.register_user(username, password)
            if response:
                st.success("User registered successfully!")
                st.info("Go to login to access the system.")
                # st.rerun()  # Redirect to login after successful registration
            else:
                st.error("Registration failed. Username might already be taken.")
    st.button("Go to Login", on_click=toggle_auth_action)

# --------------------------------
# Leads Page
# --------------------------------
def leads_page():
    st.title("Manage Leads")
    action = st.radio("Action", ["View All Leads", "Add Lead", "Update Lead", "Show Leads Requiring Calls Today"])
    if action == "View All Leads":
        leads = api.get_all_leads(token=st.session_state.token)
        if leads is None:
            handle_unauthorized()
        if leads:
            for lead in leads:
                st.subheader(f"{lead['restaurant_name']} (ID: {lead['lead_id']})")
                st.write(f"Status: {lead['status']}")
                st.write(f"Call Frequency: {lead['call_frequency']} days")
                st.write(f"Last Call Date: {lead['last_call_date']}")
                st.write("---")
        else:
            st.warning("No leads found.")
    elif action == "Add Lead":
        last_call_date = None
        restaurant_name = st.text_input("Restaurant Name")
        address = st.text_area("Address")
        status = st.radio("Status", ["New", "Active", "Closed"])
        if status == "Active":
            last_call_date = st.date_input("Last Call Date")
        call_frequency = st.number_input("Call Frequency (days)", min_value=0, step=1)
        if st.button("Add Lead"):
            response = api.create_lead(restaurant_name, address, status, call_frequency, last_call_date, token=st.session_state.token)
            if response is None:
                handle_unauthorized()
            if response:
                st.success("Lead added successfully!")
            else:
                st.error("Failed to add lead!")
    elif action == "Update Lead":
        lead_id = st.number_input("Lead ID", min_value=1, step=1)
        lead = api.get_lead_by_id(lead_id, st.session_state.token)
            
        if lead:
            # Use Streamlit form to handle the inputs and prevent refresh
            with st.form(key="lead_form", enter_to_submit=False):
                # Pre-fill the form with the current lead's details
                restaurant_name = st.text_input("Restaurant Name", value=lead.get("restaurant_name", ""))
                address = st.text_area("Address", value=lead.get("address", ""))
                status = st.selectbox("Status", ["New", "Active", "Closed"], index=["New", "Active", "Closed"].index(lead.get("status", "New")))
                call_frequency = st.number_input("Call Frequency (days)", min_value=0, step=1, value=lead.get("call_frequency", 0))
                last_call_date = st.date_input("Last Call Date", value=lead.get("last_call_date", None))
                # Submit button inside the form
                st.form_submit_button(label="Update", on_click=formsubmitted)
                if 'submitted' in st.session_state:
                    if st.session_state.submitted:
                        response = api.update_lead(
                            lead_id=lead_id,
                            token=st.session_state.token,
                            lead_data={
                                "restaurant_name": restaurant_name,
                                "address": address,
                                "status": status,
                                "call_frequency": call_frequency,
                                "last_call_date": str(last_call_date),
                            },
                        )
                        logger.debug({
                                "restaurant_name": restaurant_name,
                                "address": address,
                                "status": status,
                                "call_frequency": call_frequency,
                                "last_call_date": last_call_date,
                            })
                        logger.debug(f"=========== APP.py ========== {response}")
                        if response:
                            st.success("Lead updated successfully!")
                            st.session_state.submitted = False
                        else:
                            st.error("Failed to update lead.")
                            st.session_state.submitted = False
                else:
                    logger.debug("================================= NOT SET =======================")
        else:
            st.warning("Lead not found.")


    elif action == "Show Leads Requiring Calls Today":
        leads_due = api.get_leads_requiring_calls_today(st.session_state.token)
        if leads_due is None:
            handle_unauthorized()
        if leads_due:
            st.write("Leads Requiring Calls Today:")
            for lead in leads_due:
                st.subheader(f"{lead['restaurant_name']} (ID: {lead['lead_id']})")
                st.write(f"Address: {lead['address']}")
                st.write(f"Status: {lead['status']}")
                st.write(f"Call Frequency: {lead['call_frequency']} days")
                st.write(f"Last Call Date: {lead['last_call_date']}")
                st.write("---")
        else:
            st.warning("No leads require calls today.")

# --------------------------------
# POCs Page
# --------------------------------
def pocs_page():
    st.title("Manage Points of Contact (POCs)")
    action = st.radio("Action", ["View All POCs", "Add POC"])
    if action == "View All POCs":
        lead_id = st.number_input("Lead ID", min_value=1, step=1)
        pocs = api.get_pocs_by_lead(lead_id, token=st.session_state.token)
        if pocs is None:
            handle_unauthorized()
        if pocs:
            for poc in pocs:
                st.subheader(f"{poc['name']} (ID: {poc['poc_id']})")
                st.write(f"Role: {poc['role']}")
                st.write(f"Phone: {poc['phone']}")
                st.write(f"Email: {poc['email']}")
                st.write("---")
        else:
            st.warning("No POCs found.")
    elif action == "Add POC":
        lead_id = st.number_input("Lead ID", min_value=1, step=1)
        name = st.text_input("Name")
        role = st.text_input("Role")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        if st.button("Add POC"):
            response = api.create_poc(lead_id, name, role, phone, email, token=st.session_state.token)
            if response is None:
                handle_unauthorized()
            if response:
                st.success("POC added successfully!")
            else:
                st.error("Failed to add POC!")

# --------------------------------
# Interactions Page
# --------------------------------
def interactions_page():
    st.title("Manage Interactions")
    action = st.radio("Action", ["View All Interactions", "Add Interaction"])
    if action == "View All Interactions":
        lead_id = st.number_input("Lead ID", min_value=1, step=1)
        interactions = api.get_interactions_by_lead(lead_id, token=st.session_state.token)
        if interactions is None:
            handle_unauthorized()
        if interactions:
            for interaction in interactions:
                st.subheader(f"Interaction ID: {interaction['interaction_id']}")
                st.write(f"Date: {interaction['interaction_date']}")
                st.write(f"Details: {interaction['details']}")
                st.write(f"Order Placed: {'Yes' if interaction['order_placed'] else 'No'}")
                st.write("---")
        else:
            st.warning("No interactions found.")
    elif action == "Add Interaction":
        lead_id = st.number_input("Lead ID", min_value=1, step=1)
        interaction_date = st.date_input("Interaction Date")
        details = st.text_area("Details")
        order_placed = st.checkbox("Order Placed")
        if st.button("Add Interaction"):
            response = api.create_interaction(lead_id, interaction_date, details, order_placed, token=st.session_state.token)
            if response is None:
                handle_unauthorized()
            if response:
                st.success("Interaction added successfully!")
            else:
                st.error("Failed to add interaction!")

# --------------------------------
# Performance Metrics Page
# --------------------------------
def performance_page():
    st.title("View Performance Metrics")
    action = st.radio("Action", ["Get Performance Metrics", "Show Well-Performing Accounts", "Show Underperforming Accounts"])
    if action == "Get Performance Metrics":
        lead_id = st.number_input("Lead ID", min_value=1, step=1)
        if st.button("Get Performance Metrics"):
            metrics = api.get_performance_metrics(lead_id, token=st.session_state.token)
            if metrics is None:
                handle_unauthorized()
            if metrics:
                st.write(f"Order Frequency: {metrics['order_frequency']}")
                st.write(f"Last Order Date: {metrics['last_order_date']}")
                st.write(f"Performance Status: {metrics['performance_status']}")
            else:
                st.warning("No performance metrics found.")

    elif action == "Show Well-Performing Accounts":
        well_performing = api.get_well_performing_accounts(st.session_state.token)
        if well_performing:
            st.header("Well-Performing Accounts:")
            for lead in well_performing:
                st.subheader(f"{lead['restaurant_name']} (ID: {lead['lead_id']})")
                st.write(f"Status: {lead['status']}")
                st.write("---")
        else:
            st.warning("No well-performing accounts found.")

    elif action == "Show Underperforming Accounts":
        underperforming = api.get_underperforming_accounts(st.session_state.token)
        logger.debug(f"============= APP.py Underperforming ============= {underperforming}")
        if underperforming:
            st.header("Underperforming Accounts:")
            for lead in underperforming:
                st.subheader(f"{lead['restaurant_name']} (ID: {lead['lead_id']})")
                st.write(f"Status: {lead['status']}")
                st.write("---")
        else:
            st.warning("No underperforming accounts found.")

# --------------------------------
# Page Rendering Logic
# --------------------------------
if not st.session_state.authenticated:
    if st.session_state.auth_action == "Login":
        login()
    else:
        register()
else:
    if st.session_state.current_page == "leads":
        leads_page()
    elif st.session_state.current_page == "pocs":
        pocs_page()
    elif st.session_state.current_page == "interactions":
        interactions_page()
    elif st.session_state.current_page == "performance":
        performance_page()