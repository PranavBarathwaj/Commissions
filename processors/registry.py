# processors/registry.py
import importlib

def get_processor(company, rep_name):
    """Dynamically import and return the appropriate processor"""
    try:
        module_name = f"processors.{company.lower()}_{rep_name.lower()}"
        processor_module = importlib.import_module(module_name)
        return processor_module.process
    except ImportError:
        return None