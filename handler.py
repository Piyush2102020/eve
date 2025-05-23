import traceback

# Safe Execution Wrapper:
# -----------------------
# This decorator wraps functions to catch any runtime exceptions
# and return them in a structured error JSON. Useful for productionizing
# the assistant by ensuring errors don't crash the app and are handled gracefully.
def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_data = {
                "success":False,
                "error": str(e),
                "function": func.__name__,
                "trace": traceback.format_exc()
            }
            print(f"Error in {func.__name__}: {str(e)}")
            return error_data
    return wrapper




# Output Formatting Helper:
# -------------------------
# Formats the result of any module's execution into a standard JSON structure
# for consistency. Contains keys for `success` (bool) and `data` (result or error message).
def output_json(success,result):
    return {"success":success,"data":result}


# ErrorHandler Class:
# -------------------
# Base class designed to automatically apply the safe_run decorator to 
# all callable methods in any subclass (like Weather, News, etc.). 
# This ensures that all public methods are protected against runtime errors 
# and return standardized error messages if exceptions occur.
class ErrorHandler:
    def __init__(self):
        self._wrap_modules()
    
    def _wrap_modules(self):
        for attr_name in dir(self):
            if attr_name.startswith("__"):
                continue
            attr=getattr(self,attr_name)
            if callable(attr):
                setattr(self,attr_name,safe_run(attr))
