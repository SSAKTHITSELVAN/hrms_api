
def employee_code_generator(company_code: str, department_code: str, state: int) -> str:
    '''
    Automatic employee code generation
    '''
    employee_code = company_code + department_code + str(state)
    return employee_code


def employee_password_generator(company_code: str, department_code: str, state: int) -> str:
    '''
    Automatic employee password generation
    '''
    employee_password = company_code + department_code + str(state)
    return employee_password
