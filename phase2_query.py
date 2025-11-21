import sys
from pymongo import MongoClient
from datetime import datetime


def main_menu(collection):
  while True:
    print("Welcome to NewsLens: An Interactive Document Store!!!\n")

    print("1. Most Common Words by Media Type\n")
    print("2. Article Count Difference Between News and Blogs\n")
    print("3. Top 5 News Sources by Article Count (2015)\n")
    print("4. 5 Most Recent Articles by Source\n")
    print("5. Exit the Program\n")

    print("Choose from [1-5]\n")

    choice = input("Please enter your explore our features: ")
    if choice =="1":
        most_common_words(collection)

    if choice =="2":
        article_count_difference(collection)

    if choice =="3":
        top_5_news_sources(db)

    if choice =="4":
        most_recent_articles(db)

    if choice =="5":
        break
    
    if choice not in ("1" , "2" , "3" , "4" ,"5"):
        print("Invalid Input !!!")
        print("Please try again")
        continue
    
  return

def most_common_words(collection):
    while True:
        media = input("Please enter media type or press 'q' to return to the main menu: ").strip().lower()

        if media == "q":
            print("Returning to the Main Menu...\n")
            return

        if media not in ("news", "blog"):
            print("Invalid Media Type!!!")
            print("Please try again.")
            continue

        common_words = [
            { "$match": {"media-type": {"$regex": f"^{media}$",  "$options": "i"}}},
            { "$project": {"words": {"$split": ["$content"," "]}}},
            { "$unwind": "$words"},
            { "$project": {"word": {"$toLower": "$words"}}},
            { "$match": { "word": {"$regex": "^[a-z]+$"}}},
            { "$group": {"_id":"$word","count": {"$sum": 1}}},
            { "$sort": { "count": -1 }},
            { "$limit": 5 }                  
            ]
            
        
        words_list = list(collection.aggregate(common_words))
        print("Most Common Words by Media Type: \n")
        

        if not words_list:
            print("No words found.\n")
        else:
            for i, doc in enumerate(words_list, start=1):
                print(f"{i}. {doc['_id']} — {doc['count']}")

        return most_common_words(collection)
            
    
def article_count_difference(collection):
    while True:
        date = input("Please enter a date (e.g., September 1, 2015) or press 'q' to return to the main menu: : ").strip()

        if date == "q":
            print("Returning to the Main Menu...\n")
            return
        
        dt = datetime.strptime(date, "%B %d, %Y")
        d = dt.strftime("%Y-%m-%d")
        
        

        article_count = [
            {"$match" : {"published": {"$regex": f"^{d}"}}},
            {"$project": {"media": {"$toLower": "$media-type"}}},
            {"$group": {"_id": "$media", "count": {"$sum": 1}}}
        ]

        articles = list(collection.aggregate(article_count))
        for doc in articles:
            print(f"{doc['_id']} - {doc['count']}")

       

        
        









        return article_count_difference(collection)

def most_recent_articles(collection):









    return most_recent_articles(collection)

def top_5_news_sources(collection):













    return top_5_news_sources(collection)
  

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Usage: python main.py <database_file>")
        sys.exit()

    port_number = sys.argv[1]
    client = MongoClient(f"mongodb://localhost:{port_number}/")
    db = client["291db"]
    collection = db["articles"]
   
    

    print(f"Successfully connected to port number {port_number} !\n")

    main_menu(collection)

    client.close()  