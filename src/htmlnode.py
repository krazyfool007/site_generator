class HTMLNode():
    def __init__(self, tag:str = None, value:str = None, children:list = None, props:dict = None) -> None:
        self.tag = tag # a string representing the HTML tag name ("p", "a", "h1" etc)
        self.value = value # a string representing the value of the tag (e.g the text for a title tag or paragraph)
        self.children = children # a list of other HTMLNode objects that are children of this node
        self.props = props # Dict of key-value pairs representing attriubutes of the tags. If it's a link it has the link info.
        pass

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html_string = ""
        for key, value in self.props.items():
            html_string += f" {key}='{value}'"
        return html_string
    
    def __repr__(self) -> str:
        
        return f"HTMLNode \nTag: {self.tag} \nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"
    
    def __eq__(self, value: object) -> bool:
        return (
            self.tag == value.tag
            and self.value == value.value 
            and self.children == value.children 
            and self.props == value.props
            )
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode needs a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}"
    
    def __repr__(self) -> str:
        return f"LeafNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props if self.props else None})"