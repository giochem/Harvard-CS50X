-- Keep a log of any SQL queries you execute as you solve the mystery.
-- See an overview of the data types provided
SELECT name FROM sqlite_schema
where type = "table";
-- Look for cases to be investigated
select * from crime_scene_reports
where day = 28 and month = 7 and year = 2021 and street = "Humphrey Street";

-- Read witness statements
select * from interviews
where day = 28 and month = 7 and year = 2021 and transcript like "%bakery%";

-- watch the cars go to the bakery
select * from bakery_security_logs
where day = 28 and month = 7 and year = 2021 and hour = 10 and minute > 15 and minute <= 25 and activity = "exit";

-- find the thief's bank account
select account_number from atm_transactions
where day = 28 and month = 7 and year = 2021
and atm_location = "Leggett Street" and transaction_type = "withdraw";

-- find the thief's identifier
select person_id from bank_accounts
where account_number in
(select account_number from atm_transactions
where day = 28 and month = 7 and year = 2021
and atm_location = "Leggett Street" and transaction_type = "withdraw")
group by person_id

-- find the airport the thief departs from
select * from airports where city = "Fiftyville";

-- find the thief's flight number
select id from flights
where origin_airport_id =
(select id from airports where city = "Fiftyville")
and day = 29 and month = 7 and year = 2021
order by hour, minute;

-- find the thief's passport number
select passport_number from passengers
where flight_id in
(select id from flights
where origin_airport_id =
(select id from airports where city = "Fiftyville")
and day = 29 and month = 7 and year = 2021
order by hour, minute
);

-- find phone number
select * from phone_calls
where day = 28 and month = 7 and year = 2021
and duration < 60;


-- thief
select name from people
where id in
(select person_id from bank_accounts
where account_number in
(select account_number from atm_transactions
where day = 28 and month = 7 and year = 2021
and atm_location = "Leggett Street" and transaction_type = "withdraw")
group by person_id)

and phone_number in
(select caller from phone_calls
where day = 28 and month = 7 and year = 2021
and duration < 60)

and passport_number in
(select passport_number from passengers
where flight_id =
(select id from flights
where origin_airport_id =
(select id from airports where city = "Fiftyville")
and day = 29 and month = 7 and year = 2021
order by hour, minute
))

and license_plate in
(select license_plate from bakery_security_logs
where day = 28 and month = 7 and year = 2021 and hour = 10
and minute > 15 and minute <= 25
and activity = "exit");

-- city to
select city from airports
where id =
(select destination_airport_id from flights
where origin_airport_id =
(select id from airports where city = "Fiftyville")
and day = 29 and month = 7 and year = 2021
order by hour, minute);

-- thief's cacomplice
select name from people
where phone_number =
(select receiver from phone_calls
where day = 28 and month = 7 and year = 2021
and duration < 60 and caller =
(select phone_number from people
where id in
(select person_id from bank_accounts
where account_number in
(select account_number from atm_transactions
where day = 28 and month = 7 and year = 2021
and atm_location = "Leggett Street" and transaction_type = "withdraw")
group by person_id)

and phone_number in
(select caller from phone_calls
where day = 28 and month = 7 and year = 2021
and duration < 60)

and passport_number in
(select passport_number from passengers
where flight_id =
(select id from flights
where origin_airport_id =
(select id from airports where city = "Fiftyville")
and day = 29 and month = 7 and year = 2021
order by hour, minute
))

and license_plate in
(select license_plate from bakery_security_logs
where day = 28 and month = 7 and year = 2021 and hour = 10
and minute > 15 and minute <= 25
and activity = "exit")
)
);