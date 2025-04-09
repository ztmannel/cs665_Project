--create a new employee with corresponding rows
INSERT INTO employee_personal_info (employee_id, first_name, last_name, position, phone, address, city, state, country, personal_email) VALUES
('6386', 'Carol', 'Gates', 'Support', '555-555-5005', '5523 Parkridge Cir', 'Wichita', 'KS', 'USA', 'crochet4lyfe@email.com');
INSERT INTO badge_info (employee_id, badge_id, activation_date, deactivation_date) VALUES
('6386', '6', '29032025', 'NULL');
INSERT INTO compensation_table (employee_id, salary, bonus, salary_set_date) VALUES
('6386', '70000', '2000', '29032025');
INSERT INTO badge_sign_in_times (badge_id, date_scanned, time_scanned) VALUES
('6', '30032025', '0830');
INSERT INTO employee_company_info (employee_id, company_email, department, manager_emp_id, hire_date, termination_date) VALUES
('6386', 'c.gates@company.com', 'Support', 'NULL', '29032025', 'NULL');
INSERT INTO employee_time_off (employee_id, hours_remaining, hours_consumed, total_annual_hours) VALUES
('6386', '88', '0', '88');

--show all employees names and their badge swipe times
SELECT first_name, last_name, date_scanned, time_scanned
    FROM employee_personal_info p
    JOIN badge_info b ON p.employee_id = b.employee_id
    JOIN badge_sign_in_times bst ON b.badge_id = bst.badge_id;

--update an employee's salary/bonus
UPDATE compensation_table
    SET salary = 75000
    WHERE employee_id = '3690';

--delete all employee badge sign in for badge_id 5
DELETE FROM badge_sign_in_times WHERE badge_id = '5'