from src.models import WithTimeBase


class Article(WithTimeBase):
    class Meta:
        table = "blog_article"
