import tiktoken


class Tokenizer:
    def __init__(self, encoding_name):
        self._encoding_name = encoding_name
        self.encoding = tiktoken.get_encoding(self._encoding_name)

    def encode(self, text):
        tokens = self.encoding.encode(text=text)
        return tokens

    def decode(self, tokens):
        text = self.encoding.decode(tokens)
        return text
