# External Libraries
import nltk

# Built-in Libraries
import re

# User Libraries
import website_manager as wm
import file_manager as fm


def tokenize(raw_text: str) -> list:
	"""
	Takes raw strings, sterilazes text, uses lemmatization, tokenizes words, and returns tokens in a sorted list.
	"""
	no_space_text = " ".join(raw_text.split())  # Remove extra spaces
	no_punctuation_text = re.sub("[^0-9A-Za-z ]", "", no_space_text)  # Remove punctuation
	pure_text = "".join([i.lower() for i in no_punctuation_text])  #   To lower

	# Tokenize and remove stop words
	tokens = nltk.tokenize.word_tokenize(pure_text)
	stop_words = nltk.corpus.stopwords.words("english")
	tokens = [token for token in tokens if token not in stop_words]

	# Lemmatize and sort
	lemm = nltk.stem.WordNetLemmatizer()
	tokens = [lemm.lemmatize(token) for token in tokens]
	tokens.sort()
	return tokens

def stats()-> None:
	all_links = fm.get("_all_links")
	print("Total of ", len(all_links.keys()), " tags: ", all_links.keys())
	total_urls = 0
	for tag in all_links.keys():
		total_urls = total_urls + len(all_links[tag])
		print("For ", tag, ", there are ", len(all_links[tag]), " urls in data block.")
	print("There are total of ", total_urls, " posts in the data block.")


if "__main__":
	feed_link = "https://hashnode.com/n/"
	tags = [
		# Comment out for safety and sanity while debugging.
		"javascript",
		"python"
	]

	# Links to blog posts (also used in file naming)
	all_links = {}
	data_block = {}
	for tag in tags:
		# Get urls and save them locally
		urls = wm.get_url_list(feed_link + tag)
		fm.save("tag_" + tag + "_links", data= urls)
		
		# Get raw text from each url and process it into tokens
		for url in urls:
			raw = wm.get_text_from_url(url)
			fm.save("raw_" + url, data= raw) # Optional.
			data_block[url] = {
				"tag": tag,
				"tokens": tokenize(raw)
			}
		
		# Update link list
		all_links[tag] = urls

	# Save the list of links and data block
	if len(all_links) > 0 and len(data_block.keys()) > 0:
		fm.save("_all_links", data= all_links)
		fm.save("_data_block", data= data_block)

	
