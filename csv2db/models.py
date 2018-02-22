from django.db import models

# Create your models here.
class company(models.Model):
	"""docstring for company"""
	Symbol 	=	models.CharField(	max_length=100)
	Name 	=	models.CharField( 	max_length=500)
	MarketCap	=	models.FloatField()
	Sector	=	models.CharField(	max_length=500)
	Industry	=	models.CharField(max_length=500)

	class Meta:
		ordering	=	["Symbol"]

	def __str__(self):
		return str(self.id)
	
class Stock(models.Model):
	date		=	models.DateTimeField()
	marketsym	=	models.CharField(max_length=20)
	symbol 		=	models.ForeignKey(company,on_delete=models.CASCADE,null=True,blank=True)
	openp 		=	models.FloatField()
	closep		=	models.FloatField()
	low			=	models.FloatField()
	high		=	models.FloatField()
	volume		=	models.FloatField()

	class Meta:
		ordering	=	["symbol"]

	def __str__(self):
		return self.marketsym