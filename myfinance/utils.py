from enum import Enum
# from .models import Transaction, Category

# Helper methods

class BuiltinCategories(Enum):
    CAR_AND_TRANSPORTATION = 1
    CAR_INSURANCE = 2
    CAR_PAYMENT = 3
    GAS_AND_CHARGING = 4
    PARKING_AND_FEES = 5
    PUBLIC_AND_OTHER_TRANSPORTATION = 6
    SERVICE_AND_REPAIRS = 7
    BILLS = 20
    PHONE = 21
    INTERNET = 22
    TELEVISION = 23
    UTILITIES = 24
    BUSINESS = 40
    ADVERTISING = 41
    LEGAL = 42
    SUPPLIES_AND_EQUIPMENT = 43
    SHIPPING = 44
    BUSINESS_TAXES = 45
    EDUCATION = 60
    BOOKS = 61
    ONLINE_COURSES = 62
    STUDENT_LOANS = 63
    TUITION = 64
    TUTOR = 65
    ENTERTAINMENT = 80
    GENERAL = 81
    ARTS = 82
    MOVIES_AND_TV_SHOWS = 83
    MUSIC = 84
    MAGAZINES_AND_NEWSPAPERS = 85
    LIVE_ENTERTAINMENT = 86
    FINANCIAL = 120
    CPA_FEES = 121
    FINANCIAL_ADVISOR = 122
    LIFE_INSURANCE = 123
    INVESTING = 124
    SAVINGS = 125
    TAXES = 126
    FOOD = 140
    ALCOHOL = 141
    COFFEE_SHOPS = 142
    FAST_FOOD = 143
    GROCERIES = 144
    RESTAURANTS = 145
    GIVING = 160
    CHARITY = 161
    GIFTS = 162
    HEALTH_AND_WELLNESS = 180
    DENTIST = 181
    DOCTOR = 182
    EYECARE = 183
    GYM = 184
    HEALTH_INSURANCE = 185
    PHARMACY = 186
    SPORTS_AND_RECREATION = 187
    SUPPLEMENTS = 188
    HOME = 200
    FURNITURE_AND_DECOR = 201
    HOME_IMPROVEMENT = 202
    HOME_INSURANCE = 203
    HOME_SUPPLIES = 204
    LAWN_AND_GARDEN = 205
    MORTGAGE_AND_RENT = 206
    HOME_SERVICES = 207
    INCOME = 220
    BONUS = 221
    INTEREST_INCOME = 222
    SELF_EMPLOYMENT_INCOME = 223
    PAYCHECK = 224
    REIMBURSEMENT = 225
    RENTAL_INCOME = 226
    RETURNED_PURCHASES = 227
    KIDS = 240
    ALLOWANCE = 241
    BABY_SUPPLIES = 242
    BABYSITTER_AND_DAYCARE = 243
    CHILD_SUPPORT = 244
    KIDS_ACTIVITIES = 245
    TOYS = 246
    MISCELLANEOUS = 260
    SELF_IMPROVEMENT_AND_CARE = 300
    HAIR_AND_SALON = 301
    COUNSELING_AND_THERAPY = 302
    PERSONAL_DEVELOPMENT = 303
    SPA_AND_MASSAGE = 304
    PETS = 320
    PET_FOOD_AND_SUPPLIES = 321
    PET_GROOMING = 322
    PET_SITTING = 323
    VETERINARY = 324
    SHOPPING = 340
    ELECTRONICS_AND_SOFTWARE = 343
    HOBBIES = 344
    SPORTING_GOODS = 342
    TRANSFER = 360
    CREDIT_CARD_PAYMENT = 361
    TRANSFER_TO_ANOTHER_ACCOUNT = 362
    TRAVEL = 380
    AIRPLANE = 381
    AIRBNB_AND_HOTEL = 382
    MOVING = 383
    RENTAL_CAR_AND_TAXI = 384
    VACATION = 385
    CLOTHING = 387



category_map = {
    "Clothing": BuiltinCategories.CLOTHING,
    "Accessories": BuiltinCategories.CLOTHING,
    "Parking": BuiltinCategories.PARKING_AND_FEES,
    "Wholesale": BuiltinCategories.SHOPPING,
    "Business": BuiltinCategories.BUSINESS,
    "Computers": BuiltinCategories.ELECTRONICS_AND_SOFTWARE,
    "Electronics": BuiltinCategories.ELECTRONICS_AND_SOFTWARE,
    "Food": BuiltinCategories.FOOD,
    "Beverage": BuiltinCategories.FOOD,
    "Beer": BuiltinCategories.ALCOHOL,
    "Wine": BuiltinCategories.ALCOHOL,
    "Spirits": BuiltinCategories.ALCOHOL,
    "Charities": BuiltinCategories.CHARITY,
    "Charity": BuiltinCategories.CHARITY,
    "Non-Profit": BuiltinCategories.CHARITY,
    "Automotive": BuiltinCategories.CAR_AND_TRANSPORTATION,
    "Auto": BuiltinCategories.CAR_AND_TRANSPORTATION,
    "Repair": BuiltinCategories.SERVICE_AND_REPAIRS,
    "Transfer": BuiltinCategories.TRANSFER,
    "Wire": BuiltinCategories.TRANSFER,
    "Payment": BuiltinCategories.CREDIT_CARD_PAYMENT,
    "Credit Card": BuiltinCategories.CREDIT_CARD_PAYMENT,
    "Payroll": BuiltinCategories.CREDIT_CARD_PAYMENT,
    "Shops": BuiltinCategories.SHOPPING,
    "Deposit": BuiltinCategories.INCOME,
    "Veterinarians": BuiltinCategories.VETERINARY,
    "Veterinarian": BuiltinCategories.VETERINARY,
    "Bar": BuiltinCategories.ALCOHOL,
    "Drink": BuiltinCategories.ALCOHOL,
    "Financial": BuiltinCategories.FINANCIAL,
    "Taxes": BuiltinCategories.TAXES,
    "Venmo": BuiltinCategories.TRANSFER,
    "Lodging": BuiltinCategories.AIRBNB_AND_HOTEL,
    "Travel": BuiltinCategories.TRAVEL,
    "Recreation": BuiltinCategories.SPORTS_AND_RECREATION,
    "Arts": BuiltinCategories.ARTS,
    "Entertainment": BuiltinCategories.ENTERTAINMENT,
    "Hotel": BuiltinCategories.AIRBNB_AND_HOTEL,
    "Hotels": BuiltinCategories.AIRBNB_AND_HOTEL,
    "Motel": BuiltinCategories.AIRBNB_AND_HOTEL,
    "Motels": BuiltinCategories.AIRBNB_AND_HOTEL,
    "Advertising": BuiltinCategories.ADVERTISING,
    "Marketing": BuiltinCategories.ADVERTISING,
    "Beauty": BuiltinCategories.SELF_IMPROVEMENT_AND_CARE,
    "Furniture": BuiltinCategories.FURNITURE_AND_DECOR,
    "Home": BuiltinCategories.HOME,
    "Decor": BuiltinCategories.FURNITURE_AND_DECOR,
    "Supermarkets": BuiltinCategories.GROCERIES,
    "Groceries": BuiltinCategories.GROCERIES,
    "Debit": BuiltinCategories.TRANSFER,
    "Payment": BuiltinCategories.CREDIT_CARD_PAYMENT,
    "Pets": BuiltinCategories.PETS,
    "Digital Purchase": BuiltinCategories.SHOPPING,
    "Education": BuiltinCategories.EDUCATION,
    "Software": BuiltinCategories.ELECTRONICS_AND_SOFTWARE,
    "Convenience": BuiltinCategories.SHOPPING,
    "Withdrawal": BuiltinCategories.MISCELLANEOUS,
    "Government": BuiltinCategories.TAXES,
    "Agencies": BuiltinCategories.TAXES,
    "Home Improvement": BuiltinCategories.HOME_IMPROVEMENT,
    "Landscaping": BuiltinCategories.HOME_SERVICES,
    "Gas": BuiltinCategories.GAS_AND_CHARGING,
    "Restaurants": BuiltinCategories.RESTAURANTS,
    "Wash": BuiltinCategories.CAR_AND_TRANSPORTATION,
    "Taxi": BuiltinCategories.RENTAL_CAR_AND_TAXI,
    "Pharmacies": BuiltinCategories.PHARMACY,
    "Fast Food": BuiltinCategories.FAST_FOOD,
    "Utilities": BuiltinCategories.UTILITIES,
    "Truck": BuiltinCategories.CAR_AND_TRANSPORTATION,
    "Rentals": BuiltinCategories.RENTAL_CAR_AND_TAXI,
    "Hardware": BuiltinCategories.HOME_IMPROVEMENT,
    "Music": BuiltinCategories.MUSIC,
    "Video": BuiltinCategories.MOVIES_AND_TV_SHOWS,
    "DVD": BuiltinCategories.MOVIES_AND_TV_SHOWS,
    "Telecommunication": BuiltinCategories.PHONE,
    "Tax": BuiltinCategories.TAXES,
    "Security": BuiltinCategories.HOME_SERVICES,
    "Ride Share": BuiltinCategories.RENTAL_CAR_AND_TAXI,
    "Coffee": BuiltinCategories.COFFEE_SHOPS,
    "Coffee Shop": BuiltinCategories.COFFEE_SHOPS,
    "Sporting": BuiltinCategories.SPORTING_GOODS,
    "Credit": BuiltinCategories.TRANSFER,
    "Media": BuiltinCategories.ENTERTAINMENT,
    "Mental": BuiltinCategories.COUNSELING_AND_THERAPY,
    "Healthcare": BuiltinCategories.HEALTH_AND_WELLNESS,
    "Interest": BuiltinCategories.INTEREST_INCOME,
    "Musical": BuiltinCategories.HOBBIES,
    "Instruments": BuiltinCategories.HOBBIES,
    "Subscription": BuiltinCategories.MISCELLANEOUS,
    "Personal": BuiltinCategories.SELF_IMPROVEMENT_AND_CARE,
    "Square": BuiltinCategories.TRANSFER,
    "Dentists": BuiltinCategories.DENTIST,
    "Refund": BuiltinCategories.RETURNED_PURCHASES,
    "Department": BuiltinCategories.SHOPPING,
    "Insurance": BuiltinCategories.HEALTH_INSURANCE,
    "Schools": BuiltinCategories.EDUCATION,
    "Bank Fees": BuiltinCategories.MISCELLANEOUS,
    "PayPal": BuiltinCategories.TRANSFER,
    "Cable": BuiltinCategories.TELEVISION,
    "Bookstores": BuiltinCategories.BOOKS,
    "Shipping": BuiltinCategories.SHIPPING,
    "Gym": BuiltinCategories.GYM,
    "Gyms": BuiltinCategories.GYM,
    "Fitness": BuiltinCategories.HEALTH_AND_WELLNESS,
    "Discount Stores": BuiltinCategories.SHOPPING,
    "Rent": BuiltinCategories.MORTGAGE_AND_RENT,
    "Medical": BuiltinCategories.HEALTH_AND_WELLNESS,
}

def categorize_transactions(transactions):
    for transaction in transactions:
        original_categories = transaction['category']
        new_category = BuiltinCategories.MISCELLANEOUS

        cat_found = False

        if not original_categories:
            transaction['builtin_cat_id'] = int(new_category.value)
            continue
        
        # Order by specificity
        for cat in reversed(original_categories):
            if cat in category_map:
                new_category = category_map[cat]
                break
            else:
                keywords = cat.split()

                for word in keywords:
                    if word in category_map:
                        new_category = category_map[word]
                        cat_found = True
                        break
            
            # To break inner loop for split keywords
            if cat_found:
                break

        transaction['builtin_cat_id'] = int(new_category.value)
