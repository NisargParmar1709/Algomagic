import json
import itertools

def load_json_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path) as f:
        return json.load(f)

def get_user_input(data):
    """Asks the user for input to filter the data."""
    categories_length = len(data['categories'])
    
    print("Available categories:")
    for i, category in enumerate(data['categories']):
        print(f"{i+1}. {category['name']}")

    category_indices = input("Enter category numbers (comma-separated): ").split(',')
    category_indices = [int(index.strip()) - 1 for index in category_indices]

    keywords = input("Enter keywords (comma-separated): ").split(',')
    keywords = [keyword.strip() for keyword in keywords]

    channels = input("Enter favorite channels (comma-separated): ").split(',')
    channels = [channel.strip() for channel in channels]

    content_types_input = input("Enter content types (comma-separated), or press Enter to skip: ")
    if content_types_input:
        content_types = content_types_input.split(',')
        content_types = [content_type.strip() for content_type in content_types]
        content_types_skipped = False
    else:
        content_types = [data['categories'][category_index]['contentType'] for category_index in category_indices]
        content_types_skipped = True
        
    durations_input = input("Enter average video lengths (comma-separated), or press Enter to skip: ")
    if durations_input:
        durations = durations_input.split(',')
        durations = [duration.strip() for duration in durations]
        durations_skipped = False
    else:
        durations = [data['categories'][category_index]['avgVideoLen'] for category_index in category_indices]
        durations_skipped = True

    return category_indices, keywords, channels, content_types, durations, content_types_skipped, durations_skipped

def generate_combinations(data, category_indices, keywords, channels, content_types, durations):
    """Generates all possible combinations based on user input."""
    categories = [data['categories'][category_index]['name'] for category_index in category_indices]
    combinations = list(itertools.product(categories, keywords, channels, content_types, durations))
    return combinations

def print_combinations(combinations, content_types_skipped, durations_skipped):
    """Prints the generated combinations."""
    result_set = set({})
    count = 0
    show_category = input("Do you want to see category in the results? (yes/no): ")
    show_keyword = input("Do you want to see keyword in the results? (yes/no): ")
    show_channel = input("Do you want to see channel in the results? (yes/no): ")
    if content_types_skipped:
        pass
    else:
        show_content_type = input("Do you want to see content type in the results? (yes/no): ")
    if durations_skipped:
        pass
    else:
        show_duration = input("Do you want to see duration in the results? (yes/no): ")

    for combination in combinations:
        category, keyword, channel, content_type, duration = combination
        result_str = ""
        if show_category.lower() == "yes":
            result_str += f"Category: {category}, "
        if show_keyword.lower() == "yes":
            result_str += f"Keyword: {keyword}, "
        if show_channel.lower() == "yes":
            result_str += f"Channel: {channel}, "
        if content_types_skipped:
            pass
        else:
            if show_content_type.lower() == "yes" and not content_types_skipped:
                result_str += f"Content Type: {content_type}, "
        if durations_skipped:
            pass
        else:
            if show_duration.lower() == "yes" and not durations_skipped:
                result_str += f"Duration: {duration}, "

        result_str = result_str.strip().rstrip(',')
        result_set.add(result_str)

    for i in result_set:
        print(i)
        with open('user_youtube_choice', 'a', encoding='utf-8') as f:
            f.write(i)
        count += 1
    print(f"Total combinations: {count}")        

def search_on_youtube():
    """Asks the user what they want to search on YouTube."""
    search_query = input("What do you want to search on YouTube? ")
    return search_query

def main():
    file_path = 'data.json'
    data = load_json_data(file_path)
    category_indices, keywords, channels, content_types, durations, content_types_skipped, durations_skipped = get_user_input(data)
    combinations = generate_combinations(data, category_indices, keywords, channels, content_types, durations)
    print_combinations(combinations, content_types_skipped, durations_skipped)
    search_query = search_on_youtube()
    print(f"Searching for '{search_query}' on YouTube...")

if __name__ == "__main__":
    main()