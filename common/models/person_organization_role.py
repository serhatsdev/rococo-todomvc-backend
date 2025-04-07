from enum import Enum
from rococo.models import PersonOrganizationRole as BasePersonOrganizationRole

class PersonOrganizationRoleEnum(Enum):
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"

class PersonOrganizationRole(BasePersonOrganizationRole):
    pass
