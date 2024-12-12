import logging
import pymysql

logger = logging.getLogger('mysql_api')

def insert_person_data_into_sql(mysql_conn, mysql_tb, person_data: dict, commit: bool = True) -> dict:
    """
    Insert person_data into MySQL table with parameter binding.
    """
    query = (f"INSERT INTO {mysql_tb}" +
             f" {tuple(person_data.keys())}" +
             f" VALUES ({', '.join(['%s'] * len(person_data))})").replace("'", '')
    values = tuple(person_data.values())
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(query, values)
            if commit:
                mysql_conn.commit()
                logger.info("Record inserted into MySQL DB. ✅️")
                return {"status": "success",
                        "message": "Record inserted into MySQL DB"}
            logger.info("Record insertion waiting to be committed to MySQL DB. 🕓")
            return {"status": "success",
                    "message": "Record insertion waiting to be committed to MySQL DB."}
    except pymysql.Error as excep:
        logger.error("%s: MySQL record insert failed ❌", excep)
        return {"status": "failed",
                "message": "MySQL record insertion error"}

def select_person_data_from_sql_with_id(mysql_conn, mysql_tb, person_id: int) -> dict:
    """
    Query MySQL DB to get full person data using the unique person_id.
    """
    query = f"SELECT * FROM {mysql_tb} WHERE id = %s"
    values = person_id
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(query, values)
            person_data = cursor.fetchone()
            if person_data is None:
                logger.warning("MySQL record with ID: %s does not exist ❌.", person_id)
                return {"status": "failed",
                        "message": f"MySQL record with ID: {person_id} does not exist"}
            logger.info("Person with ID: %s retrieved from MySQL DB. ✅️", person_id)
            return {"status": "success",
                    "message": f"Record matching ID: {person_id} retrieved from MySQL DB",
                    "person_data": person_data}
    except pymysql.Error as excep:
        logger.error("%s: MySQL record retrieval failed ❌", excep)
        return {"status": "failed",
                "message": "MySQL record retrieval error"}

def add_attendance_record(mysql_conn, mysql_tb, attendance_data: dict, commit: bool = True) -> dict:
    """
    Add an attendance record to the MySQL table.
    """
    query = (f"INSERT INTO {mysql_tb}" +
             f" (person_id, timestamp)" +
             f" VALUES (%s, %s)").replace("'", '')
    values = (attendance_data["person_id"], attendance_data["timestamp"])
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(query, values)
            if commit:
                mysql_conn.commit()
                logger.info("Attendance record added to MySQL DB. ✅️")
                return {"status": "success",
                        "message": "Attendance record added to MySQL DB"}
            logger.info("Attendance record waiting to be committed to MySQL DB. 🕓")
            return {"status": "success",
                    "message": "Attendance record waiting to be committed to MySQL DB."}
    except pymysql.Error as excep:
        logger.error("%s: MySQL attendance record insertion failed ❌", excep)
        return {"status": "failed",
                "message": "MySQL attendance record insertion error"}

def get_person_by_id(mysql_conn, mysql_tb, person_id: int) -> dict:
    """
    Fetch a person by ID from the MySQL table.
    """
    query = f"SELECT id, name FROM {mysql_tb} WHERE id = %s"
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(query, (person_id,))
            person_data = cursor.fetchone()
            if person_data is None:
                logger.warning("Person with ID: %s not found in MySQL DB ❌.", person_id)
                return {"status": "failed",
                        "message": f"Person with ID: {person_id} not found in MySQL DB"}
            logger.info("Person with ID: %s found in MySQL DB. ✅️", person_id)
            return {"status": "success",
                    "person_data": person_data}
    except pymysql.Error as excep:
        logger.error("%s: Failed to fetch person by ID ❌", excep)
        return {"status": "failed",
                "message": "Failed to fetch person by ID"}

def select_all_person_data_from_sql(mysql_conn, mysql_tb) -> dict:
    """
    Query MySQL DB to get all person data.
    """
    query = f"SELECT * FROM {mysql_tb}"
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(query)
            person_data = cursor.fetchall()
            if person_data is None:
                logger.warning("No MySQL person records were found ❌.")
                return {"status": "failed",
                        "message": "No MySQL person records were found."}
            logger.info("All person records retrieved from MySQL DB. ✅️")
            return {"status": "success",
                    "message": "All person records retrieved from MySQL DB",
                    "person_data": person_data}
    except pymysql.Error as excep:
        logger.error("%s: MySQL record retrieval failed ❌", excep)
        return {"status": "failed",
                "message": "MySQL record retrieval error"}

def delete_person_data_from_sql_with_id(mysql_conn, mysql_tb, person_id: int, commit: bool = True) -> dict:
    """
    Delete record from MySQL DB using the unique person_id.
    """
    select_query = f"SELECT * FROM {mysql_tb} WHERE id = %s"
    del_query = f"DELETE FROM {mysql_tb} WHERE id = %s"
    try:
        with mysql_conn.cursor() as cursor:
            # Check if record exists in DB
            cursor.execute(select_query, (person_id,))
            if not cursor.fetchone():
                logger.error("Person with ID: %s does not exist in MySQL DB. ❌", person_id)
                return {"status": "failed",
                        "message": f"MySQL record with ID: {person_id} does not exist in DB"}

            cursor.execute(del_query, (person_id,))
            if commit:
                mysql_conn.commit()
                logger.info("Person with ID: %s deleted from MySQL DB. ✅️", person_id)
                return {"status": "success",
                        "message": "Record deleted from MySQL DB"}
            logger.info("Record deletion waiting to be committed to MySQL DB. 🕓")
            return {"status": "success",
                    "message": "Record deletion waiting to be committed to MySQL DB."}
    except pymysql.Error as excep:
        logger.error("%s: MySQL record deletion failed ❌", excep)
        return {"status": "failed",
                "message": "MySQL record deletion error"}
