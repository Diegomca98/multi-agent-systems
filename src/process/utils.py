import pandas as pd
import os
from datetime import datetime
from markdown_pdf import Section
from pathlib import Path
import streamlit as st
from markdown_pdf import MarkdownPdf

def get_endpoint_mapping(agent_list):
    selected_agents_endpoints = {}

    endpoints = {
        "Financial": [
            "income-statement", 
            "cash-flow-statement", 
            "balance-sheet-statement"
        ],
        "Accounting": [
            "cash-flow-statement-growth", 
            "balance-sheet-statement-growth", 
            "income-statement-growth"
        ],
        "Legal" : [
            "profile", 
        ],
        "Risk": [
            "rating", 
            "financial-growth"
        ],
        "Investment" : [
            "stock-price-change", 
            "historical-market-capitalization", 
            "discounted-cash-flow"
        ]
    }

    if agent_list == list(endpoints.keys()):
        return endpoints
    else:
        for agent in agent_list:
            selected_agents_endpoints[agent] = endpoints[agent]
        return selected_agents_endpoints


def show_example_cleaned(data):
    print(data)

def metrics_data(times, token, outputs, executions, summary_crew):
    execution_time = []
    for i in range(len(times)-1):
        execution_time.append(times[i+1] - times[i])

    # DataFrame para métricas
    metrics_data = {
        'agent': executions,
        'execution_time': execution_time,
        'output_agent_tokens': token,
        'total_tokens': summary_crew.usage_metrics.total_tokens,
        'prompt_tokens': summary_crew.usage_metrics.prompt_tokens,
        'completion_tokens': summary_crew.usage_metrics.completion_tokens,
        'timestamp': [datetime.now()] * len(executions),
    }
    
    # DataFrame para outputs
    outputs_data = {
        'agent': executions,
        'output': outputs
    }

    df_metrics = pd.DataFrame(metrics_data)
    df_outputs = pd.DataFrame(outputs_data)

    # Appendear a CSVs existentes
    metrics_file = "aia-lab-mx-finance-multiagent/data/docs/metrics/Metrics.csv"
    outputs_file = "aia-lab-mx-finance-multiagent/data/docs/metrics/Outputs_Agents.csv"

    # Para métricas
    if not os.path.exists(metrics_file):
        df_metrics.to_csv(metrics_file, index=False)
    else:
        df_metrics.to_csv(metrics_file, mode='a', header=False, index=False)

    # Para outputs
    if not os.path.exists(outputs_file):
        df_outputs.to_csv(outputs_file, index=False)
    else:
        df_outputs.to_csv(outputs_file, mode='a', header=False, index=False)

    print(f"\nData appended to:")
    print(f"Metrics: {metrics_file}")
    print(f"Outputs: {outputs_file}")

def generate_and_download_pdf(result):
    if hasattr(result, "task_output") and result.task_output:
        last_task_output = result.task_output[-1]
        if hasattr(last_task_output, "output"):
            markdown_text = last_task_output.output

    file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Crear el objeto PDF
    pdf = MarkdownPdf(toc_level=2)
    section = Section(markdown_text)
    pdf.add_section(section)
    
    temp_pdf_path = "temp_report.pdf"
    pdf.save(temp_pdf_path)

    with open(temp_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    
    st.session_state.pdf_bytes = pdf_bytes
    st.session_state.file_name = file_name
    
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)


def export_to_pdf_form(result):
    if result: 
        with st.form("pdf_export_form"):
            st.write("Haz clic en el botón para generar el PDF.")
            Pdf_file = st.form_submit_button("Generar PDF")
            
            if Pdf_file:
                generate_and_download_pdf(result)  
                st.success("PDF generado correctamente. Haz clic en 'Descargar PDF' para descargarlo.")
