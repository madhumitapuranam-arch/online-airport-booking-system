# main menu
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(host="localhost", user="root",
                               password="PYTHONCOURSE", database="mysql")
mycursor = mydb.cursor()

# Entry menu
def initiate():
    print("WELCOME TO ABUDHABI INTERNATIONAL AIRPORT!\n")
    print("1. Passenger Registration")
    print("2. Flight availability")
    print("3. Book the flight")
    print("4. Cancel booking")
    print("5. Booking payment")
    print("6. Ticket generation")
    print("7. Exit the system")
    while True:
        choice = input("Enter your choice (1/2/3/4/5/6/7): ")
        if choice == "1":
            p_id = int(input("Enter Passenger ID: "))
            f_name = input("Enter first name: ")
            l_name = input("Enter last name: ")
            passport_no = input("Enter passport number: ")
            phone_no = input("Enter phone number: ")
            email = input("Enter email: ")

            passenger(p_id, f_name, l_name, passport_no, phone_no, email)

        elif choice == "2":
            departure = input("Enter departure airport:")
            arrival = input("Enter arrival airport:")

            flight(departure, arrival)


        elif choice == "3":
            p_id = int(input("Enter Passenger ID: "))
            b_id = int(input("Enter booking ID: "))
            f_id = int(input("Enter flight ID: "))
            booking_date = input("Enter booking date: ")
            seat_no = input("Enter seat number: ")

            book(b_id, p_id, f_id, booking_date, seat_no)

        elif choice == "4":
            b_id = int(input("Enter booking ID: "))
            cancel_booking(b_id)

        elif choice == "5":
            pay_id = int(input("Enter payment ID: "))
            b_id = int(input("Enter booking ID: "))
            amount = float(input("Enter amount: "))
            pay_method = input("Enter payment method: ")
            pay_status = input("Enter payment status: ")
            pay_date = input("Enter payment date: ")

            payment(pay_id, b_id, amount, pay_method, pay_status, pay_date)

        elif choice == "6":
            b_id = int(input("Enter booking ID: "))
            p_id = int(input("Enter Passenger ID: "))
            f_id = int(input("Enter flight ID: "))
            booking_date = input("Enter booking date: ")
            seat_no = input("Enter seat number: ")

            generate_ticket(b_id, p_id, f_id, booking_date, seat_no)


        elif choice == "7":
            print("Thank you for using AbuDhabi International Airport!")
            mycursor.close()
            mydb.close()
            break

        else:
            print("Invalid choice! Please try again.")

# Entering passenger data into mysql table
def passenger(p_id, f_name, l_name, passport_no, phone_no, email):
    mycursor.execute(f"INSERT INTO Passenger(passenger_id, first_name, last_name, passport_number, phone_number, email) "
                     f"VALUE ({p_id}, '{f_name}', '{l_name}', '{passport_no}', '{phone_no}', '{email}')")
    mydb.commit()
    print("Passenger registration complete.")

# Search for flight availability
def flight(departure, arrival):
    mycursor.execute(f"SELECT * FROM Flight WHERE departure_airport = '{departure}' AND arrival_airport = '{arrival}'")
    records = mycursor.fetchall()

    if records:
        print(f"Flight from {departure} to {arrival} is available.")
        for row in records:
            print("Flight ID : ", row[0], "From:", row[2], "To:", row[3])
    else:
        print(f"Sorry, flights from {departure} to {arrival} are not available.")

# Book the flight
def book(b_id, p_id, f_id, booking_date, seat_no):
    mycursor.execute(f"INSERT INTO Booking(booking_id, passenger_id, flight_id, booking_date, seat_number) "
                     f"VALUE ({b_id}, {p_id}, {f_id}, '{booking_date}', {seat_no})")
    mydb.commit()
    print("Booking complete.")

# Cancel booking
def cancel_booking(b_id):
    mycursor.execute(f"DELETE FROM Booking WHERE booking_id = {b_id}")
    mydb.commit()

    if mycursor.rowcount == 0:
        print("Booking ID does not exist.")
    else:
        print("Booking successfully cancelled and removed.")

# Booking payment
def payment(pay_id, b_id, amount, pay_method, pay_status, pay_date):
    mycursor.execute(f"INSERT INTO Payment(payment_id, booking_id, amount, payment_method, payment_status, payment_date) "
                     f"VALUES ({pay_id}, {b_id}, {amount}, '{pay_method}', '{pay_status}', '{pay_date}')")
    mydb.commit()
    print("Payment complete.")

# Generate Ticket
def generate_ticket(b_id, p_id, f_id, booking_date, seat_no):
    # Collect passenger name
    mycursor.execute(f"SELECT first_name, last_name FROM Passenger WHERE passenger_id = {p_id} ")
    passenger = mycursor.fetchone()
    passenger_name = f"{passenger[0]} {passenger[1]}"

    # Collect flight details
    mycursor.execute(f"SELECT departure_airport, arrival_airport FROM Flight WHERE flight_id = {f_id} ")
    flight = mycursor.fetchone()
    route = f"{flight[0]} to {flight[1]}"

    ticket_text = f"""
    ---FLIGHT TICKET---
    Booking ID: {b_id}
    Passenger Name: {passenger_name}
    Flight ID: {f_id}
    Route: {route}
    Booking Date: {booking_date}
    Seat Number: {seat_no}

    Thank you for using AbuDhabi International Airport!
    """

    with open("ticket.txt", "w") as file:
        file.write(ticket_text)
    print("Ticket generation complete.")


# Main Program Start
if __name__ == "__main__":
    initiate()








