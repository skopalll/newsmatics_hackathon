#import nltk
import helpers
from keybert import KeyBERT

# Download necessary NLTK resources
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('punkt_tab')

#from rake_nltk import Rake

def generate_keywords_keybert(title: str, text: str, top_n: int = 3):
    """
    Extract keywords using KeyBERT from the combined title and text.
    
    Args:
        title (str): The title of the content.
        text (str): The body text of the content.
        top_n (int): Number of keywords to extract (default is 3).
    
    Returns:
        list: A list of the top extracted keywords.
    """
    # Combine the title and text into one string
    combined_text = f"{title} {text}"
    
    # Initialize KeyBERT model (uses a default BERT model; you can specify another model if desired)
    model = KeyBERT()
    
    # Extract keywords. keyphrase_ngram_range=(1, 2) extracts unigrams and bigrams.
    keywords = model.extract_keywords(combined_text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    
    # The result is a list of tuples: (keyword, score). We only need the keywords.
    return [keyword for keyword, score in keywords]

"""
def generate_keywords(title: str, text: str):
    # Combine title and text
    combined_text = f"{title} {text}"
    
    # Initialize RAKE with default stopwords from NLTK
    rake = Rake()
    
    # Extract keywords from the combined text
    rake.extract_keywords_from_text(combined_text)
    
    # Retrieve the ranked phrases (keywords)
    keywords = rake.get_ranked_phrases()
    
    return keywords
"""

def update_keywords_table():
    topics = helpers.get_topics()
    for id, date, title, text in topics:
        keywords = generate_keywords_keybert(title, text)
        helpers.add_keywords(id, ";".join(keywords))

# Example usage:
if __name__ == "__main__":
    sample_title = "Trump and Zelenskyy's meeting turns into a heated argument"
    sample_text = (
        "In a development that has rattled diplomatic circles, a private meeting between former U.S. President Donald Trump and Ukrainian President Volodymyr Zelenskyy turned unexpectedly contentious last week. What began as a scheduled discussion on economic cooperation and strategic security soon escalated into a verbal clash that left aides from both sides visibly shaken. A Meeting Gone Awry The high-profile encounter was set against a backdrop of longstanding differences between the two leaders. Initially convened to review ongoing U.S.-Ukraine initiatives, the dialogue soon took a sharp turn. Sources close to the event reported that the atmosphere grew tense as Trump questioned the efficacy of Zelenskyy’s domestic and foreign policy strategies. In response, Zelenskyy staunchly defended his administration’s recent reforms and criticized what he described as “unwarranted interference” in Ukraine’s sovereign affairs. One senior diplomatic aide, speaking on condition of anonymity, described the exchange as “one of the most heated discussions weve seen in recent memory. Both leaders were unwavering in their positions, with emotions running high as each laid out their frustrations.” Diverging Perspectives and Political Backdrop The clash comes at a time when U.S.-Ukraine relations remain in a delicate balance. Trump, who has frequently challenged international norms during his tenure, reiterated his skepticism toward multilateral engagements and urged a reassessment of long-standing U.S. commitments overseas. Meanwhile, Zelenskyy, whose presidency has been marked by efforts to secure both economic assistance and political support from Western allies, defended his nation’s policy decisions and the urgency of reforms amid ongoing regional conflicts. Political analysts note that the argument highlights deeper ideological rifts—not just between the two men, but also in the broader context of evolving global alliances. “This isn’t simply about one meeting,” commented a veteran foreign policy expert. “It’s a reflection of contrasting visions for national sovereignty and international cooperation at a time when both the U.S. and Ukraine are grappling with unprecedented internal and external pressures.” Implications for Bilateral Relations Although neither leader has released an official statement detailing the incident, the fallout is already evident in diplomatic circles. Insiders suggest that the discord may complicate forthcoming negotiations on economic aid and security guarantees. Some observers warn that this public display of discord could embolden critics on both sides, potentially undermining confidence in future diplomatic engagements. Despite the tensions, both camps have reiterated their commitment to ongoing projects. An unnamed U.S. administration official stated, “Even amidst disagreement, we recognize the importance of a stable and strategic relationship with Ukraine. We hope that cooler heads will prevail in the coming weeks.” Looking Ahead As the international community watches closely, the incident underscores the complex interplay between personal leadership styles and national policy. With both Trump and Zelenskyy having cultivated fiercely loyal bases, the heated exchange is likely to become a touchstone for critics and supporters alike. The coming days will reveal whether this confrontation marks a turning point in U.S.-Ukraine relations or if it will soon be overshadowed by other pressing global issues. For now, the incident serves as a stark reminder that even at the highest levels of diplomacy, personal dynamics can dramatically influence international relations. Further developments are expected as both sides continue to navigate the turbulent waters of modern geopolitics."
    )
    #keywords = generate_keywords_keybert(sample_title, sample_text)
    #print("Extracted Keywords:", keywords)
    helpers.create_keywords_table()
    update_keywords_table()
    topics = helpers.get_topics()
    print(helpers.get_keyword(topics[0][0]))