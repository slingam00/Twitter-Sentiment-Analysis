import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import datetime
import sys

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'UkcS6bn1lK3wFm9mVBWFSzzTM'
		consumer_secret = 'RDCdfsHwB19Me0zXdc9jZBDBdSrSpbkw49JPlgOKc1b6qQuxbX'
		access_token = '1186082375647846400-0QV4EhbNj9ClCc5XAe9jJkzg7UGJgv'
		access_token_secret = 'yKpT8N1JrHy6ZFMpoXj2DToAOLu0V1z8qXoIrJSUf9SYd'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count=10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:

			# call twitter api to fetch tweets

			fetched_tweets = []
			#date_since = "2019-04-01"
			# startDate = datetime.datetime(2019, 4, 1, 0, 0, 0)
			# endDate = datetime.datetime(2019, 5, 1, 0, 0, 0)

			# tmpTweets = self.api.search(q=query, count=count)
			# for tweet in tmpTweets:
			# 	print(tweet)
			# 	if tweet.created_at < endDate and tweet.created_at > startDate:
			# 		fetched_tweets.append(tweet)

			fetched_tweets = self.api.search(q=query, count=count, since = "2019-04-01")

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				print(tweet._json['user']['location'])

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				#parsed_tweet['location'] = tweet.location

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
					else:
						tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def main():
	# creating object of TwitterClient Class
	api = TwitterClient()

	# calling function to get tweets
	candidates = ["Joe Biden",
				  "Pete Buttigieg",
				  "Amy Klobuchar",
				  "Bernie Sanders",
				  "Tom Steyer",
				  "Elizabeth Warren",
				  "Andrew Yang"]

	for i in candidates:
		tweets = api.get_tweets(query=i, count=10000)
	# picking positive tweets from tweets
		print(i)
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
		pos = 100*len(ptweets)/len(tweets)
		print("Positive tweets percentage: {} %".format(pos))
	# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
		neg = 100*len(ntweets)/len(tweets)
		print("Negative tweets percentage: {} %".format(neg))
		print("Postive/Negative Tweet Ratio: " + str(round(pos/neg,3)))
		print("\n")
	# percentage of neutral tweets
		#print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

	# # printing first 5 positive tweets
	# print("\n\nPositive tweets:")
	#
	# for tweet in ptweets[:10]:
	# 	print(tweet['text'])
	#
	# # printing first 5 negative tweets
	# print("\n\nNegative tweets:")
	# for tweet in ntweets[:10]:
	# 	print(tweet['text'])

if __name__ == "__main__":
	# calling main function
	main()
