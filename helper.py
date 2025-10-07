from matplotlib import pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # fetch no of msg
    num_messages = df.shape[0]

    # fetch words
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    #fetch no of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch no of links
    links = []
    for msg in df['message']:
        links.extend(extract.find_urls(msg))

    return num_messages, len(words),num_media_messages,len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / len(df)) * 100, 2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,new_df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stopwords(msg):
        y=[]
        for word in msg:
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=800, height=400 , background_color='white').generate(temp['message'].str.cat(sep=" "))
    temp['message'] = temp['message'].apply(remove_stopwords)
    return wc


def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])

    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_time = df.groupby('only_date').count()['message'].reset_index()

    return daily_time

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap














