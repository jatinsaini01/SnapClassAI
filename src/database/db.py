from src.database.congig import supabase
import bcrypt
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#converting password into hash
def hash_pass(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
#checking password
def check_pass(password , database_password):
    return bcrypt.checkpw(password.encode(),database_password.encode())
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
def teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0
def create_teacher(name , username , password):
    data = {
        "name" : name , "username":username , "password":hash_pass(password)
    }
    response = supabase.table("teachers").insert(data).execute()
    return response.data
def teacher_login(username , password):
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response:
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    else:
        return None
#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data
def create_student(new_name , face_embedding=None , voice_embedding=None):
    data = {"name":new_name , "face_embedding":face_embedding , "voice_embedding":voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data
def get_student_subjects(student_id):
    response = supabase.table("subjects_students").select("* , subjects(*)").eq("student_id" , student_id).execute()
    return response.data
def get_student_attendence(student_id):
    response = supabase.table("attendence_logs").select("* , subjects(*)").eq("student_id" , student_id).execute()
    return response.data
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
def create_subject(subject_code , subject_name , subject_section , teacher_id , subject_id):
    data = {"subject_code":subject_code , "name":subject_name , "section":subject_section , "teacher_id":teacher_id , "subject_id":subject_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data
def get_teacher_subjects(teacher_id):
    response=supabase.table("subjects").select("* , subjects_students(count) , attendence_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subjects = response.data
    for subject in subjects:
        subject["total_students"] = subject.get("subjects_students",[{}])[0].get('count',0) if subject.get('subjects_students') else 0
        attendence = subject.get('attendence_logs',[])
        unique_sessions = len(set(log['timestamp'] for log in attendence))
        subject['total_classes'] = unique_sessions
    return subjects
def enroll_student_to_subject(student_id , subject_id):
    data = {"student_id":student_id , "subject_id":subject_id}
    response = supabase.table("subjects_students").insert(data).execute()
    return response.data
def unenroll_student_to_subject(student_id , subject_id):
    data = {"student_id":student_id , "subject_id":subject_id}
    response = supabase.table("subjects_students").delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data
def create_attendence(logs):
    response = supabase.table("attendence_logs").insert(logs).execute()
    return response.data
def get_attendence_for_teacher(teacher_id):
    response = supabase.table("attendence_logs").select("* ,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data
    