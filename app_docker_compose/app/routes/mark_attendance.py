import os
import uuid
import logging
import traceback
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from app.models import AttendanceModel, PersonModel
from app.api.mysql import add_attendance_record, get_person_by_id
from app.utils import format_date
from app.routes.recognize_person import recognize_person_file  # Modify to use file-based recognition

router = APIRouter()
logger = logging.getLogger("mark_attendance_router")

@router.post("/mark_attendance")
async def mark_attendance(file: UploadFile = File(...)):
    """
    Marks attendance for a person based on the uploaded face image, after verifying their identity.
    The uploaded file will be compared to existing faces in the database to verify the person.
    """
    response_data = {}
    try:
        # Verify the person using face recognition by file upload
        recognized_person = await recognize_person_file(file)  # Use face recognition with file input
        if not recognized_person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Person not recognized"}
            )

        # Check if the person exists in the database (after verification)
        person = get_person_by_id(recognized_person.id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": f"Person with ID {recognized_person.id} not found"},
            )

        # Create a new attendance record
        timestamp = datetime.utcnow()
        attendance_record = AttendanceModel(
            person_id=recognized_person.id,
            timestamp=timestamp,
        )

        # Save to the database
        add_attendance_record(attendance_record)

        # Prepare the response
        response_data["message"] = "Attendance marked successfully"
        response_data["data"] = {
            "person_id": recognized_person.id,
            "name": recognized_person.name,  # Use recognized person's name
            "timestamp": format_date(timestamp),
        }

    except Exception as excep:
        logger.error("%s: %s", excep, traceback.print_exc())
        response_data["message"] = "Failed to mark attendance"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response_data) from excep

    return response_data
