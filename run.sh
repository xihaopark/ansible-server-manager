#!/bin/bash
source venv/bin/activate
streamlit run app_secure.py --server.port 8501 --server.address 0.0.0.0
