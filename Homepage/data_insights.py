import io
import base64
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from django.db.models import Count
from .models import Rating
from .models import UserProfile

def data_insights():
    # Get the count of ratings for each food
    food_rating_counts = Rating.objects.values('food').annotate(count=Count('food')).order_by('-count')

    # Get the names of the top 10 most rated foods
    top_foods = [f['food'] for f in food_rating_counts[:10]]
    print(""+ str(top_foods))
   
    # Create a bar chart of the top 10 most rated foods
    counts = [f['count'] for f in food_rating_counts[:10]]
    plt.bar(top_foods, counts,
        color=['#C0C0C0', '#202020', '#7E909A', '#1C4E80', '#A5D8DD', '#EA6A47', '#48abf1', '#fce3b4'
        , '#F0C0A8', '#ee91ad'])
    plt.title('Top 10 Most Rated Foods')
    plt.xlabel('Food Name')
    plt.ylabel('Number of Ratings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Set the y-axis range
    plt.ylim([0, max(counts) + 1])

    # Save the chart as a PNG image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    most_rated_food_graph = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    buffer.close()

    #################################

    favourite_category_count = UserProfile.objects.values('foodCategory').annotate(count=Count('foodCategory')).order_by('-count')

    top_categories = [fC['foodCategory'] for fC in favourite_category_count[:10]]
    print("" + str(top_categories))



    # Create a bar chart of the top 10 most rated foods
    countsOne = [fC['count'] for fC in favourite_category_count[:10]]
    plt.bar(top_categories, countsOne, 
        color=['#C0C0C0', '#202020', '#7E909A', '#1C4E80', '#A5D8DD', '#EA6A47', '#A5D8DD'])
    plt.title('Top Food Category')
    plt.xlabel('Food Genre')
    plt.ylabel('Number of Users')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()


    # Set the y-axis range
    plt.ylim([0, max(counts) + 1])

    # Save the chart as a PNG image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    favourite_categories_graph = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    buffer.close()

    ################################################
    pref_location_count = UserProfile.objects.values('prefLocation').annotate(count=Count('prefLocation')).order_by('-count')

    pref_location = [PL['prefLocation'] for PL in pref_location_count[:10]]
    print("" + str(pref_location))



    # Create a bar chart of the top 10 most rated foods
    countsPL = [PL['count'] for PL in pref_location_count[:5]]
    plt.pie(countsPL, labels=pref_location, autopct='%1.1f%%')
    plt.title('Preferred Location')
    # plt.xlabel('Food Genre')
    # plt.ylabel('Number of Users')
    # plt.xticks(rotation=45, ha='right')
    # plt.tight_layout()


    # Set the y-axis range
    # plt.ylim([0, max(countsPL) + 1])

    # Save the chart as a PNG image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    pref_location_graph = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    buffer.close()

    return most_rated_food_graph, favourite_categories_graph, pref_location_graph
