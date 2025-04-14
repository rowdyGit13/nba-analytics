from django.db import models

class Team(models.Model):
    team_id = models.IntegerField(unique=True)  # API ID
    abbreviation = models.CharField(max_length=3)
    city = models.CharField(max_length=50)
    conference = models.CharField(max_length=10)
    division = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.full_name

class Player(models.Model):
    player_id = models.IntegerField(unique=True)  # API ID
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=10, null=True, blank=True)
    height_feet = models.IntegerField(null=True, blank=True)
    height_inches = models.IntegerField(null=True, blank=True)
    height_total_inches = models.IntegerField(null=True, blank=True)  # For easy sorting
    weight_pounds = models.IntegerField(null=True, blank=True)
    jersey_number = models.CharField(max_length=10, null=True, blank=True)
    college = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    draft_year = models.IntegerField(null=True, blank=True)
    draft_round = models.IntegerField(null=True, blank=True)
    draft_number = models.IntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='players')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def height_display(self) -> str:
        """Returns height in format '6-2'"""
        if self.height_feet is not None and self.height_inches is not None:
            return f"{self.height_feet}-{self.height_inches}"
        return ""

class Game(models.Model):
    game_id = models.IntegerField(unique=True)  # API ID
    date = models.DateField()
    datetime = models.DateTimeField(null=True, blank=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    visitor_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    home_team_score = models.IntegerField()
    visitor_team_score = models.IntegerField()
    season = models.CharField(max_length=9)  # Stores NBA season in YYYY-YYYY format (e.g., '2022-2023')
    status = models.CharField(max_length=20)
    period = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=10, null=True, blank=True)
    postseason = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.visitor_team} @ {self.home_team} ({self.date})"