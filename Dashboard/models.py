from django.db import models
from django.contrib.auth.models import AbstractUser


### 1. Security ###
class Security(models.Model):
    type = models.CharField(max_length = 100)
    level = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.type



### 2. Data_repository ###
class DataRepository(models.Model):
    security = models.ForeignKey(Security, on_delete = models.DO_NOTHING) 
    name = models.CharField(max_length= 100)
    data_type = models.CharField(max_length=100)
    size = models.FloatField()
    
    def __str__(self):
        return self.name

    

### 3. Scraper ###
class Scraper(models.Model):
    data_repository = models.ForeignKey(DataRepository, on_delete = models.DO_NOTHING)
    type_source = models.CharField(max_length=100)
    url_source = models.URLField()
    
    def __str__(self):
        return self.type_source



### 4. Plateforme ###
class Plateforme(models.Model):
    scraper = models.ForeignKey(Scraper, on_delete = models.DO_NOTHING)
    name = models.CharField(max_length = 100)
    url = models.URLField()
    
    def __str__(self):
        return self.name


### 5. DataSource ###
class DataSource(models.Model):
    scraper = models.ManyToManyField(Scraper, related_name='Associer')
    type = models.CharField(max_length=100)
    data = models.JSONField()
    
    def __str__(self):
        return self.type

    

### 6. DataParser ###
class DataParser(models.Model):
    data_sources = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='Traiter')
    data = models.JSONField()
    
    def __str__(self):
        return self.data_sources

    

### 7. DataProcessor ###
class DataProcessor(models.Model):
    data_parse = models.JSONField()
    data_parses = models.ManyToManyField(DataParser, related_name='Traiter')
    
    def __str__(self):
        return self.data_parse



### 8. KPI ###
class KPI(models.Model):
    data_processor = models.ForeignKey(DataProcessor, on_delete=models.CASCADE, related_name='Calculer')
    name = models.CharField(max_length=100)
    value = models.FloatField(default=0.0)
    # calculation_logic = models.TextField(help_text="Python code for calculating the KPI")

    # def calculate(self):
    #     local_vars = {'platform': self.platform, 'value': self.value}
    #     exec(self.calculation_logic, {}, local_vars)
    #     self.value = local_vars['value']
    #     self.save()

    def __str__(self):
        return f"{self.name}"


### 9. Utilisateur, Employe et Administrateur ###
class Utilisateur(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_set',  # Nom unique pour éviter les conflits
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='utilisateur'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_set',  # Nom unique pour éviter les conflits
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='utilisateur'
    )


class Employe(Utilisateur):
    def connect(self):
        print(f"{self.username} connected")
        return True

    def disconnect(self):
        print(f"{self.username} disconnected")
        return True

    def consult_dashboard(self):
        print(f"{self.username} consulting dashboard")
        return True


### 10. Notification ###
class Notification(models.Model):
    employe = models.ManyToManyField(Employe, related_name='Consulter')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='Créer')
    title = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    consulted = models.BooleanField(default=False)

    def trigger_alert(self):
        print(f"Triggering alert: {self.title}")
        return True

    def __str__(self):
        return self.title


### 11. Dashboard ###
class Dashboard(models.Model):
    owner = models.ForeignKey('Employe', on_delete=models.CASCADE, related_name='dashboards')
    widgets = models.ManyToManyField('Widget', related_name='dashboards')

    def __str__(self):
        return f"Dashboard for {self.owner.username}"



### 12. Widget ###
class Widget(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.DO_NOTHING)
    kpi = models.ForeignKey(KPI, on_delete = models.CASCADE, related_name='Afficher')
    type = models.CharField(max_length=100)
    data = models.JSONField()
    
    def __str__(self):
        return self.type






