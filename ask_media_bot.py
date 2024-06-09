from datetime import datetime, timedelta
import json
import utils  # Assuming utils.py is in the same directory and contains required functions

def get_comparison(topic, dates):
    # get summaries & links for each stance
    summary_dict, num_dict, links_dict = utils.make_summaries(topic, dates)
    tot_num = sum(num_dict.values())  # total number of news
    # compare stances
    summary_string = '\n'.join([f'[{key}]: {value}' for key, value in summary_dict.items() if num_dict[key] != 0])  # string for openai comparison (only non-empty stances)
    bulk_compare_json = utils.compare_stances(topic, summary_string, dates=dates, full_reply=False)
    bulk_compare_dict = json.loads(bulk_compare_json)  # convert to dict
    # assemble TG post:
    post = []
    # common ground
    post.append(f"**__Общее__** (кол-во новостей: {tot_num}): {bulk_compare_dict['общее']}")
    # differences
    for stance, num_news in num_dict.items():
        if num_news == 0:
            post.append(f"**__{stance}__**: Нет новостей по этой теме")
            continue
        links = ", ".join([f"[{str(i+1)}]({link})" for i, link in enumerate(links_dict[stance][:5])])
        post.append(f"**__{stance}__** ({num_news}, links: {links}): {bulk_compare_dict[stance]}")

    result = '\n\n'.join(post)
    return result

def main():
    # set dates as today and yesterday
    end_date = datetime.now().date()
    start_date = datetime.now().date() - timedelta(days=5)
    dates = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
    # dates = ['2024-05-24', '2024-05-25']
    topic = input("Please enter the topic: ")
    # Call the function with user inputs
    print(get_comparison(topic, dates))
    
if __name__ == "__main__":
    main()
