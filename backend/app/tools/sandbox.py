import subprocess
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def execute_code(code: str, language: str):
    # 1. אתחול משתנים למניעת שגיאות ב-finally
    temp_file_path = None
    exec_path = None
    lang = language.lower()

    # 2. מיפוי הגדרות שפה
    configs = {
        "python": {"ext": ".py", "command": ["python"]},
        "javascript": {"ext": ".js", "command": ["node"]},
        "typescript": {"ext": ".ts", "command": ["ts-node"]},
        "go": {"ext": ".go", "command": ["go", "run"]},
        "nodejs": {"ext": ".js", "command": ["node"]},
        "java": {"ext": ".java", "command": ["java"]}, # דורש Java 11+ להרצה ישירה
        "c++": {"ext": ".cpp", "command": None}, # טיפול מיוחד למטה
        "cpp": {"ext": ".cpp", "command": None}
    }

    config = configs.get(lang)
    if not config:
        return {"success": False, "error": f"Language '{language}' is not supported yet."}

    try:
        # 3. יצירת הקובץ הזמני
        with tempfile.NamedTemporaryFile(suffix=config["ext"], delete=False, mode='w', encoding='utf-8') as f:
            f.write(code)
            temp_file_path = f.name

        # 4. טיפול מיוחד ב-C++ (קומפילציה והרצה)
        if lang in ["c++", "cpp"]:
            exec_path = temp_file_path.replace(".cpp", ".exe") # ב-Windows עדיף .exe
            # בדיקה אם g++ בכלל קיים במערכת
            import shutil
            if not shutil.which("g++"):
                return {"success": False, "error": "C++ Compiler (g++) not found on this system. Please install MinGW."}
                        # הרצה של הקובץ שקומפל
            run_cmd = [exec_path]
        else:
            # הרצה רגילה (Python, JS, Go...)
            run_cmd = config["command"] + [temp_file_path]

        # 5. ביצוע ההרצה בפועל
        result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr or result.stdout}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Execution timed out (10s limit)."}
    except Exception as e:
        return {"success": False, "error": f"Internal Sandbox Error: {str(e)}"}
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if exec_path and os.path.exists(exec_path):
            os.remove(exec_path)