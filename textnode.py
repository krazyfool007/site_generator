class TextNode():
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        
    
    def __eq__(self, value: object) -> bool:
        if self.text == value.text & self.text_type == value.text_type & self.url == value.url:
            return True
        return False
        

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"