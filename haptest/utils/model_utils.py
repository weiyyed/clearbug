from sweetest.config import web_keywords, common_keywords
def get_keyword_choice():
    keyword_pc=[('',"---")]
    web_keywords.update(common_keywords)
    for k,v in web_keywords.items():
        if not k.isupper():
            keyword_pc.append((v,k))
    return keyword_pc