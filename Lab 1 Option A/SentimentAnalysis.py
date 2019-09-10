import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id= '993vf_dRP-TY_Q',
                     client_secret= 'c1pMRIto8DoqUQ4VgbXAvOwzOcw',
                     user_agent='my user agent'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

negative_comments_list = []
neutral_comments_list = []
positive_comments_list = []

def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments

#function to process comments whether they are positive negative or neutral
#the variables negative_comments_list, neutral_comments_list, positive_comments_list are initialized through lines 14 to 17

def process_comments(comments, index, i):
    ##if i excceds the length of the total comments will return each list of negative, positive and neutral
    if len(comments) == i:
        return negative_comments_list, neutral_comments_list, positive_comments_list
    ##if index is met or excceded then all the replies of a given
    if len(comments[i].replies) <= index:
        return process_comments(comments, 0, i+1)

    neu = get_text_neutral_proba(comments[i].replies[index].body)
    neg = get_text_negative_proba(comments[i].replies[index].body)
    pos = get_text_positive_proba(comments[i].replies[index].body)

    ####code below compares the values that are taken from get_text functions for positive, negative and neutral
    ####if pos is of highest value stores it in positive_comments_list, if not moves on to negative, and finally neutral.
    if pos > neg and pos > neu:
        positive_comments_list.append(comments[i].replies[index].body)
    elif neg > neu and neg > pos:
        negative_comments_list.append(comments[i].replies[index].body)
    else:
        neutral_comments_list.append(comments[i].replies[index].body)
    return process_comments(comments, index+1, i), process_comments(comments[i].replies, 0, 0)

def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    print(comments[0].body)
    print(comments[0].replies[0].body)

    neg = get_text_negative_proba(comments[0].replies[0].body)
    pos = get_text_positive_proba(comments[0].replies[0].body)
    neu = get_text_neutral_proba(comments[0].replies[0].body)

    print(neg)
    #start of implementation of my code line 39 to 57, 70 to 72
    process_comments(comments, 0, 0)
    print(len(negative_comments_list))
    print(len(neutral_comments_list))
    print(len(positive_comments_list))

main()
