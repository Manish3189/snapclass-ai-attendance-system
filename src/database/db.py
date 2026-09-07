from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def check_teacher_exists(username):
    #check for unique username,returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username",username ).execute()
    return len(response.data) > 0 


def create_teacher(username,password,name):
    data = {
            "username": username, 
            "password": hash_pass(password),
            "name": name
        }
    response = supabase.table("teachers").insert(data).execute()
    return response.data 


def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("username",username).execute () # here we are check the username is exits then we check for the password

    if response.data:
        teacher = response.data[0] # we only get 1 response in the form of array 
        if check_pass(password ,teacher['password']):
            return teacher
    return None 



def get_all_students():
    response =  supabase.table("students").select("*").execute()
    return response.data  # we get the data in the form of array 

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {
        'name': new_name,
        'face_embedding': face_embedding,
        'voice_embedding': voice_embedding
    }

    response = supabase.table('students').insert(data).execute()
    return response.data



def create_subject(subject_code, name, section, teacher_id):
    data = { 
            "subject_code" : subject_code,
            "name" : name,
            "section" : section,
            "teacher_id":  teacher_id
        }
        
    

    response = supabase.table('subjects').insert(data).execute()
    return response.data 


def get_teacher_subject(teacher_id):

    response = (
        supabase
        .table("subjects")
        .select("""
            *,
            subject_student(count),
            attendance_logs(timestamp)
        """)
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:

        # Number of students enrolled in this subject
        sub["total_students"] = (
            sub.get("subject_student", [{}])[0].get("count", 0)
        )

        # Attendance records
        attendance = sub.get("attendance_logs", [])

        # Number of unique attendance timestamps
        unique_sessions = len(
            set(
                log["timestamp"]
                for log in attendance
                if log.get("timestamp")
            )
        )

        sub["total_classes"] = unique_sessions

        # Remove nested data because we don't need it anymore
        sub.pop("subject_student", None)
        sub.pop("attendance_logs", None)

    return subjects

def enrolled_student_to_subject(student_id, subject_id) :
    data = {'student_id' : student_id, "subject_id": subject_id}
    response = supabase.table('subject_student').insert(data).execute()
    return response.data

def unenrolled_student_to_subject(student_id, subject_id) :
    response = supabase.table('subject_student').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table('subject_student').select('*, subjects(*)').eq('student_id',student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id',student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data 

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data