from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Round
import re

GENDER = ((1, 'Male'), (0, 'Female'))
AGE = ((0, 'Adult'), (1, 'Child'), (2, 'Teenager'))


class Films(models.Model):
    genre = models.IntegerField(blank=True, null=True)
    hkmdb_id = models.IntegerField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    name_zh = models.TextField(blank=True, null=True)
    visible = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'films'

    def __str__(self):
        return str(self.genre)


class Sentences(models.Model):
    actor_id = models.IntegerField(blank=True, null=True)
    film_id = models.IntegerField(blank=True, null=True)
    media_code = models.IntegerField(blank=True, null=True)
    media_part = models.TextField(blank=True, null=True)
    timestamp_duration_ms = models.IntegerField(blank=True, null=True)
    timestamp_ends_at_ms = models.IntegerField(blank=True, null=True)
    timestamp_starts_at_ms = models.IntegerField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    annotation_auto = models.TextField(blank=True, null=True)
    annotation_string = models.TextField(blank=True, null=True)
    alpha = models.TextField(blank=True, null=True)
    characters_string = models.TextField(blank=True, null=True)
    num_characters = models.IntegerField(blank=True, null=True)
    num_tokens = models.IntegerField(blank=True, null=True)
    orth = models.TextField(blank=True, null=True)
    pron = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    tokens_string = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'sentences'

    def converter_time_start(self):
        m, s = divmod(self.timestamp_starts_at_ms, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    def converter_time_end(self):
        m, s = divmod(self.timestamp_ends_at_ms, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    def real_time_duration(self):
        return self.timestamp_duration_ms

    # def annot_func(self):
    #     # pattern = re.compile("(?P<chienese_char>\w+)_(?P<pron>\w+)_(?P<speech>\w+)")
    #     # match = pattern.fullmatch(self.annotation_string, re.IGNORECASE)
    #     f = re.match("(?P<chienese_char>\w+)_(?P<pron>\w+)_(?P<speech>\w+)", self.annotation_string, re.IGNORECASE)
    #     # context = {
    #     #     'chinese_char': match.group("chienese_char"),
    #     #     'pron': match.group("pron"),
    #     #     'speech': match.group("speech")
    #     # }
    #     return f.groupdict()


class Tokens(models.Model):
    word_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tokens'


class Words(models.Model):
    orth = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    pron = models.TextField(blank=True, null=True)
    alpha = models.TextField(blank=True, null=True)
    freq = models.IntegerField(blank=True, null=True)
    freq_adult = models.IntegerField(blank=True, null=True)
    freq_child = models.IntegerField(blank=True, null=True)
    freq_teenager = models.IntegerField(blank=True, null=True)
    freq_female = models.IntegerField(blank=True, null=True)
    freq_male = models.IntegerField(blank=True, null=True)
    freq_comedy = models.IntegerField(blank=True, null=True)
    freq_crime = models.IntegerField(blank=True, null=True)
    freq_drama = models.IntegerField(blank=True, null=True)
    freq_1943 = models.IntegerField(blank=True, null=True)
    freq_1947 = models.IntegerField(blank=True, null=True)
    freq_1948 = models.IntegerField(blank=True, null=True)
    freq_1950 = models.IntegerField(blank=True, null=True)
    freq_1951 = models.IntegerField(blank=True, null=True)
    freq_1952 = models.IntegerField(blank=True, null=True)
    freq_1953 = models.IntegerField(blank=True, null=True)
    freq_1954 = models.IntegerField(blank=True, null=True)
    freq_1955 = models.IntegerField(blank=True, null=True)
    freq_1956 = models.IntegerField(blank=True, null=True)
    freq_1957 = models.IntegerField(blank=True, null=True)
    freq_1958 = models.IntegerField(blank=True, null=True)
    freq_1959 = models.IntegerField(blank=True, null=True)
    freq_1960 = models.IntegerField(blank=True, null=True)
    freq_1961 = models.IntegerField(blank=True, null=True)
    freq_1962 = models.IntegerField(blank=True, null=True)
    freq_1963 = models.IntegerField(blank=True, null=True)
    freq_1964 = models.IntegerField(blank=True, null=True)
    freq_1965 = models.IntegerField(blank=True, null=True)
    freq_1966 = models.IntegerField(blank=True, null=True)
    freq_1967 = models.IntegerField(blank=True, null=True)
    freq_1968 = models.IntegerField(blank=True, null=True)
    freq_1969 = models.IntegerField(blank=True, null=True)
    freq_1970 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'words'

    def __str__(self):
        return str(self.id)

    @classmethod
    def sum_freq(cls):
        return cls.objects.exclude(tag='Pu').aggregate(
            summation=Sum('freq')
        )['summation']

    # @classmethod
    # def percent_n(cls):
    #     summation = cls.sum_freq()
    #     percent_list = []
    #     words = cls.objects.all().exclude(tag='Pu')
    #     for word in words:
    #         calc = round((word.freq / summation) * 100, 2)
    #         percent_list.append(calc)
    #         print(cls.objects.exclude(tag='Pu').values_list(
    #              Round(F('freq') / summation * 100),
    #              flat=True
    #         ))
    #     return cls.objects.exclude(tag='Pu').aggregate(
    #              r=Round(F('freq') / summation * 100)
    #         )['r']

    @classmethod
    def percent_n(cls):
        calc = 0
        summation = cls.sum_freq()
        percent_list = []
        words = cls.objects.all().exclude(tag='Pu')
        print(words)
        for word in words:
            calc = round((word.freq / summation) * 100, 2)
            return calc


    @classmethod
    def rank(cls):
        words = cls.objects.all().exclude(tag='Pu')
        rank = 1
        rank_list = []
        while rank < words.count():
            rank_list.append(rank)
            rank += 1
        return rank_list


class Characters(models.Model):
    freq = models.IntegerField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'characters'


class Actors(models.Model):
    age = models.IntegerField(blank=True, null=True, choices=AGE)
    code = models.TextField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True, choices=GENDER)
    name_en = models.TextField(blank=True, null=True)
    name_zh = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'actors'

    def __str__(self):
        return str(self.age)