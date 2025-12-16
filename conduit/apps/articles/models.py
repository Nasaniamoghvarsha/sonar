from django.db import models

from conduit.apps.core.models import TimestampedModel


class ArticleManager(models.Manager):
    def filter_by_params(self, author=None, tag=None, favorited=None):
        queryset = self.get_queryset().select_related('author', 'author__user')

        if author is not None:
            queryset = queryset.filter(author__user__username=author)

        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        if favorited is not None:
            queryset = queryset.filter(
                favorited_by__user__username=favorited
            )

        return queryset


class Article(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    objects = ArticleManager()

    # Every article must have an author. This will answer questions like "Who
    # gets credit for writing this article?" and "Who can edit this article?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Profile` can have
    # many `Article`s.
    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='articles'
    )

    tags = models.ManyToManyField(
        'articles.Tag', related_name='articles'
    )

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    body = models.TextField()

    article = models.ForeignKey(
        'articles.Article', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag