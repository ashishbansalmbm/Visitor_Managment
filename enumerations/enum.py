 #all enums
from enum import Enum


class Designation(Enum):
    AST_PROF = "Assistant Professor"
    ASC_PROF = "Associate Professor"
    PROF = "Professor"
    OT = "Other"


class UserType(Enum):
    SC = "SC"
    SD = "SD"
    SE = "SE"
    SF = "SF"
    SG = "SG"
    SH = "SH"
    SEH = "Section Head"
    DH = "Division Head"
    GH = "Group Head"
    GD = "Group Director"
    DD = "Deputy Director"
    AD = "Associate Director"
    D = "Director"
    S = "Student Intern"

class BloodGroup(Enum):
    OM = "O-Minus"
    OP = "O-Positive"
    AM = "A-Minus"
    AP = "A-Positive"
    BM = "B-Minus"
    ABM = "AB-Minus"
    ABP = "AB-Positive"
    BP = "B-Positive"


class Gender(Enum):
    M = "Male"
    F = "Female"
    OT = "Other"


class Category(Enum):
    GEN = "General"
    OBC = "Other Backward Class"
    SC = "Scheduled Caste"
    ST = "Scheduled Tribe"


class ConditionType(Enum):
    B = "Broken"
    L = "Lost"
    SD = "Service Due"


class DeviceType(Enum):
    L = "Laptop"
    M = "Mobile"
    H = "Hard Disk"
    PD = "Pen Drive"
    C = "Camera"
