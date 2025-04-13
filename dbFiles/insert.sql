INSERT INTO employee_personal_info (employee_id, first_name, last_name, position, phone, address, city, state, country, personal_email) VALUES
('3052', 'Jason', 'Jones', 'CEO', '555-555-5000', '8762 E Kansas St', 'Wichita', 'KS', 'USA', 'moneyspender@email.com'),
('1125', 'Jim', 'Dean', 'Manager', '555-555-5001', '3750 N Main', 'Wichita', 'KS', 'USA', 'partyboy76@email.com'),
('7590', 'Francis', 'Penn', 'Senior Analyst', '555-555-5002', '1168 E Thompson St', 'Wichita', 'KS', 'USA', 'write4fun@email.com'),
('3690', 'John', 'Little', 'Analyst', '555-555-5003', '506 S Atlanta Ave', 'Wichita', 'KS', 'USA', 'loudmusiclover07@email.com'),
('9358', 'Georgia', 'Robins', 'Developer', '555-555-5004', '735 W Hickory', 'Wichita', 'KS', 'USA', 'grobins@email.com');

INSERT INTO badge_info (employee_id, badge_id, activation_date, deactivation_date) VALUES
('3052', '1', '05032025', NULL),
('1125', '2', '05032025', NULL),
('7590', '3', '10032025', NULL),
('3690', '4', '27032025', NULL),
('9358', '5', '05032025', NULL);

INSERT INTO compensation_table (employee_id, salary, bonus, salary_set_date) VALUES
('3052', '120000', '6000', '10032025'),
('1125', '85000', '5000', '10032025'),
('7590', '85000', '3000', '15032025'),
('3690', '70000', '5000', '27032025'),
('9358', '80000', '5000', '10032025');

INSERT INTO badge_sign_in_times (badge_id, date_scanned, time_scanned) VALUES
('1', '10032025', '0800'),
('2', '10032025', '0755'),
('3', '15032025', '0750'),
('3', '15032025', '0751'),
('4', '27032025', '0900');

INSERT INTO employee_company_info (employee_id, company_email, department, manager_emp_id, hire_date, termination_date) VALUES
('3052', 'j.jones@company.com', 'CEO', NULL, '05032025', NULL),
('1125', 'j.dean@company.com', 'Software', '3052', '05032025', NULL),
('7590', 'f.penn@company.com', 'Software', '1125', '10032025', NULL),
('3690', 'j.little@company.com', 'Software', '1125', '27032025', NULL),
('9358', 'g.robins@company.com', 'Development', '1125', '05032025', NULL);

INSERT INTO employee_time_off (employee_id, hours_remaining, hours_consumed, total_annual_hours) VALUES
('3052', '104', '16', '120'),
('1125', '96', '16', '112'),
('7590', '64', '16', '80'),
('3690', '72', '8', '80'),
('9358', '80', '0', '80');