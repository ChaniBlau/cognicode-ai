import subprocess
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

def execute_code(code: str, language: str = "python"):
    """
    מריץ קוד בתוך סביבה מבודדת ומחזיר את התוצאה או השגיאה.
    """
    # מיפוי סיומות קבצים ופקודות הרצה
    extensions = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts"
    }
    
    suffix = extensions.get(language.lower(), ".txt")
    
    # יצירת קובץ זמני להרצה
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w', encoding='utf-8') as f:
        f.write(code)
        temp_file_path = f.name

    try:
        # פקודת הרצה (כרגע מותאם לפייתון, ניתן להרחיב ל-node וכו')
        if language.lower() == "python":
            cmd = ["python", temp_file_path]
        elif language.lower() == "javascript":
            cmd = ["node", temp_file_path]
        else:
            return {"success": False, "error": f"Language {language} not supported yet."}

        # הרצה ותפיסת הפלט
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5 # מניעת לולאות אינסופיות של המשתמש
        )

        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            # שגיאה בזמן הרצה (Runtime Error)
            return {"success": False, "error": result.stderr or result.stdout}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout: Code execution took too long (limit: 5s)."}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        # מחיקת הקובץ הזמני
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)