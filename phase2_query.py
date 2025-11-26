from pymongo import MongoClient
from datetime import datetime


def main_menu(collection):
  # Displays the features to the user and asks for valid input.
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
    
    # Handling invalid inputs
    if choice not in ("1" , "2" , "3" , "4" ,"5"):
        print("Invalid Input !!!")
        print("Please try again")
        continue
    
  

def most_common_words(collection):
    while True:
        print("\n")
        media = input("Please enter media type or press 'q' to return to the main menu: ").strip().lower()

        # Returns to menu
        if media == "q":
            print("\n")
            print("Returning to the Main Menu...\n")
            return
        
        # validating correct input
        if media not in ("news", "blog"):
            print("Invalid Media Type!!!")
            print("Please try again.")
            continue

        common_words = [
            { "$match": {"media-type": {"$regex": f"^{media}$",  "$options": "i"}}},
            # Matching media-type with user input
            { "$project": {"words": {"$regexFindAll": {"input":"$content","regex": r"[A-Za-z0-9_-]+"}}}},
            # Extracting all different word along with hyphens and underscores patterns from the content using regex
            # Storing them in 'words' array

            { "$unwind": "$words"},
            # Each matched word becomes a seperate document
            { "$project": {"word": {"$toLower": "$words.match"}}},
            # Converting all matched word to lowercase for even counting
            { "$match": { "word": {"$regex": "^[a-z0-9]+$"}}},
            # Again matching to keep only alphanumeric words
            { "$group": {"_id":"$word","count": {"$sum": 1}}},
            # Grouping by the word and counting them 
            { "$sort": { "count": -1 }}
            # Sorting words by decreasing count
            #{ "$limit": 5 }                  
            ]
            
        
        words_list = list(collection.aggregate(common_words))


        print("\n")
        print("Most Common Words by Media Type: \n")
        

        if not words_list:
            print("No words found.\n")


        # Handle ties at the 5th position
        if len(words_list) < 5:
            last_element = words_list[-1]['count']
        
        else:
            last_element = words_list[4]['count']

        top_5_common_words = []

        for doc in words_list:
            if doc['count'] >= last_element:
                top_5_common_words.append(doc)

        # printing results
        for  doc in top_5_common_words:
            print(f"{doc['_id']} — {doc['count']}\n")

        
            
    
def article_count_difference(collection):
    while True:
        print("")
        date = input("Please enter a date (e.g., September 1, 2015) or press 'q' to return to the main menu: : ").strip()
        print("")

        # Return to menu
        if date == "q":
            print("Returning to the Main Menu...\n")
            return
         
        dt = datetime.strptime(date, "%B %d, %Y")
        d = dt.strftime("%Y-%m-%d")
        
        
        article_count = [
            {"$match" : {"published": {"$regex": f"^{d}"}}},
            # Matching articles whose date starts with YYYY-MM-DD
            {"$project": {"media": {"$toLower": "$media-type"}}},
            # Converting media-type to lowercase and storing it under 'media'
            {"$group": {"_id": "$media", "count": {"$sum": 1}}}
            # Grouping articles by media type and counting them
        ]

        articles = list(collection.aggregate(article_count))

        if not articles:
            print("No articles were published on this day.\n")

        for doc in articles:
            print(f"The number of {doc['_id']} articles are:\n")
            print(f"{doc['_id']} - {doc['count']}\n")

        news_count = 0
        blog_count = 0
        
        #counting media types
        for doc in articles:
            if doc['_id'] == "news":
                news_count = doc['count']
            
            if doc['_id'] == "blog":
                blog_count = doc['count']
                
        # printing results
        if news_count > blog_count:
            difference_1 = news_count - blog_count
            print("The number of News articles are greater than blog articles by", difference_1)
            
        
        elif blog_count > news_count:
            difference_2 = blog_count - news_count
            print("The number of Blog articles are greater than news articles by", difference_2)
            

        else:
            print("They both have same number of articles!!!")

def most_recent_articles(collection):
            while True:
                source_name = input("Please enter a source or press 'q' to return to the main menu: ").strip().lower()
                print("")

                # Return to menu
                if source_name == "q":
                    print("Returning to the Main Menu...\n")
                    return
                
                recent_articles = [
                    {"$match": {"source": {"$regex": f"^{source_name}$", "$options": "i"}}},  
                    # Matching articles with input source name.              
                    #{"$limit": 5 },
                    {"$project": {"title": 1,"published":1, "date": {"$substr": ["$published", 0,10 ]}}},
                    # Keeping title and published.
                    # Extracting first 10 characters of published (YYYY-MM-DD) because the data set is given with time also.
                    {"$sort": { "published": -1 }}
                    # Sorting articles by published timestamp in descending order
                ]
                articles = list(collection.aggregate(recent_articles))

                if not articles:
                    print("There are no recent articles associated with this source.\n")
                    continue

                
                print("Top 5 recent article from", source_name)
                print("")

                # Handle ties at the 5th position
                if len(articles) < 5:
                    last_element = articles[-1]['published']
                
                else:
                    last_element = articles[4]['published']

                top_5_recent = []

                for doc in articles:
                    if doc['published'] >= last_element:
                        top_5_recent.append(doc)

                # printing results
                for doc in top_5_recent:
                    print(f"{doc['title']} - {doc['date']}\n")

def top_5_news_sources(collection):
    while True:

        sources = [
            {"$match": {"media-type": {"$regex": "^news$", "$options": "i"}, "published": {"$regex": r"^2015"}}},
            # Matching where media-type is "news" and published year starts with 2015.
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            # Grouping by news and counting the number of articles per source
            { "$sort": { "count": -1 }},
            # Sorting the counts in descending order
            #{ "$limit": 5 }
        ]
        
        news_sources = list(collection.aggregate(sources))

        print("\n")
        print("Top 5 News Sources:\n")

        if not news_sources:
            print("No sources were published by news articles in 2015.\n")

        
        # Handle ties at the 5th position
        if len(news_sources) < 5:
            last_element = news_sources[-1]['count']

        else:
            last_element = news_sources[4]['count']
    
        top_5_sources = []

        for doc in news_sources:
            if doc['count'] >= last_element:
                top_5_sources.append(doc)

        # printing results
        for doc in top_5_sources:
            print(f"{doc['_id']} - {doc['count']}\n")

        return


if __name__ == "__main__":
    while True:
        print("\n")
        PORT_input= input("Please enter the port number(i.e.- 27017): ").strip()
        
        # Validating port that input are all digits.
        if PORT_input.isdigit():
            port_number = int(PORT_input)
            break

        else:
            print("")
            print("Invalid Input!!! \n")
            print("Please try again")
            continue
    # Connecting to MongoDB server        
    client = MongoClient(f"mongodb://localhost:{port_number}/")
    db = client["291db"]
    collection = db["articles"]

    print("")
    print(f"Successfully connected to port number {port_number} !\n")

    main_menu(collection)

    client.close()  