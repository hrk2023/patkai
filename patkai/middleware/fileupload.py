# WIP
# Prevents File Upload XSS attacks

from fastapi import UploadFile, File, HTTPException

whitelisted_extensions = ["csv","xlsx"]

def file_upload_xss(data: UploadFile = File(...)):

    ext = data.filename.split(".")[-1]

    if ext not in whitelisted_extensions:
        raise HTTPException(status_code=403, detail=f"file extension {ext} is not allowed")
