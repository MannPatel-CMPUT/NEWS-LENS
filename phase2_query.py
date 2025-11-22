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
        top_5_news_sources(collection)

    if choice =="4":
        most_recent_articles(collection)

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
            #{ "$limit": 5 }                  
            ]
            
        
        words_list = list(collection.aggregate(common_words))

        print("Most Common Words by Media Type: \n")
        

        if not words_list:
            print("No words found.\n")

        if len(words_list) < 5:
            last_element = words_list[-1]['count']
        
        else:
            last_element = words_list[4]['count']

        top_5_common_words = []

        for doc in words_list:
            if doc['count'] >= last_element:
                top_5_common_words.append(doc)

        for i, doc in enumerate(top_5_common_words, start=1):
            print(f"{i}. {doc['_id']} — {doc['count']}")

        
            
    
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

        if not articles:
            print("No articles were published on this day.\n")
        for doc in articles:
            print(f"{doc['_id']} - {doc['count']}\n")

        news_count = 0
        blog_count = 0

        for doc in articles:
            if doc['_id'] == "news":
                news_count = doc['count']
            
            if doc['_id'] == "blog":
                blog_count = doc['count']
        
        if news_count > blog_count:
            difference_1 = news_count - blog_count
            print("The number of News articled are greater than blog articles by", difference_1)
            
        
        elif blog_count > news_count:
            difference_2 = blog_count - news_count
            print("The number of Blog articles are greater than news articles by", difference_2)
            

        else:
            print("They both have same number of articles!!!")

def most_recent_articles(collection):
            while True:
                source_name = input("Please enter a source or press 'q' to return to the main menu: ").strip().lower()

                if source_name == "q":
                    print("Returning to the Main Menu...\n")
                    return
                
                recent_articles = [
                    {"$match": {"source": {"$regex": f"^{source_name}$", "$options": "i"}}},
                    
                    #{"$limit": 5 },
                    {"$project": {"title": 1,"published":1, "date": {"$substr": ["$published", 0,10 ]}}},
                    {"$sort": { "published": -1 }}
                ]
                articles = list(collection.aggregate(recent_articles))

                print("Top 5 recent article from", source_name)

                if not articles:
                    print("There are no recent articles associated with this source.\n")
                    continue

                if len(articles) < 5:
                    last_element = articles[-1]['published']
                
                else:
                    last_element = articles[4]['published']

                top_5_recent = []

                for doc in articles:
                    if doc['published'] >= last_element:
                        top_5_recent.append(doc)

                 
                for doc in top_5_recent:
                    print(f"{doc['title']} - {doc['date']}\n")

def top_5_news_sources(collection):
    while True:

        sources = [
            {"$match": {"media-type": {"$regex": "^news$", "$options": "i"}, "published": {"$regex": r"^2015"}}},
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            { "$sort": { "count": -1 }},
            #{ "$limit": 5 }
        ]
        
        news_sources = list(collection.aggregate(sources))

        print("\n")
        print("Top 5 News Sources:\n")

        if not news_sources:
            print("No sources were published by news articles in 2015.\n")

        if len(news_sources) < 5:
            last_element = news_sources[-1]['count']

        else:
            last_element = news_sources[4]['count']
    
        top_5_sources = []

        for doc in news_sources:
            if doc['count'] >= last_element:
                top_5_sources.append(doc)

        for doc in top_5_sources:
            print(f"{doc['_id']} - {doc['count']}\n")

        return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Usage: python phase2_query.py {port_number}")
        sys.exit()

    port_number = sys.argv[1]
    client = MongoClient(f"mongodb://localhost:{port_number}/")
    db = client["291db"]
    collection = db["articles"]
   
    

    print(f"Successfully connected to port number {port_number} !\n")

    main_menu(collection)

    client.close()  