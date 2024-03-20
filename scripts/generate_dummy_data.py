import pandas as pd
import numpy as np
import random

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define lists of first names and last names
first_names = [
    "Aarav", "Aarti", "Abhay", "Aditi", "Akash", "Amit", "Ananya", "Anil", "Anita", "Anjali",
    "Arjun", "Arun", "Ashish", "Ayush", "Bhavna", "Chandan", "Deepak", "Divya", "Gaurav", "Geeta",
    "Hari", "Indira", "Jagdish", "Jyoti", "Kamal", "Kiran", "Kunal", "Lalita", "Manish", "Meera",
    "Mohan", "Neha", "Nikhil", "Nisha", "Pooja", "Prakash", "Priya", "Rahul", "Raj", "Rakesh",
    "Rashmi", "Ravi", "Rohit", "Sandeep", "Sangeeta", "Sanjay", "Sapna", "Shalini", "Shashi", "Shikha",
    "Shiv", "Sneha", "Sonali", "Suresh", "Swati", "Tanvi", "Uma", "Vijay", "Vikas", "Vimal",
    "Vinod", "Yogesh", "Aditya", "Anand", "Avinash", "Bharat", "Chetan", "Dinesh", "Govind", "Hemant", "Ishaan", "Jay",
    "Kartik", "Lakshmi", "Madhav", "Neeraj", "Om", "Pranav", "Raghav", "Sachin", "Tarun", "Utkarsh",
    "Varun", "Yash", "Zubin", "Aditya", "Ananya", "Avinash", "Bhavana", "Chetna", "Deepika", "Gopal",
    "Harsh", "Ishita", "Jaya", "Kavya", "Lalit", "Mukta", "Naveen", "Omkar", "Prateek", "Radha", "Radikha", 
    "Samir", "Tanmay", "Uma", "Vaishali", "Yogita", "Zara", "Abhinav", "Amrita", "Arvind", "Babita", "Chandrakant", 
    "Darshan", "Ekta", "Faisal", "Girish", "Harsha",
    "Ila", "Jatin", "Kamini", "Lavanya", "Mahesh", "Nandini", "Ojas", "Parul", "Rajesh", "Savita",
    "Tanuja", "Urvashi", "Vikram", "Yashwant", "Zoya", "Alok", "Bhakti", "Charan", "Dipika", "Esha",
    "Firoz", "Gautam", "Hansa", "Ishwar", "Juhi", "Kartika", "Lata", "Manisha", "Nakul", "Omprakash",
    "Preeti", "Rajiv", "Seema", "Tara", "Uday", "Vandana", "Yogeshwari", "Zainab"
]
last_names = [
    "Agarwal", "Bansal", "Chopra", "Das", "Gupta", "Jain", "Kumar", "Mehta", "Patel", "Shah",
    "Singh", "Verma", "Sharma", "Bose", "Roy", "Sen", "Dutta", "Mukherjee", "Malhotra", "Nair",
    "Menon", "Pillai", "Rao", "Reddy", "Shetty", "Sinha", "Soni", "Thakur", "Varghese", "Yadav",
    "Chatterjee", "Banerjee", "Bhattacharya", "Srivastava", "Tripathi", "Dubey", "Shukla", "Goswami", "Mishra", "Rajput",
    "Prasad", "Pandey", "Sinha", "Khan", "Saxena", "Ganguly", "Jha", "Chauhan", "Rathore", "Rastogi",
    "Sarin", "Choudhury", "Upadhyay", "Lal", "Sengupta", "Dasgupta", "Barman", "Dey", "Ray", "Datta",
    "Bhattacharjee", "Banerji", "Bhat", "Kulkarni", "Pai", "Desai", "Bakshi", "Nath", "Kapoor", "Shroff",
    "Mirza", "Merchant", "Lobo", "Fernandes", "Biswas", "Mitra", "Chakraborty", "Chopra", "Suri", "Nanda",
    "Bhatia", "Chadha", "Mittal", "Kaul", "Verghese", "Swamy", "Ranganathan", "Raman", "Balakrishnan", "Menon",
    "Iyer", "Pant", "Puri", "Kaul", "Garg", "Gulati", "Sachdev", "Gokhale", "Kadam", "Chavan",
    "Rangan", "Narayan", "Venkatesh", "Naidu", "Subramanian", "Balaji", "Murthy", "Rangarajan", "Krishnan", "Sundaram",
    "Kannan", "Jayaraman", "Shankar", "Nambiar", "Menon", "Venkataraman", "Seshadri", "Natarajan", "Ramakrishnan", "Krishnamurthy",
    "Srinivasan", "Subramaniam", "Govindarajan", "Venkatachalapathy", "Ramachandran", "Narayanan", "Venugopal", "Viswanathan", "Sankaranarayanan"
]

# Define skills
skills = ["router setup", "cable repair", "software troubleshooting", "fiber optics", "customer service"]

def generate_phone_number():
    # Indian phone numbers start with 7, 8, or 9 followed by 9 digits
    first_digit = random.choice(["7", "8", "9"])
    remaining_digits = ''.join(random.choices("0123456789", k=9))
    phone_number = f"+91-{first_digit}{remaining_digits}"
    return phone_number

def generate_location():
    latitude = np.random.uniform(12.957078201607976, 12.991691702207596)
    longitude = np.random.uniform(77.70729957027493, 77.74926821385183)
    return [latitude, longitude]

# Generate synthetic data for technicians
technicians = pd.DataFrame({
    "name": [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(100)],  # Generate random names
    "skill_set": [random.choice(skills) for _ in range(100)],
    "rating": np.round(np.random.uniform(1, 5, size=100), 2),
    "feedback_sentiment": np.random.choice(["positive", "neutral", "negative"], 100),
    "experience_years": np.random.randint(1, 11, size=100),
    "current_location": [generate_location() for _ in range(100)],
    "day_schedule": np.random.choice(["free", "booked"], 100),
    "phoneno" : [generate_phone_number() for _ in range(100)]
})

technicians.to_csv('technicians_data.csv', index=False)
