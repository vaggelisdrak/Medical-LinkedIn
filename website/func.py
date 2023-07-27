def convert_salary(salary_per,salary):
    if salary_per == "Annum":
        salary = float(float(salary)/12)
    if salary_per == "Day":
        salary = float(float(salary)*22)
    if salary_per == "Hour":
        salary = float(float(salary)*8*22)
    if salary_per == "Month":
        salary = float(float(salary))
    if salary_per == "Week":
        salary = float(float(salary)*3)
    return salary

def unconvert_salary(salary_per,salary):
    if salary_per == "Annum":
        new_salary = float(salary*12)
    if salary_per == "Day":
        new_salary = float(salary/22)
    if salary_per == "Hour":
        new_salary = float(salary/(8*22))
    if salary_per == "Month":
        new_salary = float(salary)
    if salary_per == "Week":
        new_salary = float(salary/3)
    return new_salary
