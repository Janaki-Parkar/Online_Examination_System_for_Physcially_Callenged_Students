from database import get_connection

def save_log(student_id, event):

    conn = get_connection()

    cursor = conn.cursor()

    query = """

    INSERT INTO monitoring_log

    (student_id,event_type)

    VALUES(%s,%s)

    """

    cursor.execute(

        query,

        (student_id,event)

    )

    conn.commit()

    cursor.close()

    conn.close()