# This file is used to run the main app
# It imports the app module and runs it in Streamlit

import streamlit as st
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main app
import app 