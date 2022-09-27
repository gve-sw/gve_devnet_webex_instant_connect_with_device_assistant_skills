import os

SKILLS_APP_DIR = "SKILLS_APP_DIR="
SKILLS_PRIVATE_KEY_PATH = "SKILLS_PRIVATE_KEY_PATH="

os.chdir("..")
app_path = os.getcwd()

def write(skill_name):
    os.chdir(app_path + "/skills/" + skill_name)
    f = open(".env", "r")
    l = len(f.readlines())
    f.close()
    f = open(".env", "a")
    if (l < 4):
        f.write("\n")
        f.write(SKILLS_APP_DIR + os.getcwd() + "/" + skill_name + "\n")
        f.write(SKILLS_PRIVATE_KEY_PATH + os.getcwd() + "/id_rsa.pem")
    f.close()

write("creation")
write("notes")
write("scheduler")
write("show")