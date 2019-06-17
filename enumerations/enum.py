 #all enums
from enum import Enum


class Designation(Enum):
    AST_PROF = "Assistant Professor"
    ASC_PROF = "Associate Professor"
    PROF = "Professor"
    OT = "Other"


class UserType(Enum):
    S = "Student"
    F = "Faculty"
    U = "User"
    A = "Alumni"


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

