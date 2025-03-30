/* 
employee_personal_info(first_name, last_name, position, phone, address, city, state, country, employee_id(PK), personal_email);
badge_info(badge id(FK), employee_id (PK));
compensation_table (employee_id (PK), salary, bonus, timestamp);
badge_sign_in_times (badge id(PK), time scanned);
employee_company_info(employee_id (PK), company email, department, manager_emp_id, start date, termination date);
employee_time_off (employee_id (PK), hours remaining, hours taken, total annual hours); 
*/

CREATE TABLE IF NOT EXISTS employee_personal_info(
    first_name
    last_name
    position
    phone
    address
    city
    state
    country
    employee_id(PK)
    personal_email

);

CREATE TABLE IF NOT EXISTS badge_info(

);

CREATE TABLE IF NOT EXISTS compensation_table(

);

CREATE TABLE IF NOT EXISTS badge_sign_in_times(

);

CREATE TABLE IF NOT EXISTS employee_company_info(

);

CREATE TABLE IF NOT EXISTS employee_time_off(

);